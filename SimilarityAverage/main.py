#!/usr/bin/env python3
"""
平均顔との類似度測定スクリプト（FaceAnalyzer準拠）

機能:
- 指定フォルダ内の顔画像と平均顔画像を読み込み
- 元プログラムと同じ FaceAnalyzer クラスで類似度を計算
- 結果をテキストファイルに保存
"""

import os
import glob
import cv2
import numpy as np

from face_analyzer import FaceAnalyzer  # 元スクリプトと同じ実装を使う

def load_faces_from_dir(directory: str, size: tuple) -> list:
    """指定ディレクトリ内の顔画像を読み込んで返す"""
    image_paths = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']:
        image_paths.extend(glob.glob(os.path.join(directory, ext)))
        image_paths.extend(glob.glob(os.path.join(directory, ext.upper())))

    faces = []
    filenames = []
    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"警告: 読み込み失敗: {path}")
            continue
        img = cv2.resize(img, size)
        faces.append(img)
        filenames.append(os.path.basename(path))

    return faces, filenames

def main():
    # 設定
    faces_dir = "cropped_faces"
    average_face_path = "average/average_face.jpg"
    image_size = (128, 128)
    output_txt = "output/similarity_results.txt"

    print("=" * 50)
    print("平均顔との類似度計算（FaceAnalyzer準拠）")
    print("=" * 50)

    # 平均顔読み込み
    avg_face = cv2.imread(average_face_path)
    if avg_face is None:
        print(f"エラー: 平均顔画像の読み込みに失敗しました: {average_face_path}")
        return
    avg_face = cv2.resize(avg_face, image_size)

    # 顔画像読み込み
    faces, filenames = load_faces_from_dir(faces_dir, image_size)
    if not faces:
        print(f"エラー: {faces_dir} に有効な顔画像が見つかりません")
        return

    print(f"✓ 顔画像: {len(faces)}枚 読み込み完了")

    # 類似度計算（元の実装を利用）
    analyzer = FaceAnalyzer()
    similarities = analyzer.calculate_similarities_to_average(faces, avg_face)

    # 結果を保存
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write("平均顔との類似度結果（FaceAnalyzer準拠）\n")
        f.write("=" * 50 + "\n\n")

        for filename, sim in zip(filenames, similarities):
            f.write(f"{filename:<30} 類似度: {sim:.4f}\n")

        f.write("\n類似度順ランキング:\n")
        f.write("-" * 50 + "\n")
        sorted_items = sorted(zip(filenames, similarities), key=lambda x: x[1], reverse=True)
        for rank, (filename, sim) in enumerate(sorted_items, 1):
            f.write(f"{rank:2d}位: {filename:<30} 類似度: {sim:.4f}\n")

    print(f"✓ 類似度の計算と保存が完了しました: {output_txt}")

if __name__ == "__main__":
    main()
