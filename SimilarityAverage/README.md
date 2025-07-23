# SimilarityAverage

## 概要

複数の顔画像と平均顔画像の類似度を計算し、ランキング付きでテキスト出力するPythonツールです。  
OpenCV・scikit-learnを利用し、FaceAnalyzerクラスで特徴量抽出・類似度計算を行います。  
Docker対応済みで、簡単に環境構築・実行が可能です。

---

## ディレクトリ構成

```
SimilarityAverage/
  ├─ cropped_faces/  # 入力用の顔画像（jpg, png等）をここに配置
  ├─ average/        # 平均顔画像（average_face.jpg）をここに配置
  ├─ output/         # 類似度計算結果（similarity_results.txt）がここに出力されます
  ├─ main.py
  ├─ face_analyzer.py
  ├─ requirements.txt
  └─ Dockerfile
```

---

## 使い方

### 1. Dockerで実行する場合

#### ビルド

```
docker build -t similarity-average .
```

#### 実行（1行コマンド例・Windows PowerShell）

```
docker run -v ${PWD}\cropped_faces:/app/cropped_faces -v ${PWD}\average:/app/average -v ${PWD}\output:/app/output similarity-average
```

- `cropped_faces` フォルダに顔画像を入れてから実行してください。
- `average` フォルダに `average_face.jpg` を入れてください。
- `output` フォルダに `similarity_results.txt` が出力されます。

> ※ Mac/Linuxの場合は「$(pwd)」に、コマンドプロンプトの場合は「%cd%」に置き換えてください。

---

### 2. ローカルで実行する場合

#### 依存パッケージのインストール

```
pip install -r requirements.txt
```

#### 実行

```
python main.py
```

- `cropped_faces` フォルダに顔画像を入れてから実行してください。
- `average` フォルダに `average_face.jpg` を入れてください。
- `output/similarity_results.txt` に結果が出力されます。

---

## 主な依存パッケージ

- opencv-python
- numpy
- scikit-learn
- matplotlib

---

## 補足

- 入力画像・平均顔画像は自動で128x128にリサイズされます。
- 出力ファイル名は `output/similarity_results.txt` です。
- Docker実行時に `output` ディレクトリをマウントすれば、ホスト側で結果を受け取れます。

---
