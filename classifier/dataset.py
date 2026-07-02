import os
import pandas as pd
from PIL import Image

import torch
from torch.utils.data import Dataset
from torchvision import transforms


class ThyroidDataset(Dataset):
    def __init__(self, csv_file, image_folder):

        self.data = pd.read_csv(csv_file)
        self.image_folder = image_folder

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])

        # تحويل النصوص إلى أرقام
        self.composition_map = {
            v: i for i, v in enumerate(sorted(self.data["composition"].unique()))
        }

        self.echogenicity_map = {
            v: i for i, v in enumerate(sorted(self.data["echogenicity"].unique()))
        }

        self.margins_map = {
            v: i for i, v in enumerate(sorted(self.data["margins"].unique()))
        }

        self.calcifications_map = {
            v: i for i, v in enumerate(sorted(self.data["calcifications"].unique()))
        }

        self.tirads_map = {
            v: i for i, v in enumerate(sorted(self.data["tirads"].unique()))
        }

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        row = self.data.iloc[idx]

        image_path = os.path.join(self.image_folder, row["image"])

        image = Image.open(image_path).convert("RGB")
        image = self.transform(image)

        labels = {
            "composition": self.composition_map[row["composition"]],
            "echogenicity": self.echogenicity_map[row["echogenicity"]],
            "margins": self.margins_map[row["margins"]],
            "calcifications": self.calcifications_map[row["calcifications"]],
            "tirads": self.tirads_map[row["tirads"]],
        }

        return image, labels