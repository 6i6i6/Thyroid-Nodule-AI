import os
import json
import xml.etree.ElementTree as ET
from PIL import Image

# ==========================
# عدل هذا المسار
# ==========================

DDTI_FOLDER = r"C:\Users\ghre3\Music\datasets\DDTI"

OUTPUT_FOLDER = r"C:\Users\ghre3\Desktop\Thyroid-Nodule-AI\cropped_nodules"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

MARGIN = 15


def clamp(v, low, high):
    return max(low, min(v, high))


processed = 0
skipped = 0

for file in os.listdir(DDTI_FOLDER):

    if not file.endswith(".xml"):
        continue

    xml_path = os.path.join(DDTI_FOLDER, file)

    try:

        tree = ET.parse(xml_path)
        root = tree.getroot()

        case_number = root.find("number").text

        marks = root.findall(".//mark")

        for mark in marks:

            image_id = mark.find("image").text

            svg_node = mark.find("svg")

            if svg_node is None:
                continue

            if svg_node.text is None:
                continue

            regions = json.loads(svg_node.text)

            image_name = f"{case_number}_{image_id}.jpg"

            image_path = os.path.join(DDTI_FOLDER, image_name)

            if not os.path.exists(image_path):
                skipped += 1
                continue

            image = Image.open(image_path)

            width, height = image.size

            xs = []
            ys = []

            for region in regions:

                if "points" not in region:
                    continue

                for p in region["points"]:

                    xs.append(p["x"])
                    ys.append(p["y"])

            if len(xs) == 0:
                skipped += 1
                continue

            xmin = clamp(min(xs) - MARGIN, 0, width)
            ymin = clamp(min(ys) - MARGIN, 0, height)

            xmax = clamp(max(xs) + MARGIN, 0, width)
            ymax = clamp(max(ys) + MARGIN, 0, height)

            crop = image.crop((xmin, ymin, xmax, ymax))

            crop.save(os.path.join(OUTPUT_FOLDER, image_name))

            processed += 1

    except Exception as e:

        print(file, "->", e)

print("=" * 50)
print("Finished")
print("Processed :", processed)
print("Skipped   :", skipped)
print("Saved to  :", OUTPUT_FOLDER)
print("=" * 50)