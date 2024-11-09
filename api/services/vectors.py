from gensim.models import word2vec
from typing import List


class WordVectors:
    def __init__(self):
        self.model = word2vec.Word2Vec.load("./models/jawiki-latest-pages-articles.model")

    # 対応する単語がない場合は空のリストを返す
    def most_similar(self, positive: List[str] | None, negative: List[str], topn=2):
        try:
            return self.model.wv.most_similar(positive=positive, negative=negative, topn=topn)
        except Exception:
            return []
