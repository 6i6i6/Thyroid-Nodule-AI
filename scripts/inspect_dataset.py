from pathlib import Path

DATASET_ROOT = Path("datasets")

print("=" * 60)

for dataset in DATASET_ROOT.iterdir():
    if not dataset.is_dir():
        continue

    print(f"\n📁 {dataset.name}")

    counts = {}

    for file in dataset.rglob("*"):
        if file.is_file():
            ext = file.suffix.lower()
            counts[ext] = counts.get(ext, 0) + 1

    total = sum(counts.values())
    print(f"Total files: {total}")

    for ext, num in sorted(counts.items()):
        print(f"{ext:<8} {num}")