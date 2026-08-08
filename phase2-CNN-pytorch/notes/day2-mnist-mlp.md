# Phase 2 · Day 2 学习笔记 —— nn.Module + 训练三件套（MNIST 完整训练循环）

> 今天把 Day 1 手搓的「流水线雏形」升级成 PyTorch 标准写法,第一次跑通一个完整训练：在 MNIST 上训 MLP 认手写数字,测试准确率 95%+。核心收获不是 MNIST 本身,而是**那套「换零件就能复用」的训练骨架**——以后 CNN、Transformer、Diffusion Policy 复现全用它。

---

## 一、全局：一次训练 = 五个零件拼成的流水线

```
数据 → 模型 → 损失函数 → 优化器 → 训练循环(转起来) → 评估
```

- 模型：一个参数随机、什么都不会的网络
- 损失函数：量「这次答得多离谱」的尺子
- 优化器：根据尺子读数把参数往「更对」拧的调参师傅
- 数据：一批批的题目 + 标准答案（DataLoader 负责切分投喂）
- 训练循环：让「答题→量误差→拧参数」重复上万次
- 评估：拿没见过的题考真实水平

Day 1 我其实已手搓过雏形（y_pred 是模型、MSE 是尺子、`w-=lr*grad` 是优化器、for 是循环）。今天只是把每个零件换成能拼大网络的**标准工业件**。

---

## 二、核心概念

**nn.Module**：所有模型的基类,继承它就白拿了 `.parameters()`（收集全部参数）、autograd 自动求导、`.to(device)`、`model(x)` 自动触发 forward 等一整套能力。

**搭模型三件套**：`__init__` 里建层（`self.` 存成属性）→ `super().__init__()` 必写第一行 → `forward` 定义数据怎么流。

**训练三件套**：
- 损失函数 `CrossEntropyLoss`：分类专用；内部含 softmax,喂**原始 logits** + **整数标签**。
- 优化器 `optimizer`：`step()` ＝ 更新参数,`zero_grad()` ＝ 清零；靠 `model.parameters()` 知道管谁。
- 数据 `DataLoader`：把数据集切成 mini-batch 传送带；`batch_size` 每批多少,`shuffle` 是否打乱。

**标准训练循环（背下来）**：
```
前向 → 算 loss → zero_grad → backward → step
```
顺序铁律：清零必须在求梯度之前。

**mini-batch 与 epoch**：6万张 ÷ 64 ≈ 938 个 batch,每 batch 走一次五步循环,所以一个 epoch 参数被更新约 938 次。

---

## 三、GPU 用法（我的机器：RTX 5060 8GB，已配好）

标准三步,记死：
```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MLP().to(device)          # 模型搬上去
images = images.to(device)        # 数据也搬上去（训练循环里）
labels = labels.to(device)
```
铁律：**模型和数据必须在同一 device**,否则报 `Expected all tensors to be on the same device`。

顺带养成写 `model.train()` / `model.eval()` 的习惯（现在没 Dropout/BN 加不加一样,但以后有了忘写会出玄学 bug）。

---

## 四、易错点

- `self.` 去掉 → `fc1` 变局部变量,`__init__` 一结束就没了,`forward` 里 `self.fc1` 报 `AttributeError`。`self.` 是「存进对象、跨方法共享」的开关。
- 忘 `super().__init__()` → 参数没被登记,`.parameters()` 收不到,网络训不动。
- 用 `model.forward(x)` 而非 `model(x)` → 跳过 nn.Module 的包装机制,可能出问题。一律 `model(x)`。
- 忘展平 `images.view(...)` → 二维图喂进 `nn.Linear` 形状报错。
- `zero_grad()` 挪到 `backward()` 后 → 刚算的梯度被清成 0,参数纹丝不动。
- **训练时加了 `no_grad()`** → `backward()` 没梯度可算,网络完全学不动。训练不能关梯度,评估才关。
- `forward` 里自己加 softmax + 用 CrossEntropyLoss → softmax 两次,概率被压平,越学越差。喂原始 logits。
- 数据和模型不在同一 device → 报 device 不匹配。

---

## 五、重点思考题（艾宾浩斯自测用，遮答案先自己讲）

**Q. 训练循环里把 `optimizer.zero_grad()` 挪到 `loss.backward()` 后面会怎样？**
> 网络原地不动。顺序变成「算新梯度→立刻清零→更新」,刚算的梯度被清成 0,step() 拿全 0 梯度更新,参数不变。清零必须在求梯度前。

**Q. 训练时能不能用 `with torch.no_grad()`？为什么评估要用？**
> 训练绝不能用——它关掉梯度追踪,而训练靠 backward() 求梯度,加了就学不动。评估该用,因为评估只前向看结果、不求梯度,关掉省显存又加速。「需要梯度的地方不关,不需要的地方(评估/推理)就关」。

**Q. 为什么喂给 CrossEntropyLoss 的必须是原始 logits，不能自己先加 softmax？**
> CrossEntropyLoss 内部已含 softmax。自己再加一层 = softmax 两次,第二次对已是概率的东西再压一遍,把拉开的概率压平,自信度被抹掉,梯度变弱,学得又慢又差。

**Q. optimizer 怎么知道要更新哪些参数？**
> 创建时传了 `model.parameters()`,等于把全网络参数名册交给了它。step() 就照这份名册更新。

---

## 六、我的心得

- 1.新概念：logits原始数据，网络直接输出
- 2.softmax函数：输入logits,输出总和为1的概率
- 3.标准循环五步代码记下来