## Phase 2.5 — Transformer

从零实现 Transformer 的学习记录。这是进入具身智能（模仿学习）之前的最后一块基础，因为 Diffusion Policy、ACT、OpenVLA 等机器人策略模型的骨干都建立在 Transformer 之上。

---

## 为什么学这个

方向是**以 driving 为切入 embodiment，研究 VLA policy**。近几年的机器人策略模型有一个共同点：主干是 Transformer，而不是 CNN 或 RNN。

原因可以用一个具体场景说清楚：指令「把红色的杯子拿起来」需要和图像里那一块像素建立联系，但 token「红色的」该关注第 37 个 patch 还是第 142 个，**完全取决于杯子这次摆在哪**。语言和图像之间不存在任何固定的空间邻近关系，CNN 的局部性假设在这里彻底失效。

而 attention 是**动态算出该关注谁**的，杯子换位置权重自动跟着换。

所以这个阶段的目标不是"了解 Transformer"，而是**能在 debug 时把整条形状流跑在脑子里**——因为复现论文时定位问题的人只能是我自己。

---

## 目录结构

```
phase2.5-transformer/
├── README.md                     本文件
├── transformer.py                核心实现（Encoder + 全部组件）
├── mini_gpt.py                   字符级 GPT，含训练与生成
├── vit.py                        ViT 结构（只验证前向与形状，不训练）
├── transformer-essentials.md     核心提炼：哪些真正有用、哪些可以忘
│
├── day01/                        注意力机制
├── day02/                        多头注意力
├── day03/                        位置编码 + Transformer Block
└── review-tracker.md             复习追踪
```

每个 `dayXX/` 是当天的学习过程记录（含实验、踩坑、中间输出），**只增不改**。
根目录的 `.py` 是整理后可复用的模块。

---

## 快速开始

```bash
python3 transformer.py    # 七项自检
python3 vit.py            # ViT 形状流
python3 mini_gpt.py       # 训练字符级 GPT，几分钟
```

`transformer.py` 的七项自检：形状保持、注意力权重归一化、causal mask 生效、cross-attention 形状、**位置编码是否真的打破了置换等变性**、参数量分解、梯度回传。

环境：Python 3.10 + PyTorch 2.13.0+cu130，WSL2 (Ubuntu)，RTX 5060 Laptop 8GB。

---

## 实现内容

| 模块 | 说明 |
|---|---|
| `scaled_dot_product_attention` | 四步：算相似度 → 缩放 → softmax → 加权求和 |
| `MultiHeadAttention` | 把 `d_model` 切成 h 份并行；三个来源参数分开写，支持 cross-attention |
| `FeedForward` | 逐位置独立的升维-非线性-降维 |
| `PositionalEncoding` | 正弦编码，无长度上限 |
| `TransformerBlock` | Pre-LN 两子层结构，形状保持 |
| `TransformerEncoder` | N 层堆叠 + 收尾归一化 |
| `MiniGPT` | 加上 token/position embedding 与输出头，可训练可生成 |
| `ViT` | patch embedding + CLS token，图像分类结构 |

**几个刻意的设计选择：**

- **全程负索引**（`size(-1)`、`transpose(-2,-1)`、`softmax(dim=-1)`）——让同一个函数能吃 `(L,D)`、`(B,L,D)`、`(B,h,L,D)` 三种输入，后面加 heads 维时不用改一行
- **Q/K/V 三个参数分开写**而不是一个 `x`——否则 cross-attention 永远做不了，而那是多模态的核心
- **`mask.unsqueeze(1)` 显式留出 heads 维**——不依赖广播自动补维。当 `batch == num_heads` 时自动补维**不报错但结果全错**
- **Pre-LN 而非原论文的 Post-LN**——让残差旁路保持干净，深层训练稳定
- **返回注意力权重**——用于可视化和不变量检查

---

## 学习记录

### 注意力机制

CNN 的感受野每层只长 2，RNN 必须串行且记忆容量固定。需要一种**任意两个位置直接相连、且可并行**的机制。

Attention 是一次**可导的软检索**：Q 拿着问题去和所有 K 比对，按相似度混合所有 V。用 softmax 而不是 argmax，是因为 argmax 不可导、梯度传不过去，整个网络就没法端到端训练。

三个实现要点：

- **`/√d_k`**：点积方差随维度线性增长（Var = d_k），不缩放会让 softmax 接近 one-hot、梯度趋近 0
- **mask 填 `-inf` 不填 0**：屏蔽发生在 softmax **之前**，`exp(-inf)=0` 而 `exp(0)=1`——填 0 会让屏蔽反而变成加权
- **`dim=-1`**：`scores` 的行是"谁在问"，要的是每个 query 的分配之和为 1

### 多头注意力

一组 Q/K/V 只能定义一种"什么算相似"的标准，面对多种关系会被迫**平均化**。

