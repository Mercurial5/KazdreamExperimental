from typing import Protocol, Callable

import requests
from requests import Response
from requests.exceptions import RequestException, JSONDecodeError


class RequestWrapperInterface(Protocol):
    """
    The purpose of this interface is to ensure that when we create new implementations* of RequestWrapper, we will
    override these methods. Example of usage:

    request_wrapper: RequestWrapperInterface = SomeRequestWrapper()

    Because of this interface we can be sure*, that SomeRequestWrapper will have all the methods we need.


    * For example, we can implement RequestWrapper that uses proxies.
    Or write custom request sender for complex cases.

    * Even though python itself won't throw an error if SomeRequestWrapper won't implement those methods,
    but type checkers like mypy will detect this unexpected behaviour.
    """

    def send(self, method: str, link: str, **kwargs) -> dict:
        """
        Sends request.

        Returns dict with these keys:
        status: bool - Was request successful or no?
        error: str - If status is False, error message will be here
        content: str | dict - If status is Ture, response will be here

        :return:
        """


class RequestWrapper:
    def send(self, method: str, link: str, **kwargs) -> dict:
        send_method = self._get_method(method)

        try:
            response = send_method(link, **kwargs)
        except RequestException as e:
            return dict(status=False, error=str(e))

        if kwargs.get('to_json'):
            try:
                response = response.json()
            except JSONDecodeError as e:
                return dict(status=False, error=str(e))
        else:
            response = response.text

        return dict(status=True, content=response)

    @staticmethod
    def get(link: str, **kwargs) -> Response:
        return requests.get(link, **kwargs)

    def _get_method(self, name: str) -> Callable[[str, dict], Response]:
        match name:
            case 'GET':
                return self.get
            case _:
                raise ValueError(f'Method {name} not found in {self.__class__.__name__}')
