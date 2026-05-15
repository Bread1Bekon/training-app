class AppError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class AuthenticationError(AppError):
    pass


class ForbiddenError(AppError):
    pass


class NotFoundError(AppError):
    pass


class ConflictError(AppError):
    pass
