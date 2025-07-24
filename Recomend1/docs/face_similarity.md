# 顔画像処理・類似度計算の仕組み

## 0. 本プロジェクトでの実際の手法

- **顔検出**：`CroppedAnimeFace/anime_face_detector.py`でAnimeFaceDetector（アニメ顔専用の深層学習モデル）を利用し、画像からアニメキャラの顔領域を自動検出。
- **顔画像の切り出し**：検出した顔を128x128ピクセルにリサイズし、`CroppedAnimeFace/output/`や`CreateAverageFace/cropped_faces/`に保存。
- **平均顔生成**：`CreateAverageFace/main.py`で、複数の顔画像を画素ごとに平均化（ピクセル平均）して平均顔画像を作成。
- **特徴量抽出・類似度計算**：`SimilarityAverage/face_analyzer.py`等で、顔画像から深層学習モデル（例：VGGFaceや独自モデル）で特徴ベクトルを抽出し、
  - 「ユーザーの推しキャラの平均顔の特徴量」と「各キャラ顔特徴量」からコサイン類似度を計算。
- **類似度記録**：計算結果を`SimilarityAverage/output/similarity_results.txt`や`Recomend1/data/similarity_results.csv`に保存。
- **レコメンド**：`Recomend1/main.py`で、類似度・レビュー・ジャンル好み等を合成スコア化し、未視聴アニメを推薦。

---

## 1. 画像からアニメ顔画像を抜き取る仕組み

### (1) 顔検出
- 画像から顔領域を自動検出する。
- 一般的な手法：OpenCVのHaar Cascade、Dlib、MTCNN、YOLO、アニメ顔専用モデル（AnimeFaceDetectorなど）
- 本プロジェクト例：`CroppedAnimeFace/anime_face_detector.py`でAnimeFaceDetectorを利用

### (2) 顔領域の切り出し・保存
- 検出した顔領域を画像から切り出し、一定サイズ（例: 128x128）にリサイズ
- 1枚の画像から複数の顔を検出・保存可能
- 切り出し画像は`cropped_faces/`や`output/`ディレクトリに保存

---

## 2. 平均顔の作り方

### (1) 顔画像の前処理
- 切り出した顔画像を同じサイズ・同じ顔向きに揃える（アライメント）
- 画像をグレースケール化や正規化する場合も

### (2) 平均顔の生成
- 複数の顔画像を画素ごとに平均化（ピクセル平均）
  - 例：N枚の画像の各ピクセル値を足してNで割る
- もしくは、顔特徴ベクトル（深層学習モデルの出力）を平均化し、平均顔特徴ベクトルを作る
- 平均顔画像は`CreateAverageFace/main.py`などで生成

---

## 3. 類似度の測定方法

### (1) 特徴量抽出
- 顔画像を深層学習モデル（例: VGGFace, 独自アニメ顔モデル）に入力し、特徴ベクトルを得る
- 特徴ベクトルは128次元や512次元など

### (2) 類似度計算
- コサイン類似度（cosine similarity）を用いるのが一般的
  - 数式: similarity = (A・B) / (||A|| * ||B||)
  - 1に近いほど似ている
- **「ユーザーの推しキャラの平均顔の特徴量」と「各キャラ顔特徴量」からコサイン類似度を計算**
- 結果を`similarity_results.csv`に保存

### (3) 閾値設定
- 類似度が0.8以上など、しきい値を設けて“推し候補”を抽出
- 分布に応じて動的に調整も可能

---

## 4. 参考実装例
- 顔検出: `CroppedAnimeFace/anime_face_detector.py`
- 平均顔生成: `CreateAverageFace/main.py`
- 類似度計算: `SimilarityAverage/main.py` など

---

## 5. 応用・発展
- 顔特徴以外（髪色・目の形・表情など）も特徴量として加味可能
- GAN等で“理想の推し顔”を生成し、類似度を測る応用も 