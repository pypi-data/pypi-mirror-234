import os
from typing import Optional, Dict, Any
from unittest.mock import MagicMock

import lsjsonclasses
import requests
from requests import Session

import re

from lsrestclient import (
    LsRestClientResponse,
    exceptions,
)
from lsrestclient.contexts.bearer_token import bearer_token_context

find_parameters_regex = re.compile("{(.*?)}")


class LsRestClient(Session):
    _clients = {}

    @classmethod
    def from_env(
        cls,
        env_name: str,
        name: Optional[str] = None,
        required: bool = True,
    ):
        """
        Create an instance of the LsRestClient class using environment variables.
        It gets globally saved under the given name, so that it can be reused.

        :param env_name: The name of the environment variable that holds the base URL.
        :param name: An optional name for the client instance.
        :param required: A flag indicating whether the environment variable is required. Defaults to True.
        :return: An instance of the LsRestClient class.
        """
        base_url = os.environ.get(env_name, "")
        if base_url == "" and required:
            raise EnvironmentError(f"Environment variable '{env_name}' needs to be set")

        return cls(base_url=base_url, name=name)

    @classmethod
    def client(cls, name: str):
        """
        Retrieves the LsRestClient instance with the specified name.
        If a client with the given name does not exist, an exception is raised.

        :param name: The name of the LsRestClient to be retrieved.
        :return: The LsRestClient instance with the given name.
        """
        try:
            return cls._clients[name]
        except KeyError:
            raise Exception(f"LsRestClient with name '{name}' not initialized.")

    def __init__(
        self,
        base_url: str = None,
        name: str = "default",
    ) -> None:
        """Class representing a REST client for JSON API."""

        self._mocks = {}
        self.base_url = base_url
        self.base_headers = {"content-type": "application/json"}
        self.name = name
        super().__init__()
        self._clients[name] = self

    @staticmethod
    def mock_name(client_name: str, method: str, url: str) -> str:
        return f"{client_name}_{method.upper()}_{url}"

    def full_url(
        self,
        url: str,
        params: Optional[dict] = None,
    ) -> str:
        """
        Builds a full url from the base_url with url parameters replaced.

        :param url: The relative URL to be used to build the full URL.
        :param params: An optional dictionary that contains the parameters to be used in formatting the URL.
                       Default is None. Used parameters get removed from the dictionary.
        :return: The full URL with the parameters replaced.
        """
        if params is None:
            params = {}

        full_url = f"{self.base_url}{url}"
        found = find_parameters_regex.findall(full_url)
        url_params = {p: params[p] for p in found}
        for p in found:
            del params[p]
        return full_url.format(**url_params)

    def caller(self, method: str, url: str, *args, **kwargs) -> LsRestClientResponse:
        # check mocks
        mock = self._mocks.get(self.mock_name(self.name, method, url), None)
        func = mock if mock is not None else self.request
        return func(method, url, *args, **kwargs)

    def request(
        self,
        method: str,
        url: str,
        *args,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> LsRestClientResponse:  # pragma: no cover
        """
        :param method: The HTTP method to be used for the request.
        :param url: The URL endpoint for the request.
        :param args: Additional arguments for the request.
        :param params: Optional query parameters for the request.
        :param body: Optional request body in JSON format.
        :param kwargs: Additional keyword arguments for the request.
        :return: An instance of LsRestClientResponse.

        This method sends an HTTP request using the provided method, URL, parameters, and body.
        It returns an instance of LsRestClientResponse which represents the response received from the server.

        The `method` parameter specifies the HTTP method to be used for the request,
        e.g., 'GET', 'POST', 'PUT', 'DELETE', etc.

        The `url` parameter specifies the URL endpoint for the request.

        The `args` parameter is used to pass additional arguments to the underlying `Session.request` method.
        These arguments are passed directly to the `requests.request` function.

        The `params` parameter is an optional dictionary of query parameters to be included in the request URL.
        This can be used to include query parameters in the URL, e.g., '/endpoint?key=value'.

        The `body` parameter is an optional dictionary representing the request body in JSON format.
        This can be used to send data in the request body for methods like 'POST' or 'PUT'.

        The `kwargs` parameter is used to pass additional keyword arguments to the underlying `Session.request` method.
        These keyword arguments are passed directly to the `requests.request` function.

        The returned value is an instance of LsRestClientResponse, which represents the response received from the
        server. This object provides various properties and methods to access the response data.

        Note: This method raises a `ConnectionError` if a connection error occurs during the request.
        """
        # apply base_headers

        with bearer_token_context() as bearer_token:
            bearer_headers = {"Authorization": f"Bearer {bearer_token}"} if bearer_token is not None else {}

        headers = self.base_headers | bearer_headers | kwargs.get("headers", {})

        kwargs |= dict(headers=headers)

        # params
        if params is None:
            params = {}
        if body is not None:
            kwargs["data"] = lsjsonclasses.LSoftJSONEncoder.dumps(body).encode("utf8")

        full_url = self.full_url(url, params)

        try:
            requests_response = requests.request(
                method.upper(),
                full_url,
                *args,
                params=params,
                **kwargs,
            )
            response = LsRestClientResponse.from_requests_response(requests_response)
            return response

        except requests.ConnectionError:
            raise exceptions.ConnectionError(url=full_url)

    def get(self, *args, **kwargs) -> LsRestClientResponse:
        """
        Send a GET request to the specified URL.

        :param args: Positional arguments used to construct the URL.
        :param kwargs: Additional keyword arguments for the request.
        :return: The response object of type LsRestClientResponse.
        """
        return self.caller("GET", *args, **kwargs)

    def post(self, *args, **kwargs) -> LsRestClientResponse:
        """
        This method is used to send a POST request using the LSRestClient class.

        :param args: The positional arguments for the POST request, including the URL and any additional parameters.
        :param kwargs: The keyword arguments for the POST request, including headers, body, and any other parameters.
        :return: An instance of LsRestClientResponse, representing the response from the POST request.
        """
        return self.caller("POST", *args, **kwargs)

    def put(self, *args, **kwargs) -> LsRestClientResponse:
        """
        This method is used to send a PUT request using the LSRestClient class.

        :param args: The arguments to be passed to the request.
        :param kwargs: The keyword arguments to be passed to the request.
        :return: An instance of LsRestClientResponse representing the response from the server.
        """
        return self.caller("PUT", *args, **kwargs)

    def patch(self, *args, **kwargs) -> LsRestClientResponse:
        """
        Send a PATCH request to the specified URL with the provided arguments.

        :param args: The arguments for the PATCH request.
        :param kwargs: The keyword arguments for the PATCH request.
        :return: The response from the PATCH request as an `LsRestClientResponse` object.
        """
        return self.caller("PATCH", *args, **kwargs)

    def delete(self, *args, **kwargs) -> LsRestClientResponse:
        """
        Deletes a resource using the DELETE method.

        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: An instance of LsRestClientResponse.
        """
        return self.caller("DELETE", *args, **kwargs)

    def options(self, *args, **kwargs) -> LsRestClientResponse:
        """
        Send an OPTIONS request using the LsRestClient.

        :param args: Additional positional arguments to be passed to the request.
        :param kwargs: Additional keyword arguments to be passed to the request.
        :return: LsRestClientResponse object containing the response of the OPTIONS request.
        """
        return self.caller("OPTIONS", *args, **kwargs)

    def head(
        self,
        *args: object,
        **kwargs: object,
    ) -> object:
        """
        Send a HEAD request to the specified URL.

        :param args: Positional arguments passed to the `request` method.
        :param kwargs: Keyword arguments passed to the `request` method.
        :return: The response object from the request.
        """
        return self.request("HEAD", *args, **kwargs)

    def mock(self, mock_name: str, mock: MagicMock):
        self._mocks[mock_name] = mock

    def unmock(self, mock_name: str):
        if mock_name in self._mocks:
            del self._mocks[mock_name]
