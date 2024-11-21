import os
import shutil

# 이미지 경로 설정
base_img_train_path = "/Users/minhyeok/Desktop/PROJECT/SENSEU/images/img_train"
base_img_val_path = "/Users/minhyeok/Desktop/PROJECT/SENSEU/images/img_val"

def move_images_to_root(base_path):
    """하위 폴더의 이미지를 최상위 폴더로 이동"""
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".jpg"):
                    src_path = os.path.join(folder_path, file)
                    dst_path = os.path.join(base_path, file)
                    try:
                        shutil.move(src_path, dst_path)
                        print(f"Moved: {src_path} -> {dst_path}")
                    except Exception as e:
                        print(f"Error moving {src_path}: {e}")

    # 하위 폴더 삭제
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            print(f"Removed folder: {folder_path}")

if __name__ == "__main__":
    move_images_to_root(base_img_train_path)
    move_images_to_root(base_img_val_path)