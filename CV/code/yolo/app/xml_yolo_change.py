import os
import xml.etree.ElementTree as ET

# 경로 설정
base_folder = "/Users/minhyeok/Desktop/PROJECT/SENSEU/dataset"
train_xml_folder = "/Users/minhyeok/Desktop/PROJECT/SENSEU/dataset/labels/train"
val_xml_folder = "/Users/minhyeok/Desktop/PROJECT/SENSEU/dataset/labels/val"
output_folder = "/Users/minhyeok/Desktop/PROJECT/SENSEU/dataset/labels"

# 클래스 이름과 ID 동적 할당
class_name_to_id = {}
class_counter = 0

def get_class_id(class_name):
    global class_counter
    if class_name not in class_name_to_id:
        class_name_to_id[class_name] = class_counter
        class_counter += 1
    return class_name_to_id[class_name]

def convert_xml_to_yolo(xml_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for label_folder in os.listdir(xml_folder):
        label_path = os.path.join(xml_folder, label_folder)
        if not os.path.isdir(label_path):
            continue

        for xml_file in os.listdir(label_path):
            if xml_file.endswith(".xml"):
                xml_path = os.path.join(label_path, xml_file)
                tree = ET.parse(xml_path)
                root = tree.getroot()

                # 이미지 파일 이름과 크기 정보 추출
                try:
                    img_name = root.find('.//filename').text
                    img_width = int(root.find('.//size/width').text)
                    img_height = int(root.find('.//size/height').text)
                except AttributeError as e:
                    print(f"XML 파싱 오류: {xml_path}, {e}")
                    continue

                yolo_annotations = []

                for obj in root.findall('.//object'):
                    class_name = obj.find('name').text.strip()
                    class_id = get_class_id(class_name)

                    bbox = obj.find('bndbox')
                    xmin = int(bbox.find('xmin').text)
                    ymin = int(bbox.find('ymin').text)
                    xmax = int(bbox.find('xmax').text)
                    ymax = int(bbox.find('ymax').text)

                    x_center = ((xmin + xmax) / 2) / img_width
                    y_center = ((ymin + ymax) / 2) / img_height
                    bbox_width = (xmax - xmin) / img_width
                    bbox_height = (ymax - ymin) / img_height

                    yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}")

                yolo_file = os.path.join(output_folder, xml_file.replace(".xml", ".txt"))
                with open(yolo_file, "w") as f:
                    f.write("\n".join(yolo_annotations))

                print(f"변환 완료: {yolo_file}")

def process_datasets():
    print("훈련 데이터셋 변환 중...")
    convert_xml_to_yolo(train_xml_folder, os.path.join(output_folder, "train"))
    
    print("검증 데이터셋 변환 중...")
    convert_xml_to_yolo(val_xml_folder, os.path.join(output_folder, "val"))

    with open(os.path.join(output_folder, "classes.txt"), "w") as f:
        for class_name, class_id in sorted(class_name_to_id.items(), key=lambda x: x[1]):
            f.write(f"{class_name}\n")

    print("클래스 목록이 'classes.txt' 파일로 저장되었습니다.")

if __name__ == "__main__":
    process_datasets()