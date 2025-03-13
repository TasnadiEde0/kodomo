import os
import uuid

from PIL import Image
from torchvision import transforms

input_folder = "static/training_data/original/bad_images"
output_folder = "static/training_data/augmented/bad_images"

os.makedirs(output_folder, exist_ok=True)

horizontal_flip = transforms.RandomHorizontalFlip(p=1.0)
vertical_flip = transforms.RandomVerticalFlip(p=1.0)
rotation = transforms.RandomRotation(degrees=45)

"""
    Augments pictures to multiply the number of training images
"""
num = 0
for img_name in os.listdir(input_folder):
    if img_name.endswith((".jpg", ".png", ".jpeg")):
        img_path = os.path.join(input_folder, img_name)
        img = Image.open(img_path)

        print(num)
        num += 1

        for i in [0, 1]:
            for j in [0, 1]:
                for k in [0, 45, 90, 135]:
                    filename = f"{output_folder}/{uuid.uuid4()}.jpg"

                    new_img = img.copy()
                    new_img.rotate(k)
                    augmentation_transforms = transforms.Compose([
                        transforms.RandomHorizontalFlip(p=i),
                        transforms.RandomVerticalFlip(p=j)
                    ])
                    new_img = augmentation_transforms(img)

                    new_img.save(filename)
