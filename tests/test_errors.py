from app.errors import (
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
)


def test_error_status_codes():
    assert AuthenticationError("bad credentials").status_code == 401
    assert ForbiddenError("no access").status_code == 403
    assert NotFoundError("missing").status_code == 404
    assert ConflictError("duplicate").status_code == 409
