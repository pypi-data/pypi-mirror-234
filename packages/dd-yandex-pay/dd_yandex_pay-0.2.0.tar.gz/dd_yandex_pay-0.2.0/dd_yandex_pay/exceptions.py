from typing import Optional

from requests import Response


class BaseYPError(Exception):
    """
    Base DD Yandex Pay Exception.
    """

    default_message = "Base Yandex Pay exception."
    default_code = "base_ddyp_exception"

    def __init__(self, message: Optional[str] = None, code: Optional[str] = None):
        self.code = code or self.default_code
        self.message = message or self.default_message
        super().__init__(f"Error {self.code}: {self.message}")


class YandexPayAPIError(BaseYPError):
    """
    General Yandex Pay API Exception.
    """

    default_message = "Yandex Pay exception."
    default_code = "ddyp_exception"

    def __init__(
        self,
        response: Response,
        message: Optional[str] = None,
        code: Optional[str] = None,
    ):
        self.response = response
        super().__init__(message, code)
