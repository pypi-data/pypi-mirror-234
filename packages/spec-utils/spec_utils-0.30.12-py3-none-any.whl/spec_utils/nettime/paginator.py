from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .container import Container


class Paginator:
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

    def next_page(self) -> Paginator:
        self._page += 1
        return getattr(self._container, self._method_name)(
            page=self._page, **self._params
        )

    def prev_page(self) -> Paginator:
        self._page -= 1
        return getattr(self._container, self._method_name)(
            page=self._page, **self._params
        )
