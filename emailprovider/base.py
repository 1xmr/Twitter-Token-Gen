from abc import abstractmethod
from enum import Enum
import typing as tp


class EmailException(Exception):
    def __init__(self, message: str, error_type: "EmailErrorType"):
        super().__init__(message)
        self.error_type = error_type


class EmailErrorType(Enum):
    NO_BALANCE = 1
    CANNOT_FETCH_OTP = 2
    CANNOT_GET_EMAIL = 3
    NO_STOCK = 4


class EmailResponse(object):
    def __init__(self, email: str, password: str, task_id: "tp.Optional[str]" = None):
        self.email      = email
        self.password   = password
        self.task_id    = task_id


class EmailMatch(object):
    def __init__(self, pattern: "tp.Optional[str]" = None, subject: "tp.Optional[str]" = None):
        self.pattern = pattern
        self.subject = subject.lower() if subject else subject


class BaseEmailService(object):
    def __init__(self, api_key: str):
        self._api_key = api_key

    @abstractmethod
    def get_email(self) -> "EmailResponse":
        ...

    @abstractmethod
    def get_otp(
            self,
            email_response: "EmailResponse",
            email_match: "EmailMatch",
            timeout: float = 60.0
    ) -> str:
        ...

    @abstractmethod
    def balance(self) -> float:
        ...
