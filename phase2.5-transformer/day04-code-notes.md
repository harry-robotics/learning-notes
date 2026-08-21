# Day 04 代码补充｜新出现的东西 + 完整流程图

配合 `mini_gpt.py` 和 `vit.py` 阅读。

---

## 掌握程度速查

先看这张表，**只有第一档需要真正弄懂**，后面两档看过就行。

| 内容 | 档位 | 理由 |
|---|---|---|
| `AdamW` 优化器 | **必须懂** | 以后所有训练都用它，不再用 SGD |
| `@torch.no_grad()` + `eval()/train()` | **必须懂** | 每次评估、推理都要用，用错会出隐蔽 bug |
| `view(-1, V)` 摊平算 loss | **必须懂** | 所有序列任务的 loss 都这么算 |
| `nn.Parameter` vs `register_buffer` | **必须懂** | 决定一个张量会不会被训练，搞错模型不收敛 |
| `.to(device)` | **必须懂** | 你已经会了，这里是复习 |
| 采样与 temperature | **必须懂** | 生成类模型的标准操作 |
| `.expand()` vs `.repeat()` | 看一眼 | 知道 expand 不复制内存即可 |
| `.flatten(2)` | 看一眼 | 一句话规则 |
| `torch.cat` / `torch.stack` | 看一眼 | 常用但直白 |
| `torch.randint` 取 batch | 看一眼 | 这个任务特有的写法 |
| `stoi` / `itos` 字典 | 忽略 | 就是普通 Python 字典 |
| `nn.init.trunc_normal_` | 忽略 | 初始化细节，照抄即可 |
| `TEXT * 40` | 忽略 | 字符串重复，纯粹是为了数据量 |

---

# 一、必须懂的六件事

## 1. AdamW：从今往后都用它

**你之前用的是 SGD**，Phase 2 的 MNIST 和 CIFAR-10 都是。**但训练 Transformer 基本不用 SGD**，一律用 Adam 系列。

```python
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
```

### 为什么换

**SGD 对所有参数用同一个学习率。** 但 Transformer 里不同层的梯度大小差别极大——嵌入层、注意力权重、FFN 的梯度可能相差几个数量级。**一个学习率对某些层太大（震荡），对另一些层太小（不动）。**

**Adam 给每个参数维护自己的学习率**：它记录每个参数过去梯度的大小，**梯度一直很大的参数就把步长调小，梯度一直很小的就调大**。

打个比方：SGD 是所有人齐步走同样的步幅；Adam 是每个人根据自己的腿长自动调整步幅。

**AdamW 里的 W 是 weight decay（权重衰减）**——一种防过拟合的手段，让参数不要变得太大。AdamW 修正了原始 Adam 里 weight decay 的实现方式。**你只需要知道：现在的标准选择是 AdamW，不是 Adam，也不是 SGD。**

### 学习率 3e-4

**这是 Transformer 训练的经验默认值**，Karpathy 称之为"Adam 的魔法数字"。你不确定用多少时，从 `3e-4` 开始基本不会错。

对比一下：SGD 的常用学习率是 `0.01` 到 `0.1`，**比 Adam 大两个数量级**。所以换优化器时不能沿用旧的学习率。

> **这条以后会直接用上**：你复现 Diffusion Policy 时，配置文件里的优化器几乎必然是 AdamW。

---

## 2. `@torch.no_grad()` 和 `eval()` / `train()`

```python
@torch.no_grad()
def generate(self, idx, max_new_tokens, temperature=1.0):
    self.eval()
    ...
    self.train()
    return idx
```

这里有两件独立的事，**经常被混为一谈**。

### `@torch.no_grad()`：关掉梯度记录

平时 PyTorch 会为每个运算记录"怎么来的"，以便反向传播。**生成文本时不需要反向传播**，这些记录纯属浪费。

`@torch.no_grad()` 是**装饰器**写法（加在函数上面那一行），效果是整个函数内部都不记录梯度。等价于把函数体全包进 `with torch.no_grad():`。

**好处**：省显存、跑得快。生成 200 个字符时差别很明显。

> 你在 Phase 2 评估 MNIST 时写过 `with torch.no_grad():`，是同一件事，只是换了个更简洁的写法。

### `eval()` / `train()`：切换层的行为

**这是完全不同的另一件事。**

我们的 `TransformerBlock` 里有 **Dropout**（Day 3 第 6 节讲过），它在训练时随机丢弃一部分神经元，推理时**完全不丢**。

`self.eval()` 就是切到"推理行为"，`self.train()` 切回来。

**为什么生成完要切回 `train()`**：因为这个函数可能在训练过程中被调用（比如每 500 步生成一段看看效果）。**如果忘了切回来，后续训练全程 Dropout 都是关闭的**——不会报错，只是模型更容易过拟合，而你完全不知道为什么。

