from fastapi import APIRouter, Query, HTTPException
from api.services import vectors as vectors_service
from api.schemas import vectors as vectors_schema
from api.schemas.response import BadRequestError, NotFoundError, TypedHTTPException
from api.services import tokenizer

router = APIRouter(prefix="/api/v1", tags=["vectors"])
mecab = tokenizer.Tokenizer()
vector = vectors_service.WordVectors()


@router.get(
    "/vectors",
    response_model=vectors_schema.WordVectorResponse,
    responses={
        400: {"model": BadRequestError, "description": "入力値が不正な場合のエラー"},
        404: {"model": NotFoundError, "description": "類似する単語が見つからなかった場合のエラー"},
        500: {"description": "サーバー内部エラー"},
    },
    response_description="単語ベクトルの計算結果",
    summary="単語ベクトルの計算",
    description="単語同士の足し算・引き算を行い、類似する単語を返却します",
)
async def calculate_vectors(
    positive: str | None = Query(
        default=None, description="足し算したい単語（カンマ区切り。例：Python,プログラミング）"
    ),
    negative: str | None = Query(default=None, description="引き算したい単語（カンマ区切り。例：パソコン）"),
    topn: int = Query(default=5, ge=1, le=20),
) -> vectors_schema.WordVectorResponse:
    try:
        if positive is None and negative is None:
            raise TypedHTTPException(
                error_response=BadRequestError(message="positiveまたはnegativeワードのいずれかは必須です。")
            )

        _positive_terms = positive.split(",") if positive else []
        _negative_terms = negative.split(",") if negative else []

        # 各単語を分かち書きする
        wakati_positive_terms = mecab.tokenize_list(_positive_terms)
        wakati_negative_terms = mecab.tokenize_list(_negative_terms)

        similar_words = vector.most_similar(positive=wakati_positive_terms, negative=wakati_negative_terms, topn=topn)

        if not similar_words:
            raise TypedHTTPException(
                error_response=NotFoundError(message="類似する単語が見つかりませんでした。別の単語で試してください。")
            )

        vectors = [vectors_schema.WordVector.from_tuple(word_tuple) for word_tuple in similar_words]
        _positive_words = [vectors_schema.Word(word=word) for word in _positive_terms]
        _negative_words = [vectors_schema.Word(word=word) for word in _negative_terms]

        return vectors_schema.WordVectorResponse(
            positive_words=_positive_words, negative_words=_negative_words, word_list=vectors
        )
    except TypedHTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
