# CreateAverageFace

## 概要

複数の顔画像から平均顔画像（average_face.jpg）を生成するPythonツールです。  
OpenCVを利用し、顔画像を自動でリサイズ・平均化します。  
Docker対応済みで、簡単に環境構築・実行が可能です。

---

## ディレクトリ構成

```
CreateAverageFace/
  ├─ cropped_faces/  # 入力用の顔画像（jpg, png等）をここに配置
  ├─ output/         # 平均顔画像（average_face.jpg）がここに出力されます
  ├─ main.py
  ├─ requirements.txt
  └─ Dockerfile
```

---

## 使い方

### 1. Dockerで実行する場合

#### ビルド

```
docker build -t create-average-face .
```

#### 実行

```
docker run -v ${PWD}\cropped_faces:/app/cropped_faces -v ${PWD}\output:/app/output create-average-face
```

- `cropped_faces` フォルダに顔画像を入れてから実行してください。
- `output` フォルダに `average_face.jpg` が出力されます。

> ※ PowerShellの場合は「`」で改行、コマンドプロンプトの場合は「^」で改行してください。  
> Mac/Linuxの場合は「\」や「$(pwd)」に置き換えてください。

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
- カレントディレクトリに `average_face.jpg` が出力されます。

---

## 主な依存パッケージ

- opencv-python
- numpy

---

## 補足

- 入力画像は自動で128x128にリサイズされます。
- 出力ファイル名は `average_face.jpg` です。
- Docker実行時に `output` ディレクトリをマウントすれば、ホスト側で結果を受け取れます。

---
