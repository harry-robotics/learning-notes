import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# 预处理：转张量 + 标准化
transform = transforms.Compose([
    transforms.ToTensor(),                          # 转张量，像素缩到 0~1
    transforms.Normalize((0.5, 0.5, 0.5),           # 3 个通道各自的均值
                         (0.5, 0.5, 0.5))            # 3 个通道各自的标准差
])

train_data = torchvision.datasets.CIFAR10(root='./data', train=True,  download=False, transform=transform)
test_data  = torchvision.datasets.CIFAR10(root='./data', train=False, download=False, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader  = DataLoader(test_data,  batch_size=64, shuffle=False)

classes = ('plane','car','bird','cat','deer','dog','frog','horse','ship','truck')

import torch.nn as nn

class CIFARNet(nn.Module):
    def __init__(self):
        super().__init__()
        # 改动1：in_channels 从 1 → 3（彩色）
        self.conv1 = nn.Conv2d(3, 6, kernel_size=5)      # 3→6 通道
        self.pool  = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)     # 6→16 通道
        self.relu  = nn.ReLU()
        # 改动2：fc1 输入维度重算（见下方形状追踪）
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # x: [batch, 3, 32, 32]
        x = self.pool(self.relu(self.conv1(x)))   # → [b,6,14,14]
        x = self.pool(self.relu(self.conv2(x)))   # → [b,16,5,5]
        x = x.view(x.size(0), -1)                 # 展平 → [b,400]
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CIFARNet().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)  # 加了 momentum，收敛更好

for epoch in range(10):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch+1}, avg_loss={running_loss/len(train_loader):.4f}")

# 评估
model.eval()
correct = total = 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print(f"Test Accuracy: {100*correct/total:.2f}%")