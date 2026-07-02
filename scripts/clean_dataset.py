import pandas as pd

df = pd.read_csv("classification_dataset.csv")

# حذف الصفوف اللي بيها أي قيمة فارغة
df = df.dropna()

# حذف الصفوف اللي بيها نص فارغ
for col in df.columns:
    df = df[df[col].astype(str).str.strip() != ""]

df.to_csv("classification_dataset_clean.csv", index=False)

print("Done!")
print("Before:", len(pd.read_csv("classification_dataset.csv")))
print("After :", len(df))