from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(BaseAPIException):
    def __init__(self, detail: str = "Not found") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestException(BaseAPIException):
    def __init__(self, detail: str = "Bad request") -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedException(BaseAPIException):
    def __init__(self, detail: str = "Unauthorized") -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(BaseAPIException):
    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class AuthError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class PermissionError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class UserNotFoundError(HTTPException):
    def __init__(self, detail: str = "User not found") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class InvalidCredentialsError(AuthError):
    def __init__(self) -> None:
        super().__init__(detail="Could not validate credentials")


class InactiveUserError(AuthError):
    def __init__(self) -> None:
        super().__init__(detail="Inactive user")


class UserExistsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )


class RateLimitExceeded(HTTPException):
    def __init__(self, detail: str = "Rate limit exceeded", retry_after: int | None = None) -> None:
        headers = {"Retry-After": str(retry_after)} if retry_after else None
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers=headers,
        )


class AccountLockedException(HTTPException):
    def __init__(self, username: str, lock_duration: int) -> None:
        detail = (
            f"Account '{username}' is temporarily locked due to multiple failed login attempts. "
            f"Please try again in {lock_duration // 60} minutes."
        )
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers={"Retry-After": str(lock_duration)},
        )


class IPBlockedException(HTTPException):
    def __init__(self, ip: str, block_duration: int) -> None:
        detail = (
            f"IP address '{ip}' is temporarily blocked due to multiple failed login attempts. "
            f"Please try again in {block_duration // 60} minutes."
        )
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers={"Retry-After": str(block_duration)},
        )


class LoginBackoffRequired(HTTPException):
    def __init__(self, delay: int, attempts: int, max_attempts: int) -> None:
        detail = (
            f"Please wait {delay} seconds before trying again. "
            f"Failed attempts: {attempts}/{max_attempts}. "
            f"Account will be locked after {max_attempts} failed attempts."
        )
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers={"Retry-After": str(delay)},
        )


class InvalidTokenError(AuthError):
    def __init__(self) -> None:
        super().__init__(detail="Invalid or expired token")
