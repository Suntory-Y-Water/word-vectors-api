from pydantic import BaseModel, Field
from typing import Literal
from fastapi import HTTPException


class ErrorResponse(BaseModel):
    status_code: int = Field(..., description="HTTPステータスコード")
    error_code: str = Field(..., description="エラーコード")
    message: str = Field(..., description="エラーメッセージ")


class BadRequestError(ErrorResponse):
    status_code: Literal[400] = 400
    error_code: Literal["BAD_REQUEST"] = "BAD_REQUEST"


class NotFoundError(ErrorResponse):
    status_code: Literal[404] = 404
    error_code: Literal["NOT_FOUND"] = "NOT_FOUND"


class TypedHTTPException(HTTPException):
    def __init__(
        self,
        error_response: ErrorResponse,
    ):
        super().__init__(status_code=error_response.status_code, detail=error_response.model_dump())
