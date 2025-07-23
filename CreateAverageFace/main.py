"""
平均顔作成スクリプト

機能:
- 指定ディレクトリにある顔画像を読み込み
- 画像を平均化して平均顔を生成
- 結果を保存
"""

import os
import glob
import cv2
import numpy as np

def load_faces(directory: str, size: tuple) -> list:
    """指定ディレクトリから顔画像を読み込んでリストで返す"""
    image_paths = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']:
        image_paths.extend(glob.glob(os.path.join(directory, ext)))
        image_paths.extend(glob.glob(os.path.join(directory, ext.upper())))

    faces = []
    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"警告: 読み込み失敗: {path}")
            continue
        img = cv2.resize(img, size)  # 念のためサイズを揃える
        faces.append(img.astype(np.float32))

    return faces

def create_average_face(faces: list) -> np.ndarray:
    """顔画像のリストから平均顔を作成"""
    avg_face = np.mean(faces, axis=0)
    avg_face = np.clip(avg_face, 0, 255).astype(np.uint8)
    return avg_face

def main():
    # 設定
    faces_dir = "cropped_faces"  # 入力ディレクトリ（切り抜き顔画像が入っている場所）
    output_path = "output/average_face.jpg"
    image_size = (128, 128)  # 顔画像サイズ

    print("=" * 50)
    print("平均顔作成ツール")
    print("=" * 50)

    # 顔画像を読み込む
    faces = load_faces(faces_dir, image_size)
    if not faces:
        print(f"エラー: {faces_dir} に有効な画像が見つかりません")
        return

    print(f"読み込み完了: {len(faces)} 枚の顔画像")

    # 平均顔を生成
    avg_face = create_average_face(faces)
    cv2.imwrite(output_path, avg_face)

    print(f"✓ 平均顔の保存完了: {output_path}")

if __name__ == "__main__":
    main()
