import torch, json
import torchvision.transforms as transforms
from torchvision.models import resnet18
from torch.utils.data import Dataset, DataLoader
from PIL import Image

class SkinDataset(Dataset):
    def __init__(self, annotations, transform=None):
        self.annotations = list(annotations.items())
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        img_path, label = self.annotations[idx]
        image = Image.open(img_path)
        if self.transform:
            image = self.transform(image)
        label = 0 if label == 'sèche' else (1 if label == 'normale' else 2)
        return image, label

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

ANNOTATION_FILE = 'annotations.json'

with open(ANNOTATION_FILE, 'r') as f:
    annotations = json.load(f)


dataset = SkinDataset(annotations, transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

dataset = SkinDataset(annotations, transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)


model = resnet18(pretrained=True)
model.fc = torch.nn.Linear(model.fc.in_features, 3)  

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10): 
    for images, labels in dataloader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    print(f"Epoch [{epoch+1}/10], Loss: {loss.item():.4f}")