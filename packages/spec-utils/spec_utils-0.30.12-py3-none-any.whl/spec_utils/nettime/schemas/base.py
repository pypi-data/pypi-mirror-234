from typing import Optional, TypeVar
from typing import Optional
from pydantic import BaseModel, Extra


class Base(BaseModel, extra=Extra.allow):
    id: Optional[int]
    name: Optional[str]

    @property
    def _extra(self) -> set[str]:
        return set(self.__dict__) - set(self.__fields__)

ModelType = TypeVar("ModelType", bound=Base)