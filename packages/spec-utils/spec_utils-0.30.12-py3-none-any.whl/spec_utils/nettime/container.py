from abc import ABC, abstractmethod
from requests import HTTPError, Response
from typing import TYPE_CHECKING, Any
from .pagination import LimitOffsetPagination as Pagination

if TYPE_CHECKING:
    from .client import Client


OFFSET_PARAM_NAME = "pageStartIndex"
LIMIT_PARAM_NAME = "pageSize"


class Container(ABC):
    def __init__(
            self,
            client: "Client",
            page_size: int = 10,
            # order: str = None
        ) -> None:
        super().__init__()
        self._client = client
        self._page_size = page_size
        self._base_path = '/api/container/elements/'

    
    @property
    @abstractmethod
    def path_attribute(self) -> str:
        ...

    @property
    @abstractmethod
    def base_params(self) -> dict:
        ...


    @property
    def path_url(self) -> str:
        return self._base_path + self.path_attribute


    @property
    def url(self) -> str:
        return self._client.url.geturl() + self.path_url
    

    @property
    def page_size(self) -> int:
        return self._page_size


    @page_size.setter
    def page_size(self, value: int) -> None:
        self._page_size = value
    
    
    def _raise_or_return_json(self, response: Response) -> Any:
        """Raise HTTPError before converting response to json

        :param response: Request response object
        """
        try:
            response.raise_for_status()
        except HTTPError:
            raise HTTPError(response.text)

        try:
            json_value = response.json()
        except ValueError:
            return response.content
        else:
            return json_value
        
    
    def list(self, offset: int = 0, params: dict = {}) -> "Pagination":
        # inner_params = params or {}
        params.update({
            OFFSET_PARAM_NAME: offset,
            LIMIT_PARAM_NAME: self.page_size
        })
        _params = self.base_params
        _params.update(params)
        
        # print("using params", _params)
        response = self._client.get(url=self.url, params=_params)
        return Pagination(
            items=response.get('items', []),
            container=self,
            method_name="list",
            params={"params": _params},
            offset=offset,
        )
    
    
    def all(self, params: dict = {}, page=None) -> Any:        
        if not page:
            page = self.list(params=params)
            for item in page: yield item

        page = page.next_page()
        if not page: return
        for item in page: yield item
        yield from self.all(params=params, page=page)


class Employee(Container):
    path_attribute = ""
    order = "Apellidos_Nombre"
    container_name = "Persona"

    @property
    def base_params(self) -> dict:
        return {
            "container": self.container_name,
            "order": self.order
        }