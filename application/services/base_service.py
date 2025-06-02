from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

RequestType = TypeVar('RequestType')
ResponseType = TypeVar('ResponseType')


class BaseService(ABC):

    @abstractmethod
    def handle(self, request: RequestType) -> ResponseType:
        pass

    @abstractmethod
    def validate_request(self, request: RequestType) -> None:
        pass
