from abc import abstractmethod
from enum import Enum


class CaptchaException(Exception):
    def __init__(self, message: str, error_type: "CaptchaErrorType"):
        super().__init__(message)
        self.error_type = error_type


class CaptchaErrorType(Enum):
    NO_BALANCE = 1


class TaskType(Enum):
    FUNCAPTCHA = 1


class BaseTask(object):
    def __init__(self, _type: "TaskType", public_key: str, page_url: str):
        self.type       = _type
        self.public_key = public_key
        self.page_url   = page_url


class BaseCaptchaService(object):
    def __init__(self, api_key: str):
        self._api_key = api_key

    @abstractmethod
    def get_balance(self):
        """
            Get the account's balance.

            Returns:
                the account's balance.
        """

        ...

    @abstractmethod
    def create_task(self, task: "BaseTask"):
        """
            Initialize and create a captcha task.

            Parameters:
                task (BaseTask): a Task object.
            Returns:
                a task_id
        """

        ...

    @abstractmethod
    def get_task_result(self, task_id: str, timeout: float):
        """
            Get the captcha result.

            Parameters:
                task_id (str): task id got from create_task method
                timeout (float): max timeout to get result

            Returns:
                the captcha result.
        """

        ...
