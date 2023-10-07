"""
DI module for network requests
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from ._interface import ABC, abstractmethod

if TYPE_CHECKING:
    from rkstreamer.types import (
        NetworkProviderResponseType
    )

class INetworkProvider(ABC):
    """Interface for Network Providers"""

    @abstractmethod
    def get(self, **kwargs) -> NetworkProviderResponseType:
        """GET request method"""


class INetworkProviderResponse(ABC):
    """Interface for Response object returned by Network Providers"""

    @abstractmethod
    def json(self) -> dict:
        """Return JSONified response"""

    @property
    @abstractmethod
    def headers(self) -> dict:
        """Response headers"""

    @property
    @abstractmethod
    def status_code(self) -> int:
        """Response code"""

    @abstractmethod
    def raise_for_status(self) -> None:
        """Raise for validating response status"""
