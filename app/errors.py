from abc import ABC, abstractmethod


class AppError(Exception, ABC):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    @property
    @abstractmethod
    def status_code(self) -> int:
        pass


class AuthenticationError(AppError):
    @property
    def status_code(self) -> int:
        return 401


class ForbiddenError(AppError):
    @property
    def status_code(self) -> int:
        return 403


class NotFoundError(AppError):
    @property
    def status_code(self) -> int:
        return 404


class ConflictError(AppError):
    @property
    def status_code(self) -> int:
        return 409
