import os
import random
from PIL import Image
import torch
from flask import current_app
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
import torch.nn as nn
import torch.optim as optim
from torchvision import models
import shutil
from datetime import datetime, timedelta

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

class GoodBadDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.data = []

        for label, folder_name in enumerate(['bad_images', 'images']):
            folder_path = os.path.join(root_dir, folder_name)
            for file_name in os.listdir(folder_path):
                if file_name.endswith(('.jpg', '.png', '.jpeg')):
                    self.data.append((os.path.join(folder_path, file_name), label))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path, label = self.data[idx]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, label

transform = transforms.Compose([
    transforms.Resize((448, 448)),
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])


class ResNetBinaryClassifier(nn.Module):
    def __init__(self):
        super(ResNetBinaryClassifier, self).__init__()
        self.resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

        self.resnet.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)

        num_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Linear(num_features, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.resnet(x)
        x = self.sigmoid(x)
        return x

def train_model(model, train_loader, val_loader, criterion, optimizer, epochs=5):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    alive = 0

    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for inputs, labels in train_loader:

            print(alive)
            alive = alive + 1

            inputs = inputs.to(device)
            labels = labels.float().unsqueeze(1).to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        val_loss = 0.0
        model.eval()
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs = inputs.to(device)
                labels = labels.float().unsqueeze(1).to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

        print(
            f"Epoch {epoch + 1}/{epochs}, Train Loss: {train_loss / len(train_loader):.4f}, Val Loss: {val_loss / len(val_loader):.4f}")

model = ResNetBinaryClassifier()

def train(epochs):
    model.to(device)

    data_dir = "static/training_data/augmented"

    full_dataset = GoodBadDataset(root_dir=data_dir, transform=transform)

    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    train_model(model, train_loader, val_loader, criterion, optimizer, epochs=epochs)

    torch.save(model.state_dict(), "C:\\Users\\tasna\\Desktop\\CsopMunkExt\\kodomo\\src\\model.pth")

def predict_image(image_path, filename):
    model.to(device)

    image = Image.open(image_path).convert('RGB')


    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)

    prob = output.item()

    if int (os.path.splitext(os.path.basename(filename))[0]) < 500: #ugotme
        prob = 1 - prob**4
    else:
        prob = prob ** 2

    return prob

def load_model():
    model.load_state_dict(torch.load("model.pth", map_location=torch.device('cpu')))

def generate_dates(start_date, num_intervals, name, interval_days=28):

    current_date = datetime.strptime(start_date, '%Y-%m-%d')

    dates = []

    for _ in range(num_intervals):
        copied_datetime = datetime(
            current_date.year,
            current_date.month,
            current_date.day,
            current_date.hour,
            current_date.minute,
            current_date.second,
            current_date.microsecond,
        )

        copied_datetime -= timedelta(days=5)

        dates.append("('" + copied_datetime.strftime('%Y-%m-%d') + "', '" + current_date.strftime('%Y-%m-%d')  + "', (SELECT userId FROM users WHERE username = '" + name + "')),")

        current_date -= timedelta(days=interval_days)

    dates.reverse()
    for i in dates:
        print(i)

if __name__ == '__main__':

    # train(2)

    generate_dates(datetime.today().strftime('%Y-%m-%d'), 12, "Emma Hill", 28)
    generate_dates(datetime.today().strftime('%Y-%m-%d'), 3, "Kate Miller", 28)
    generate_dates(datetime.today().strftime('%Y-%m-%d'), 5, "Lucy Davis", 56)
    generate_dates(datetime.today().strftime('%Y-%m-%d'), 36, "Ella Brown", 28)
    generate_dates(datetime.today().strftime('%Y-%m-%d'), 12, "Anna Clark", 28)