from fastapi import HTTPException, status


class AppError(HTTPException):
    """Base for all"""

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "Client error",
        headers: dict = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundError(AppError):
    """Not found"""

    def __init__(self, detail: str = "Entity is not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{detail}")


class ExternalAPIError(HTTPException):
    """External API Error"""

    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers: dict = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
