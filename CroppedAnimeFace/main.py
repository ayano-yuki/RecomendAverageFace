#!/usr/bin/env python3
"""
アニメ顔切り抜きスクリプト

機能:
- アニメ画像から顔を検出して切り抜き、指定サイズにリサイズして保存する
"""

import os
import sys
import glob
from typing import List
import cv2
from tqdm import tqdm

# 相対インポートのためのパス設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from anime_face_detector import AnimeFaceDetector

def main():
    """顔の検出と切り抜き処理"""
    print("=" * 50)
    print("アニメ顔切り抜きツール")
    print("=" * 50)

    # 設定
    input_dir = "input"
    output_dir = "output"
    target_size = (128, 128)  # 出力画像のサイズ

    # 入力ディレクトリ存在確認
    if not os.path.exists(input_dir):
        print(f"エラー: 入力ディレクトリが見つかりません: {input_dir}")
        return

    # 出力ディレクトリ作成
    os.makedirs(output_dir, exist_ok=True)

    # 入力画像の取得
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_dir, ext)))
        image_files.extend(glob.glob(os.path.join(input_dir, ext.upper())))

    if not image_files:
        print(f"エラー: {input_dir} に画像ファイルが存在しません")
        return

    print(f"処理対象画像数: {len(image_files)}")

    # アニメ顔検出器の初期化
    try:
        detector = AnimeFaceDetector()
    except Exception as e:
        print(f"エラー: 顔検出器の初期化に失敗しました: {e}")
        return

    face_count = 0

    # 各画像に対して顔を検出・保存
    for image_file in tqdm(image_files, desc="顔を検出中"):
        try:
            faces = detector.process_image(image_file, target_size)
            base_name = os.path.splitext(os.path.basename(image_file))[0]
            for i, face in enumerate(faces):
                filename = f"{base_name}_face_{i:03d}.jpg"
                save_path = os.path.join(output_dir, filename)
                cv2.imwrite(save_path, face)
                face_count += 1
        except Exception as e:
            print(f"警告: {image_file} の処理中にエラー: {e}")
            continue

    print("\n" + "=" * 50)
    print("顔の切り抜き処理完了！")
    print(f"検出された顔数: {face_count}")
    print(f"出力ディレクトリ: {output_dir}")

if __name__ == "__main__":
    main()
