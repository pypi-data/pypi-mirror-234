from dataclasses import dataclass
from typing import Optional

import lsjsonclasses
from requests import Response
from requests.structures import CaseInsensitiveDict


@dataclass
class LsRestClientResponse:
    """
    Represents a response from the LsRestClient.
    """

    status_code: int
    content: str
    headers: CaseInsensitiveDict

    _json: Optional[dict] = None

    def json(self):
        if self._json is None:
            self._json = lsjsonclasses.LSoftJSONDecoder.loads(self.content)
        return self._json

    @classmethod
    def from_requests_response(cls, response: Response):
        """
        Create an instance of LsRestClientResponse from a requests Response object.

        :param response: The requests Response object.
        :type response: Response
        :return: An instance of LsRestClientResponse representing the response.
        :rtype: LsRestClientResponse
        """
        return cls(
            status_code=response.status_code,
            content=response.content.decode("utf8"),
            headers=response.headers,
        )

    @classmethod
    def from_dict(cls, status_code: int = 200, data: dict = None, headers: CaseInsensitiveDict = None):
        """
        Converts a dictionary into an instance of the LsRestClientResponse class.

        :param status_code: The HTTP status code. Defaults to 200.
        :param data: The data dictionary. Defaults to None.
        :param headers: The headers dictionary. Defaults to None.
        :return: An instance of the LsRestClientResponse class.

        """
        if data is None:
            data = {}
        if headers is None:
            headers = {}

        content = lsjsonclasses.LSoftJSONEncoder.dumps(data)

        return cls(status_code=status_code, content=content, headers=headers)
