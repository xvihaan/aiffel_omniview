import os

# 경로 설정
labels_folder = "/Users/minhyeok/Desktop/PROJECT/SENSEU/dataset/labels/train"
yaml_file_path = "/Users/minhyeok/Desktop/PROJECT/SENSEU/data.yaml"

# 변환된 폴더 이름(클래스 이름) 가져오기
class_names = sorted([folder for folder in os.listdir(labels_folder) if os.path.isdir(os.path.join(labels_folder, folder))])

# `data.yaml` 파일 생성
num_classes = len(class_names)

yaml_content = f"""
path: /Users/minhyeok/Desktop/PROJECT/SENSEU
train: images/train
val: images/val

nc: {num_classes}
names: {class_names}
"""

# `data.yaml` 파일 저장
with open(yaml_file_path, "w") as f:
    f.write(yaml_content)

print(f"`data.yaml` 파일이 생성되었습니다: {yaml_file_path}")