> **规则：`no_grad` 管的是"要不要记梯度"，`eval` 管的是"层的行为模式"。两件事都要做，缺一不可。**

---

## 3. `view(-1, vocab_size)`：为什么算 loss 前要摊平

```python
loss = F.cross_entropy(logits.view(-1, vocab_size), y.view(-1))
```

### 形状问题

- `logits` 是 `(B, L, V)` = `(32, 64, 40)` —— 32 个样本、每个 64 个位置、每个位置 40 个类别的分数
- `y` 是 `(B, L)` = `(32, 64)` —— 每个位置的正确答案

**但 `cross_entropy` 只接受二维输入**：预测是 `(N, C)`，标签是 `(N,)`。

所以要摊平：

```
logits: (32, 64, 40) --view(-1, 40)--> (2048, 40)
y:      (32, 64)     --view(-1)-----> (2048,)
```

`-1` 的含义是**"这一维你自己算"**——PyTorch 会根据总元素数推出 `32 × 64 = 2048`。

### 这在语义上是什么意思

**把"32 个样本 × 64 个位置"看成 2048 个独立的分类任务。** 每个位置都在做同一件事：从 40 个字符里选一个。

**这个"摊平成一堆独立分类"的处理方式，在所有序列任务里都一样。** 你以后算动作序列的 loss 时，做的是同样的操作。

### 顺带：`F.cross_entropy` 和 `nn.CrossEntropyLoss`

**是同一个东西**，函数版和类版的区别，和 `F.relu` vs `nn.ReLU` 完全一样。

- `nn.CrossEntropyLoss()` 要先实例化再调用（适合放进 `__init__`）
- `F.cross_entropy(...)` 直接调用（适合在 `forward` 里临时用）

**都不需要你手动做 softmax，它内部包含了。**

---

## 4. `nn.Parameter` vs `register_buffer` vs 普通属性

这三个决定了"一个张量在模型里的身份"，**搞错会让模型静默地训不动**。

```python
self.cls_token = nn.Parameter(torch.zeros(1, 1, d_model))   # vit.py
self.register_buffer('pe', pe.unsqueeze(0))                  # transformer.py
self.something = torch.zeros(...)                            # 普通属性
```

| 写法 | 会被训练吗 | `.to(device)` 跟着走吗 | 存进 checkpoint 吗 |
|---|---|---|---|
| `nn.Parameter` | ✅ | ✅ | ✅ |
| `register_buffer` | ❌ | ✅ | ✅ |
| 普通属性 | ❌ | ❌ | ❌ |

**怎么选：**

- 这个张量**应该被训练**（如 CLS token、可学习位置编码）→ `nn.Parameter`
- **固定不变但要跟着模型走**（如正弦位置编码表、预计算的 mask）→ `register_buffer`
- 普通属性 → **几乎总是错的**，因为你把模型 `.to('cuda')` 之后它还留在 CPU，运算时报 device 不匹配

### CLS token 为什么是 `nn.Parameter`

它初始化为全 0，**但必须被训练**——训练会让它学会"怎么问出一个好问题"，从而在 attention 中有效汇总全图信息。如果写成 buffer，它永远是全 0，整个 CLS 机制就废了。

**而且这种错误不报错**——模型照常训练，只是分类效果差，你很难查出原因。

> **`nn.Linear`、`nn.Embedding` 内部的权重也都是 `nn.Parameter`**，只是框架帮你建好了。你自己造张量时才需要手动指定。

---

## 5. 采样与 temperature

```python
logits = self(idx_cond)[:, -1, :]              # 只要最后一个位置
probs = F.softmax(logits / temperature, dim=-1)
next_id = torch.multinomial(probs, num_samples=1)
idx = torch.cat([idx, next_id], dim=1)
```

### `[:, -1, :]`：为什么只取最后一个位置

模型对**每个**位置都输出了预测，但生成时我们只关心"下一个字符是什么"——**那就是最后一个位置的预测**。

前面位置的预测在训练时有用（每个位置都是一个训练样本），生成时用不上。

### `torch.multinomial`：按概率抽签，不是取最大

给它一个概率分布 `[0.7, 0.2, 0.1]`，它有 70% 概率返回索引 0、20% 返回 1、10% 返回 2。

**为什么不用 `argmax` 直接取最大的？** 因为那样每一步都选最可能的字符，**生成的文本会陷入重复循环**（"the the the the..."）。采样带来多样性。

### temperature：直接用 Day 1 学的 softmax 性质

```
logits / temperature
```

