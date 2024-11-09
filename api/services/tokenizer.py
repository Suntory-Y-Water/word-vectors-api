import MeCab
from typing import List


class Tokenizer:
    def __init__(self):
        self.mecab = MeCab.Tagger("-Owakati")

    def tokenize(self, text: str) -> List[str]:
        """
        テキストを分かち書きしてリストで返す

        Args:
            text (str): 分かち書きする文字列

        Returns:
            List[str]: 分かち書きされた単語のリスト
        """
        # MeCabで形態素解析
        node = self.mecab.parseToNode(text)
        tokens = []

        while node:
            # 表層形を取得（実際の単語）
            surface = node.surface
            # 品詞情報を取得
            features = node.feature.split(",")

            # 空白と記号は除外
            if surface and features[0] not in ["記号", "BOS/EOS"]:
                tokens.append(surface)

            node = node.next

        return tokens

    def tokenize_list(self, texts: List[str]) -> List[str]:
        """
        文字列のリストを受け取り、全ての文字列を分かち書きした結果をリストで返す

        Args:
            texts (List[str]): 分かち書きする文字列のリスト

        Returns:
            List[str]: 分かち書きされた全ての単語のリスト
        """
        all_tokens = []
        for text in texts:
            tokens = self.tokenize(text)
            all_tokens.extend(tokens)
        return all_tokens
