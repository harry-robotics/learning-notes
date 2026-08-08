# Phase 2 · Day 1 学习笔记 —— PyTorch 基础:Tensor 与 autograd

> 今天正式从「手写 NumPy 神经网络」过渡到 PyTorch。一句话收获:**我只负责写前向计算,梯度让 autograd 自动算**——这是 PyTorch 相比 Phase 1 手推梯度最大的解放。
> (复习进度见单独维护的 review-tracker;术语见单独维护的 glossary。)

---

## 一、核心概念梳理

**Tensor(张量)** = 会自动求导、还能上 GPU 的 NumPy 数组。用法几乎和 `ndarray` 一样,但多了两个本事:① 能在 GPU 上并行运算;② 能自动求导(autograd)。

**autograd 三件套(今天的主线)**:
1. `requires_grad=True` —— 给张量贴「追踪梯度」标签,之后凡用到它的运算都被记进**计算图(computation graph)**。负责「记账」。
2. `loss.backward()` —— 从 loss 沿计算图反向,自动算出对每个参数的梯度。负责「结账」。
3. `.grad` —— 求导结果存这里,拿它来更新参数。是「账单」。

直觉链条:**前向算出 loss → `backward()` 自动求梯度 → 读 `.grad` 做梯度下降**。这条线以后每个训练循环都在重复。

**两个必须配套的动作**:
- 每轮更新完要 `grad.zero_()` 清零(梯度默认**累加**,不清零会滚雪球)。
- 更新参数那步要包在 `with torch.no_grad():` 里(那只是调参,不该记进计算图)。

**关于 device**:`device` 只是个「地址标签」,告诉 PyTorch 东西放 CPU 还是 GPU。我现在 `cuda.is_available()` 是 False,用 CPU,学习阶段完全够。

---

## 二、关键代码

**autograd 最小例子**——体会「记账→结账→读账单」:

```python
import torch

x = torch.tensor(3.0, requires_grad=True)  # 贴追踪标签(必须浮点)
y = x ** 2                                  # 计算图记下 y=x²
y.backward()                                # 反向自动求导
print(x.grad)                               # dy/dx = 2x = 6
```

**用 autograd 复现线性回归梯度下降**——把 Phase 1 手推的梯度公式整段换成一行 `backward()`:

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0, 4.0])       # 真实规律 y = 2x + 1
y = torch.tensor([3.0, 5.0, 7.0, 9.0])

w = torch.tensor(0.0, requires_grad=True)     # 待学参数
b = torch.tensor(0.0, requires_grad=True)
lr = 0.01

for epoch in range(100):
    y_pred = w * x + b                        # 前向
    loss = ((y_pred - y) ** 2).mean()         # MSE,.mean() 压成标量才能 backward

    loss.backward()                           # 自动求梯度(替代手推公式)

    with torch.no_grad():                     # 更新参数不记账
        w -= lr * w.grad
        b -= lr * b.grad

    w.grad.zero_()                            # 清零,防累加
    b.grad.zero_()

    if epoch % 20 == 0:
        print(f"epoch {epoch}: loss={loss.item():.4f}, w={w.item():.3f}, b={b.item():.3f}")
```

跑出来 loss 一路下降、`w→2`、`b→1`。若 loss 变 nan,多半是 `lr` 太大,调小。

---

## 三、易错点(踩过 / 反复确认过的)

- **梯度不清零 → 训练飞掉**。删掉 `grad.zero_()`,梯度会一轮轮**累加**(PyTorch 故意的),等效步长爆炸,loss 震荡甚至变 nan,收敛不到正确值。每轮必清零。
- **更新参数忘包 `no_grad()` → 报错**。`w -= lr*w.grad` 是对需梯度的叶子张量做原地修改,不包 `no_grad()` 会报 `a leaf Variable that requires grad is being used in an in-place operation`,还会让计算图越滚越大吃内存。
- **对非标量 `backward()` → 报错**。`backward()` 只能从标量出发。loss 是 4 元素向量时直接 `backward()` 会报 `grad can be implicitly created only for scalar outputs`,所以要先 `.mean()`(或 `.sum()`)压成一个数。
- **`from_numpy` 共享内存 → 隐蔽 bug**。`torch.from_numpy(arr)` 和 `.numpy()` 转出的两者共享同一块内存,改 `arr` 会连带改 Tensor(反之亦然)。想要独立副本用 `torch.tensor(arr)`(会拷贝)或 `.clone()`。
- **需求导的张量必须浮点**。`torch.tensor(3, requires_grad=True)` 报错,要写 `3.0`。
- **`@` 是矩阵乘、`*` 是逐元素乘**,别混。
- **`python -m pip` 装库**能保证装进当前 python 环境,避免「装了却 import 不到」。

---

## 四、重点思考题(艾宾浩斯自测用,遮答案先自己讲)

**Q. 删掉 `grad.zero_()` 会怎样?为什么?**
> 梯度会累加(每次 backward 是加不是覆盖),越滚越大,等效步长爆炸 → loss 震荡/变 nan,收敛不了。PyTorch 故意让梯度累加,清零得自己做。

**Q. 为什么线性回归里要先 `.mean()` 才能 `backward()`?**
> `backward()` 只能从标量出发(标量对参数的导数唯一)。向量输出会变成雅可比、不唯一,PyTorch 不知怎么加权,直接调用会报错。`.mean()` 把多个误差压成一个平均损失标量,梯度就唯一了。

**Q. `from_numpy` 转出的 Tensor 改了 numpy 会不会变?埋什么坑?**
> 会变,两者共享内存。坑:本想只改 numpy,结果 Tensor 数据被偷偷改了,极难排查。要独立副本用 `torch.tensor()` 或 `.clone()`。

---

