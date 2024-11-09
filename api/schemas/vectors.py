from pydantic import BaseModel, Field
from typing import List, Tuple


class WordVector(BaseModel):
    """単語と類似度のペア"""

    word: str = Field(..., description="単語")
    similarity: float = Field(..., description="類似度")

    @classmethod
    def from_tuple(cls, tuple_data: Tuple[str, float]) -> "WordVector":
        """タプルからWordVectorを作成"""
        return cls(word=tuple_data[0], similarity=tuple_data[1])


class Word(BaseModel):
    """単語"""

    word: str = Field(..., description="単語")


class WordVectorResponse(BaseModel):
    """API応答モデル"""

    positive_words: List[Word] | None = Field(None, description="足し算した単語リスト")
    negative_words: List[Word] | None = Field(None, description="引き算した単語リスト")
    word_list: List[WordVector] = Field(..., description="単語と類似度のリスト")

    model_config = {
        "json_schema_extra": {
            "example": {
                "positive_words": [{"word": "Python"}, {"word": "プログラミング"}],
                "negative_words": [],
                "word_list": [
                    {"word": "Perl", "similarity": 0.7757585048675537},
                    {"word": "Haskell", "similarity": 0.7603100538253784},
                    {"word": "Java", "similarity": 0.7506471276283264},
                    {"word": "Ruby", "similarity": 0.7455922365188599},
                    {"word": "コンパイラ", "similarity": 0.7398861050605774},
                ],
            }
        }
    }
