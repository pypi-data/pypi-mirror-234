"""
Service - Network Provider
"""

from typing import Optional
import requests
from rkstreamer.interfaces.network import INetworkProvider, INetworkProviderResponse


def hook_raise_status(data: INetworkProviderResponse, *args, **kwargs) -> Optional[INetworkProviderResponse]:
    """Check for return status code"""
    try:
        data.raise_for_status()
    except requests.exceptions.HTTPError as exception:
        raise SystemExit(exception) from None
    return data


def requests_wrapper(function) -> INetworkProviderResponse:
    """Wrapper for Request calls"""
    def wrapper(*args, **kwargs):
        try:
            kwargs.update(
                {'hooks': {'response': [hook_raise_status]}})
            response = function(*args, **kwargs)
            return response
        except requests.exceptions.RequestException as exception:
            raise SystemExit(exception) from None
    return wrapper


class PyRequests(INetworkProvider):
    """HTTP Requests bundle for making calls to Stream APIs"""

    def __init__(self, **kwargs) -> None:

        # Creating a Requests Session and passing below parameters to be persistent.
        self.session = requests.session()
        self.session.proxies = kwargs.pop('proxy', None)
        self.session.verify = False
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
        self.kwargs = kwargs
        self.response = {}

    @requests_wrapper
    def get(self, **kwargs):
        self.response = self.session.get(**kwargs | self.kwargs)
        return self.response


class PyResponse(INetworkProviderResponse):
    """HTTP Requests Response"""

    def __init__(self) -> None:
        self.response = requests.Response()

    @property
    def headers(self):
        return self.response.headers

    @property
    def status_code(self):
        return self.response.status_code

    def json(self):
        return self.response.json()

    def raise_for_status(self):
        return self.response.raise_for_status()


__all__ = ['PyRequests']
