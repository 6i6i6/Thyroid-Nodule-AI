import os
import shutil
import pandas as pd

CSV_FILE = "classification_dataset_clean.csv"

SOURCE_FOLDER = r"C:\Users\ghre3\Desktop\Thyroid-Nodule-AI\cropped_nodules"

DEST_FOLDER = r"C:\Users\ghre3\Desktop\Thyroid-Nodule-AI\classifier_dataset"

os.makedirs(DEST_FOLDER, exist_ok=True)

df = pd.read_csv(CSV_FILE)

copied = 0
missing = 0

for image_name in df["image"]:

    src = os.path.join(SOURCE_FOLDER, image_name)
    dst = os.path.join(DEST_FOLDER, image_name)

    if os.path.exists(src):
        shutil.copy(src, dst)
        copied += 1
    else:
        print("Missing:", image_name)
        missing += 1

print("=" * 40)
print("Copied :", copied)
print("Missing:", missing)
print("=" * 40)