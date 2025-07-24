# 使い方・実行方法

## 1. 必要ファイル
- data/characters.csv
- data/anime_genres.csv
- data/anime_reviews.csv
- data/user_history.csv
- data/similarity_results.csv

## 2. 実行方法
### Docker
```sh
cd Recomend1
docker build -t recomend1-app .
docker run --rm recomend1-app
```
### ローカル
```sh
cd Recomend1
pip install -r requirements.txt
python main.py
```

## 3. カスタマイズ
- main.py内の重み（ALPHA, BETA, GAMMA, DELTA, ジャンル好みスコアの係数）を調整
- 類似度の閾値も調整可能
- CSVを拡充すれば多様なアニメ・キャラ・ユーザーに対応

## 4. CSVの準備
- 顔類似度計算は外部処理で行い、similarity_results.csvに保存
- サンプルCSVはdata/に格納
- 列の意味はREADME.md参照

## 5. 出力例
- 合成スコア順に、アニメタイトル・ジャンル・推しキャラ・レビュー点・理由を詳細表示 