多头**不是做 8 遍**，而是把 512 维切成 8 份、每份 64 维——**总算力和参数量都不变**。这个交换划算的原因是：瓶颈在"能有几种独立的关注模式"，不在"每个模式看得多深"。

难点全在张量形状：`(B,L,D)` → `view` 拆成 `(B,L,h,d_k)` → `transpose` 挪成 `(B,h,L,d_k)`。把 h 放到倒数第三维之后，它自动被当作批次的一部分，8 个头一次算完，无需循环。

`transpose` 只改读取规则不搬内存，所以后面接 `view` 必须先 `contiguous()`。

### 位置编码 + Transformer Block

Attention 的三步计算都与顺序无关（点积只看向量数值、softmax 与顺序无关、求和与加数顺序无关），所以**它把输入当成集合而非序列**——「猫追狗」和「狗追猫」是同一个输入。

**验证这一点的对照实验**（在 `day03/`）：打乱输入顺序后，不加位置编码时输出只是跟着打乱（`allclose` 为 `True`，即置换等变），加了之后输出真正不同（`False`）。**两行代码把一个抽象论证变成了可验证的事实。**

FFN 常被忽略，但它的**参数量是 attention 的两倍**。分工是：attention 横向从别的 token 搬运信息，FFN 纵向独立加工，位置之间不通气。

### mini-GPT 与真实训练

前面全是搭积木看形状，这一步第一次让 loss 真的降下来。

**最值得带走的技巧：初始 loss 应该约等于 ln(词表大小)。**

推导很简单——随机模型给每个字符相同概率 1/V，交叉熵就是 -ln(1/V) = ln V。**如果实测远低于理论值，说明有答案泄露，多半是 causal mask 没生效。**

一次前向、一行代码，就能在训练三小时之前发现结构性错误。

### ViT

图像切成 16×16 的 patch 变成 token 序列。理论上是"切块 → 拉平 → 线性变换"三步，**实现上一个 `Conv2d(kernel=16, stride=16)` 就完成**——步长等于核大小意味着核不重叠地扫过整图，数学上完全等价。

这是"论文写三步、代码写一步"的典型例子。**读代码时能认出它们是同一件事，这种识别能力比记住任何单个写法都有用。**

ViT 的代价：CNN 自带的局部性与平移不变性先验它全丢了，本来免费的知识现在必须从数据里学。**所以它在小数据上不如 CNN，需要大规模预训练才能反超。**

---

## 一个宏观视角

比起架构图，更好用的心智模型是**残差流**：

每个 token 有一条从头贯穿到尾的信息主干，维度始终是 `d_model`，从不改变。每一层只做一件事——**读取主干上的当前内容，算出一个修正量，加回主干**。

```
token 主干:  ═══════════════════════════════>
             ↑        ↑        ↑        ↑
        每层往上"加"一点，从不推倒重来
```

Attention 横向从别的 token 主干上读信息，FFN 纵向加工自己的。一横一纵，交替 N 次。

这个视角能直接解释掉一串"为什么"：为什么形状必须保持（主干宽度固定）、为什么要残差（主干本身就是残差）、为什么 LayerNorm 放在子层入口（只清洗读进去的副本，主干保持干净）、为什么能堆到 96 层（每层只做小修正）。

**这也是我读架构类论文的定位工具**：先问它改的是 Q 的来源、mask、还是输入拼接方式——大部分架构创新能被这三个问题定位。

详见 [`transformer-essentials.md`](./transformer-essentials.md)。

---

## 完成情况

- [x] Scaled Dot-Product Attention
- [x] Multi-Head Attention
- [x] 位置编码 + Transformer Block
- [x] 三种注意力对比（self / masked self / cross）
- [x] mini-GPT 训练跑通
- [x] ViT 结构与形状验证

---

## 参考资料

- Vaswani et al., *Attention Is All You Need* (2017)
- Dosovitskiy et al., *An Image Is Worth 16x16 Words* (ViT, 2020)
- 3Blue1Brown, Neural Networks 系列 Ch.5–7
- Karpathy, *Let's build GPT: from scratch, in code, spelled out*
- 李沐《动手学深度学习》v2

---

## 后续

Phase 3 进入具身智能：模仿学习入门 → 在 LIBERO 上复现 Diffusion Policy 或 ACT。

需要说明的是，**LIBERO 这个基准已经接近饱和**（多个任务套件上 95% 以上是常态），所以复现的定位是**学习验收而非研究产出**——它证明数据处理与训练流程正确，真正的问题要从失败模式里找。

注意到 ACT 用了一组可学习的 query 向量去 cross-attend 观测特征、一次性输出整段动作，**这正好对应这个阶段学的 cross-attention 中"Q 从哪来"这个设计维度**。这也是我打算从它入手的原因之一。
