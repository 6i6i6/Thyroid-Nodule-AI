import os
import csv
import xml.etree.ElementTree as ET

# ==========================
# عدل هذا المسار فقط
# ==========================

DDTI_FOLDER = r"C:\Users\ghre3\Music\datasets\DDTI"

OUTPUT_CSV = "classification_dataset.csv"

rows = []

for file in os.listdir(DDTI_FOLDER):

    if not file.endswith(".xml"):
        continue

    xml_path = os.path.join(DDTI_FOLDER, file)

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        composition = root.findtext("composition", default="")
        echogenicity = root.findtext("echogenicity", default="")
        margins = root.findtext("margins", default="")
        calcifications = root.findtext("calcifications", default="")
        tirads = root.findtext("tirads", default="")

        number = os.path.splitext(file)[0]

        for img in os.listdir(DDTI_FOLDER):

            if img.startswith(number + "_") and img.endswith(".jpg"):

                rows.append([
                    img,
                    composition,
                    echogenicity,
                    margins,
                    calcifications,
                    tirads
                ])

    except Exception as e:
        print("Error:", file, e)

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "image",
        "composition",
        "echogenicity",
        "margins",
        "calcifications",
        "tirads"
    ])

    writer.writerows(rows)

print("=" * 40)
print("Done!")
print("Images:", len(rows))
print("Saved as:", OUTPUT_CSV)
print("=" * 40)