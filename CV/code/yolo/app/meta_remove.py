import os

label_train_path = "/Users/minhyeok/Desktop/PROJECT/SENSEU/yolov7/labels/train/65767_Coa_Biogi_Agricultural_Cleanscom_View_Chabuti"
label_val_path = "/Users/minhyeok/Desktop/PROJECT/SENSEU/yolov7/labels/train/65767_Coa_Biogi_Agricultural_Cleanscom_View_Chabuti"

def rename_label_files(base_path):
    """라벨 파일에서 '_meta' 제거"""
    for file in os.listdir(base_path):
        if file.endswith("_meta.txt"):
            new_name = file.replace("_meta", "")
            src_path = os.path.join(base_path, file)
            dst_path = os.path.join(base_path, new_name)
            try:
                os.rename(src_path, dst_path)
                print(f"Renamed: {src_path} -> {dst_path}")
            except Exception as e:
                print(f"Error renaming {src_path}: {e}")

if __name__ == "__main__":
    rename_label_files(label_train_path)
    rename_label_files(label_val_path)

    