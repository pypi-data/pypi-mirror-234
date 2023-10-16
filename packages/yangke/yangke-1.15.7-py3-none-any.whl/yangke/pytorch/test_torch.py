from yangke.pytorch.mytorch import DataFitterNet, train_model
import torch
from yangke.common.config import logger

# DataFitterNet.train()
# train_model()
# x_data = [1, 2, 3]
# y_data = [2, 4, 6]
# w = torch.tensor([1])
# w.requires_grad = True
x = torch.tensor([2.0], requires_grad=True)  # 负荷、温度、湿度
w = torch.tensor([5.0], requires_grad=True)
b = torch.tensor([0.5], requires_grad=True)
print("x = ", x)
print("x.requires_grad = ", x.requires_grad)
y = w * x + b
print("y = ", y)
print("y.requires_grad = ", y.grad_fn)

y.backward()  # 反向传播,求解导数，即y对x求导
print("x.grad = ", x.grad)
loss = (y - y_) ** 2 - x.grad * 0.5
