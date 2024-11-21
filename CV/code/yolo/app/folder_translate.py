# 한글폴더명을 영어명으로 바꿔주는 스크립트

import os
import shutil
from googletrans import Translator

# 번역기 초기화
translator = Translator()

# img_train 폴더 경로
img_train_path = "/Users/minhyeok/Desktop/PROJECT/SENSEU/dataset/labels/train"

def translate_folder_name(folder_name):
    """한글 폴더명을 영어로 번역"""
    try:
        # 폴더명 번역
        translated = translator.translate(folder_name, src='ko', dest='en').text
        # 공백 및 특수문자 제거
        translated = translated.replace(" ", "_").replace("-", "_")
        return translated
    except Exception as e:
        print(f"번역 실패: {folder_name}, 오류: {e}")
        return folder_name  # 번역 실패 시 원래 이름 반환

def rename_folders(base_path):
    """한글 폴더명을 영문으로 변경"""
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            # 번역된 폴더명 생성
            new_folder_name = translate_folder_name(folder_name)
            new_folder_path = os.path.join(base_path, new_folder_name)

            # 폴더명 변경
            if folder_path != new_folder_path:
                try:
                    shutil.move(folder_path, new_folder_path)
                    print(f"폴더명 변경: {folder_name} -> {new_folder_name}")
                except Exception as e:
                    print(f"폴더명 변경 실패: {folder_name}, 오류: {e}")

if __name__ == "__main__":
    rename_folders(img_train_path)