# CroppedAnimeFace

## 概要

アニメ画像から顔を自動検出し、指定サイズに切り抜いて保存するPythonツールです。
OpenCVと独自のアニメ顔検出モデル（lbpcascade_animeface）を利用しています。
Docker対応済みで、簡単に環境構築・実行が可能です。

---

## ディレクトリ構成

```
CroppedAnimeFace/
  ├─ input/      # 入力画像（jpg, png等）をここに配置
  ├─ output/     # 切り抜かれた顔画像がここに出力されます
  ├─ models/     # アニメ顔検出モデル（自動ダウンロードされます）
  ├─ main.py
  ├─ anime_face_detector.py
  ├─ requirements.txt
  └─ Dockerfile
```

---

## 使い方

### 1. Dockerで実行する場合

#### ビルド

```
docker build -t cropped-anime-face .
```

#### 実行

```
docker run -v ${PWD}\input:/app/input ${PWD}\output:/app/output -v ${PWD}\models:/app/models 
```

- `input` フォルダに画像を入れてから実行してください。
- `output` フォルダに切り抜かれた顔画像が出力されます。

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

---

## 主な依存パッケージ

- opencv-python
- numpy
- Pillow
- scikit-learn
- matplotlib
- scipy
- requests
- tqdm

---

## 補足

- 顔検出モデル（lbpcascade_animeface.xml）は自動でダウンロードされます。
- `models/lbpcascade_animeface.xml` は `.gitignore` 推奨です（大きなファイルのため）。

---

## ライセンス

- 顔検出モデル: [nagadomi/lbpcascade_animeface](https://github.com/nagadomi/lbpcascade_animeface) (MIT)