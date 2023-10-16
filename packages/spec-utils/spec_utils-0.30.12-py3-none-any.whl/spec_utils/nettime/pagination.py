from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from .containers.container import Container


class PageNumberPagination:
    def __init__(
        self,
        items,
        container: "Container",
        method_name: str,
        params=None,
        page: int = 1,
    ) -> None:
        self._items = items
        self._page = page
        self._container = container
        self._params = params
        self._method_name = method_name

    def __iter__(self):
        yield from self._items

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int):
        return self._items[index]

    def __setitem__(self, index: int, value) -> None:
        self._items[index] = value

    def next_page(self) -> PageNumberPagination:
        self._page += 1
        return getattr(self._container, self._method_name)(
            page=self._page, **self._params
        )

    def prev_page(self) -> PageNumberPagination:
        self._page -= 1
        return getattr(self._container, self._method_name)(
            page=self._page, **self._params
        )



class LimitOffsetPagination:
    
    def __init__(
        self,
        items: Iterable,
        container: "Container",
        method_name: str,
        params: dict = {},
        offset: int = 0,
    ) -> None:
        self._items = items
        self._offset = offset
        self._container = container
        self._params = params
        self._method_name = method_name


    def __iter__(self):
        yield from self._items


    def __len__(self) -> int:
        return len(self._items)


    def __getitem__(self, index: int):
        return self._items[index]


    def __setitem__(self, index: int, value) -> None:
        self._items[index] = value


    @property
    def all(self) -> list:
        return self._items
    

    @property
    def page_size(self) -> int:
        return self._container.page_size


    def next_page(self) -> LimitOffsetPagination:
        self._offset += self.page_size
        return getattr(self._container, self._method_name)(
            offset=self._offset, **self._params
        )


    def prev_page(self) -> LimitOffsetPagination:
        self._offset += self.page_size
        return getattr(self._container, self._method_name)(
            offset=self._offset, **self._params
        )