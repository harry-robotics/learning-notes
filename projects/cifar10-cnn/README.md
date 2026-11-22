# CIFAR-10 图像分类（LeNet 风格 CNN）

## 项目简介
用一个 LeNet 风格的 CNN 在 CIFAR-10（10 类彩色物体）上做图像分类。
这是我学习 CNN 后，把 MNIST 上的网络迁移到彩色真实图像的练习项目。

## 环境
- PyTorch 2.13, CUDA 13, RTX 5060 Laptop
- 数据集：CIFAR-10。训练脚本从当前目录下的 `data/` 读取已下载的数据。

## 网络结构
输入 3×32×32 → Conv(3→6) → Pool → Conv(6→16) → Pool → FC(400→120→84→10)

## 结果
- 训练 10 epoch，测试准确率 52.92%
- 当时记录的训练 loss 从 2.30 降到 1.31。增加训练轮数是否会提高测试准确率，还需要单独比较。
- 观察：相比 MNIST（98%），CIFAR-10 明显更难（彩色、真实物体、位置多变）
- 改进方向：更多 epoch、数据增强、加深网络、BatchNorm

## 如何运行
在本项目目录打开终端。如果还没有数据，先运行第一条命令下载，再运行训练脚本：

```bash
python -c "from torchvision.datasets import CIFAR10; CIFAR10('./data', train=True, download=True)"
python train.py
```

## 下一步改进方向
- 加更多卷积层 / BatchNorm
- 数据增强（随机翻转、裁剪）
