import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

'''
训练固定数据集的代码
'''
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
        )
        self.outlayer = nn.Conv2d(128, 1, kernel_size=5, stride=1, padding=0)

    def forward(self, x):
        x = self.conv1(x)
        x = self.outlayer(x)
        return x
# 假设 X 和 Y 是 numpy 数组
# 生成数据
X = torch.randn(1000, 1, 5, 5)  # 1000条5x5的数据
Y = torch.randn(1000, 1)  # 1000条1x1的标签

dataset = TensorDataset(X, Y)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

model = MyModel()
criterion = nn.MSELoss()  # 或者其他损失函数
optimizer = optim.Adam(model.parameters(), lr=0.001)

model = MyModel()
criterion = nn.MSELoss()  # 或者其他损失函数
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 10

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, targets in dataloader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss / len(dataloader):.4f}')


torch.save(model.state_dict(), 'Model.pkl')


