from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.router import vectors
from api.schemas.response import TypedHTTPException

app = FastAPI()


# エラーハンドラー
@app.exception_handler(TypedHTTPException)
async def typed_http_exception_handler(_request: Request, exc: TypedHTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


app.add_middleware(
    CORSMiddleware,
    # ローカルホストからのアクセスを許可  # Docker内のサービスからのアクセスを許可
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)
app.include_router(vectors.router)