| temperature | 效果 |
|---|---|
| < 1（如 0.5） | 除以小数 = **放大差距** → softmax 更接近 one-hot → 更保守、更重复 |
| = 1 | 原样 |
| > 1（如 1.5） | **缩小差距** → 分布更平均 → 更随机、更容易出错 |

**这正是 Day 1 那条"输入差距越大，softmax 输出越接近 one-hot"的直接应用。** 你当时做的 `a * 10` 实验就是 temperature = 0.1 的效果。

代码里用 `0.8`，比 1 略保守。

### `idx[:, -self.max_len:]`：为什么要截断

`pos_emb = nn.Embedding(max_len, d_model)` 只有 `max_len` 个位置向量。生成超过这个长度时，**多出来的位置没有对应的位置编码，会索引越界报错。**

所以只保留最后 `max_len` 个 token 作为上下文。**这就是"上下文窗口"的由来**——GPT 的 4k、128k 上下文说的就是这个 `max_len`。

---

## 6. `.to(device)`：复习

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = MiniGPT(...).to(device)
x, y = ds.get_batch(...)   # 内部做了 .to(device)
```

**规则你已经知道**：模型和数据必须在同一个 device 上。

新增一个细节：`torch.arange(L, device=idx.device)`

**在 `forward` 内部创建新张量时，要显式指定 device**，否则它默认在 CPU 上，而 `idx` 在 GPU 上，相加会报错。

**`device=idx.device` 是标准写法**——"跟着输入走"，不用关心当前到底在 CPU 还是 GPU。你以后自己写模型时会经常用到。

---

# 二、看一眼就行的四个

**`.expand(B, -1, -1)`**（vit.py）
把 `(1, 1, 768)` 的 CLS token 复制成 `(B, 1, 768)`，好和 batch 里每个样本拼接。
`-1` = "这一维保持不变"。
**和 `.repeat()` 的区别**：`expand` 只是"假装复制"，不真占内存；`repeat` 真的复制。能用 expand 就用 expand。

**`.flatten(2)`**（vit.py）
从第 2 维开始把后面所有维度压成一维：`(B, 768, 14, 14)` → `(B, 768, 196)`。

**`torch.cat` / `torch.stack`**
- `cat` 在**已有**维度上接起来：`(B,1,D)` + `(B,196,D)` → `(B,197,D)`
- `stack` 创造**新**维度：一堆 `(64,)` → `(32, 64)`

**`torch.randint(high, (n,))`**（mini_gpt.py）
随机取 n 个起始位置，用来从长文本里切出训练片段。这个任务特有的写法，别的地方用 `DataLoader`。

---

# 三、完整流程图

## 3.1 mini-GPT：从文本到文本

```
════════════ 准备阶段（只做一次）════════════

原始文本 "to be or not to be..."
    │
    ├─→ sorted(set(text)) ──→ 词表 ['a','b',...,' ']  共 V 个字符
    │                          stoi: 字符→ID    itos: ID→字符
    │
    └─→ 全文编码成 ID 序列 ──→ data (总长度 N,) 的整数张量


════════════ 训练阶段（重复 2000 步）════════════

  从 data 里随机切 32 段，每段 64 个字符
        │
        ├─→ x = data[i   : i+64]    输入
        └─→ y = data[i+1 : i+65]    目标（错开一位）
                                    x 的第 t 位要预测 y 的第 t 位
        ↓
  x: (32, 64) 整数 ID
        ↓
┌───────────────────────────────────────────────────┐
│  token_emb(x)         (32,64) → (32,64,128)       │  查表：ID → 向量
│         +                                          │
│  pos_emb(arange(64))  (64,)   → (64,128)          │  查表：位置 → 向量
│                       广播相加                      │
│         ↓                                          │
│  x: (32, 64, 128)                                 │  语义 + 位置
└───────────────────────────────────────────────────┘
        ↓
  构造 causal mask: tril(ones(64,64)) → (1,64,64)
        ↓
╔═══════════════════════════════════════════════════╗
║  TransformerBlock × 4                             ║
║                                                   ║
║    h = LayerNorm(x)                               ║
║    x = x + MultiHeadAttention(h,h,h, mask)  ←横向 ║
║    x = x + FFN(LayerNorm(x))                ←纵向 ║
║                                                   ║
║    形状始终 (32, 64, 128)                          ║
╚═══════════════════════════════════════════════════╝
        ↓
  ln_f: 最终 LayerNorm            (32, 64, 128)
        ↓
  head: Linear(128 → V)           (32, 64, V)
        ↓                          每个位置对 V 个字符的打分
