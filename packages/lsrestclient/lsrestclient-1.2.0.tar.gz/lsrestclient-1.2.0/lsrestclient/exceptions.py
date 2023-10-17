from typing import Optional


# noinspection PyShadowingBuiltins
class ConnectionError(Exception):
    """Exception class for connection errors.

    Args:
        url (Optional[str]): The URL that the connection could not be established to.

    Attributes:
        url (Optional[str]): The URL that the connection could not be established to.

    Raises:
        ConnectionError: If a connection could not be established to the given URL.

    """

    url: str

    def __init__(self, url: Optional[str] = None) -> None:
        self.url = url
        super().__init__(f"Connection could not be established to '{url}'")


class DownStreamError(Exception):
    status_code: int
    url: str
    content: str

    def __init__(self, url: str, status_code: int, content: str) -> None:
        self.url = url
        self.status_code = status_code
        self.content = content
        super().__init__(f"Downstream error calling {self.url}. {self.status_code} {self.content}")
