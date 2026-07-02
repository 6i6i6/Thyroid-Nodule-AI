from pathlib import Path
import xml.etree.ElementTree as ET
import random
import shutil

random.seed(42)

ROOT = Path("datasets/TN5000")

# إذا عندك أسماء مختلفة عدلها فقط هنا
IMAGE_DIR = ROOT / "JPEGImages"
XML_DIR = ROOT / "Annotations"

# إذا الصور ليست داخل JPEGImages ابحث عنها تلقائياً
if not IMAGE_DIR.exists():
    jpgs = list(ROOT.rglob("*.jpg"))
    if jpgs:
        IMAGE_DIR = jpgs[0].parent

OUTPUT = Path("yolo_dataset")

for folder in [
    "images/train",
    "images/val",
    "images/test",
    "labels/train",
    "labels/val",
    "labels/test",
]:
    (OUTPUT / folder).mkdir(parents=True, exist_ok=True)

xml_files = sorted(XML_DIR.glob("*.xml"))

random.shuffle(xml_files)

n = len(xml_files)

train = xml_files[: int(n * 0.8)]
val = xml_files[int(n * 0.8): int(n * 0.9)]
test = xml_files[int(n * 0.9):]

splits = {
    "train": train,
    "val": val,
    "test": test,
}


def convert(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    w = int(root.find("size/width").text)
    h = int(root.find("size/height").text)

    labels = []

    for obj in root.findall("object"):

        xmin = float(obj.find("bndbox/xmin").text)
        ymin = float(obj.find("bndbox/ymin").text)
        xmax = float(obj.find("bndbox/xmax").text)
        ymax = float(obj.find("bndbox/ymax").text)

        xc = ((xmin + xmax) / 2) / w
        yc = ((ymin + ymax) / 2) / h

        bw = (xmax - xmin) / w
        bh = (ymax - ymin) / h

        labels.append(f"0 {xc} {yc} {bw} {bh}")

    return labels


for split, files in splits.items():

    for xml in files:

        image = IMAGE_DIR / (xml.stem + ".jpg")

        if not image.exists():
            continue

        shutil.copy(image, OUTPUT / "images" / split / image.name)

        labels = convert(xml)

        with open(
            OUTPUT / "labels" / split / f"{xml.stem}.txt",
            "w",
        ) as f:
            f.write("\n".join(labels))

print("Dataset prepared successfully.")