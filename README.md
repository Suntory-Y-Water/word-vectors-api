# word-vectors

## セットアップ

パッケージのインストール

```bash
poetry install
```

開発サーバーの起動

```bash
uvicorn api.main:app --reload --port 8000 --host 0.0.0.0
```

起動を確認後、`http://localhost:8000/docs`にアクセスします。

## 実行例

`http://localhost:8000/api/vectors?positive=水瀬いのり`にアクセスすると、下記のようなレスポンスを得ることができます。

```json
{
  "positive_words": [
    {
      "word": "水瀬いのり"
    }
  ],
  "negative_words": [],
  "word_list": [
    {
      "word": "水樹",
      "similarity": 0.745496988296509
    },
    {
      "word": "裕香",
      "similarity": 0.732845783233643
    },
    {
      "word": "奈々",
      "similarity": 0.722927331924439
    },
    {
      "word": "愛美",
      "similarity": 0.713139891624451
    },
    {
      "word": "咲",
      "similarity": 0.69900643825531
    }
  ]
}
```