┌───────────────────────────────────────────────────┐
│  摊平成一堆独立的分类任务                            │
│  logits.view(-1, V)  →  (2048, V)                 │
│  y.view(-1)          →  (2048,)                   │
│         ↓                                          │
│  F.cross_entropy  →  一个标量 loss                 │
└───────────────────────────────────────────────────┘
        ↓
  五步训练循环:
    zero_grad() → backward() → step()
        ↓
  loss 从 ln(V)≈3.7 逐步下降


════════════ 生成阶段 ════════════

  起始 idx = encode("to be")   (1, 5)
        │
        ↓  ┌──────── 循环 200 次 ────────┐
        │  │                             │
  截断到 max_len: idx[:, -64:]           │
        ↓                                │
  前向 → logits (1, L, V)                │
        ↓                                │
  只取最后一位 [:, -1, :] → (1, V)       │
        ↓                                │
  除以 temperature → softmax → probs     │
        ↓                                │
  multinomial 按概率抽一个 → next_id     │
        ↓                                │
  cat 接到 idx 后面 ─────────────────────┘
        ↓
  decode(idx) → 生成的文本
```

**三个关键点：**

1. **输入目标错开一位**，所以一次前向同时训练了 64 个位置的预测任务
2. **causal mask 是这个训练方式成立的前提**——没有它，位置 t 能看到 t+1，直接看到答案
3. **生成是串行的**，一次只能出一个字符。训练可以并行，生成不行——**这是自回归模型的固有代价**

---

## 3.2 ViT：从图像到类别

```
输入图像  (B, 3, 224, 224)
        ↓
┌───────────────────────────────────────────────────┐
│  PatchEmbedding                                   │
│    Conv2d(3→768, kernel=16, stride=16)            │
│    核不重叠地扫过整图，每次覆盖一个 16×16 的块      │
│         ↓                                          │
│    (B, 768, 14, 14)      14×14=196 个 patch       │
│         ↓ .flatten(2)                              │
│    (B, 768, 196)                                  │
│         ↓ .transpose(1,2)                          │
│    (B, 196, 768)         ← 变成了 token 序列！     │
└───────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────┐
│  拼上 CLS token                                    │
│    cls_token (1,1,768) --expand--> (B,1,768)      │
│    cat([cls, patches], dim=1)                     │
│         ↓                                          │
│    (B, 197, 768)         ← 197 = 1 + 196          │
└───────────────────────────────────────────────────┘
        ↓
  + pos_emb (1, 197, 768)   可学习位置编码
        ↓
╔═══════════════════════════════════════════════════╗
║  TransformerBlock × N     ← 和 Day 3 写的完全一样  ║
║  无 mask（图像没有"未来"，所有 patch 互相可见）    ║
║  形状始终 (B, 197, 768)                            ║
╚═══════════════════════════════════════════════════╝
        ↓
  ln_f                       (B, 197, 768)
        ↓
  取出 CLS 位置 x[:, 0]      (B, 768)
        ↓                     ← 只用这一个向量代表整张图
  head: Linear(768→类别数)   (B, num_classes)
```

**三个关键点：**

1. **`Conv2d(kernel=16, stride=16)` 就是"切块+拉平+线性变换"三步的合并写法**
2. **无 mask**——图像不像文本有时间顺序，所有 patch 互相可见
3. **只取 CLS 位置**，其余 196 个 patch 的输出在分类任务里被丢弃（但在检测、分割任务里会用上）

---

## 3.3 VLA：把两条线接起来

```
   图像 (B,3,224,224)              指令 "pick up the red cup"
        ↓                                   ↓
   ViT PatchEmbedding                  分词 → token ID
        ↓                                   ↓
   (B, 196, D) 图像 token            (B, 10, D) 语言 token
        │                                   │
        └───────────┬───────────────────────┘
                    ↓  torch.cat(dim=1)
            (B, 206, D)  一个混合序列
                    ↓
            + 位置编码 / 模态标识
                    ↓
    ╔═══════════════════════════════════╗
    ║  Transformer 主干                  ║
    ║  在这里，语言 token 通过 attention  ║
    ║  自动"指向"相关的图像 patch         ║
    ╚═══════════════════════════════════╝
                    ↓
              动作头 (Action Head)
                    ↓
         (B, T, action_dim) 未来 T 步的动作
```

**这就是 OpenVLA、RT-2 的骨架。** 再回看提炼文档说的三个接口：

| 接口 | 在这张图的哪里 |
|---|---|
| **Q/K/V 从哪来** | 是把两种 token 拼起来做 self-attention（上图），还是让语言 cross-attend 图像 |
| **mask 怎么设** | 图像 token 之间要不要全可见？语言能不能看到未来？ |
| **输入怎么拼** | 拼接顺序、各占多少 token、要不要加模态标识 |

**这三处就是你未来改的地方。**


