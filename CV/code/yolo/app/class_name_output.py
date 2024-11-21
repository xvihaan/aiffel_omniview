import os
import xml.etree.ElementTree as ET
import json

# 경로 설정
xml_folder = "/Users/minhyeok/Desktop/PROJECT/SENSEU/dataset"
labels_folder = "/Users/minhyeok/Desktop/PROJECT/SENSEU/dataset/labels"
yaml_file_path = "/Users/minhyeok/Desktop/PROJECT/SENSEU/data.yaml"

# 클래스 이름과 ID 매핑
class_name_to_id = {}
class_id_to_name = []
class_counter = 0

def extract_class_names(xml_folder):
    """XML 파일에서 클래스 이름 추출 및 매핑"""
    global class_counter

    for folder_name in ["train", "val"]:
        folder_path = os.path.join(xml_folder, folder_name)

        for label_folder in os.listdir(folder_path):
            label_path = os.path.join(folder_path, label_folder)

            # 디렉토리인지 검사하고 숨김 파일 무시
            if not os.path.isdir(label_path) or label_folder.startswith('.'):
                continue

            # XML 파일 탐색
            for xml_file in os.listdir(label_path):
                xml_path = os.path.join(label_path, xml_file)

                if xml_file.endswith(".xml"):
                    tree = ET.parse(xml_path)
                    root = tree.getroot()

                    for obj in root.findall(".//object"):
                        class_name = obj.find("name").text.strip()

                        if class_name not in class_name_to_id:
                            class_name_to_id[class_name] = class_counter
                            class_id_to_name.append(class_name)
                            class_counter += 1

    print(f"총 {class_counter}개의 클래스가 추출되었습니다.")

def update_txt_files(labels_folder):
    """.txt 파일의 클래스 ID 업데이트"""
    for split in ["train", "val"]:
        split_folder = os.path.join(labels_folder, split)

        for txt_file in os.listdir(split_folder):
            if txt_file.endswith(".txt"):
                txt_path = os.path.join(split_folder, txt_file)

                with open(txt_path, "r") as f:
                    lines = f.readlines()

                updated_lines = []
                for line in lines:
                    elements = line.strip().split()
                    old_class_id = int(elements[0])

                    # 새로운 클래스 ID 매핑
                    class_name = class_id_to_name[old_class_id]
                    new_class_id = class_name_to_id[class_name]
                    elements[0] = str(new_class_id)
                    updated_lines.append(" ".join(elements))

                # 업데이트된 내용을 다시 저장
                with open(txt_path, "w") as f:
                    f.write("\n".join(updated_lines))

                print(f"업데이트 완료: {txt_path}")

def create_yaml_file():
    """data.yaml 파일 생성"""
    num_classes = len(class_id_to_name)

    yaml_content = f"""
path: /Users/minhyeok/Desktop/PROJECT/SENSEU
train: images/train
val: images/val

nc: {num_classes}
names: {json.dumps(class_id_to_name)}
"""

    with open(yaml_file_path, "w") as f:
        f.write(yaml_content)

    print(f"`data.yaml` 파일이 생성되었습니다: {yaml_file_path}")

if __name__ == "__main__":
    # 클래스 이름 추출
    extract_class_names(xml_folder)

    # .txt 파일 업데이트
    update_txt_files(labels_folder)

    # data.yaml 파일 생성
    create_yaml_file()