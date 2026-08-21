# Phase 2.5 — Transformer

从零手写 Transformer 的学习记录与实现。这是 Phase 3（具身智能 / 模仿学习）之前的最后一块基础，因为 Diffusion Policy、ACT、OpenVLA 等 VLA 模型的骨干全部建立在 Transformer 之上。

---

## 为什么学这个

我的方向是**以 driving 为切入 embodiment，研究 VLA policy**。近几年的机器人策略模型有一个共同点：主干是 Transformer，而不是 CNN 或 RNN。

原因可以用一个具体场景说清楚：指令「把红色的杯子拿起来」需要和图像里那一块像素建立联系，但 token「红色的」该关注第 37 个 patch 还是第 142 个，**完全取决于杯子这次摆在哪**。语言 token 和图像 patch 之间不存在任何固定的空间邻近关系，CNN 的局部性假设在这里彻底失效。

Transformer 的 cross-attention 恰好对症：它**动态算出该关注谁**，杯子换位置权重自动跟着换。

所以这个阶段的目标不是"了解 Transformer"，而是**能在 debug 时把整条形状流跑在脑子里**——因为复现论文时定位问题的人只能是我自己。

---

## 目录结构

```
phase2.5-transformer/
├── README.md                     本文件
├── transformer.py                整合实现（Encoder 完整，持续更新）
├── transformer-essentials.md     核心提炼：哪些真正有用、哪些可以忘
│
├── day01/                        注意力机制
│   ├── attention_from_scratch.ipynb
│   └── day01-push.md
├── day02/                        多头注意力
│   ├── multi_head_attention.ipynb
│   └── day02-push.md
├── day03/                        位置编码 + Transformer Block
│   ├── transformer_block.ipynb
│   └── day03-push.md
└── review-tracker.md             艾宾浩斯复习追踪
```

每个 `dayXX/` 是当天的学习过程记录（含实验、踩坑、中间输出），**只增不改**。
`transformer.py` 是整理后可复用的模块，随进度持续演进。

---

## 快速开始

```bash
python3 transformer.py
```

会跑七项自检：形状保持、注意力权重归一化、causal mask 生效、cross-attention 形状、位置编码是否真的打破了置换等变性、参数量分解、梯度回传。

```python
from transformer import TransformerEncoder, make_causal_mask

model = TransformerEncoder(d_model=512, num_heads=8, d_ff=2048, num_layers=6)
x = torch.randn(2, 10, 512)
out, attn_maps = model(x)              # (2, 10, 512)
out, _ = model(x, make_causal_mask(10))  # 自回归模式
```

环境：Python 3 + PyTorch 2.13.0+cu130，WSL2 (Ubuntu)，RTX 5060 Laptop 8GB。

---

## 实现内容

| 模块 | 说明 |
|---|---|
| `scaled_dot_product_attention` | 核心的四步：算相似度 → 缩放 → softmax → 加权求和 |
| `MultiHeadAttention` | 把 `d_model` 切成 h 份并行；三个来源参数分开写，支持 cross-attention |
| `FeedForward` | 逐位置独立的升维-非线性-降维 |
| `PositionalEncoding` | 正弦编码，无长度上限 |
| `TransformerBlock` | Pre-LN 两子层结构，形状保持 |
| `TransformerEncoder` | N 层堆叠 + 收尾归一化 |

**几个刻意的设计选择：**

- **全程负索引**（`size(-1)`、`transpose(-2,-1)`、`softmax(dim=-1)`）——让同一个函数能吃 `(L,D)`、`(B,L,D)`、`(B,h,L,D)` 三种输入，加 heads 维时不用改一行
- **Q/K/V 三个参数分开写**而不是一个 `x`——否则 cross-attention 永远做不了
- **`mask.unsqueeze(1)` 显式留出 heads 维**——不依赖广播自动补维。当 `batch == num_heads` 时自动补维不报错但结果全错
- **Pre-LN 而非原论文的 Post-LN**——让残差旁路保持干净，深层训练稳定
- **返回注意力权重**——用于可视化和不变量检查

---

## 学习记录

### Day 01 — 注意力机制

CNN 的感受野每层只长 2，RNN 必须串行且记忆容量固定。需要一种**任意两个位置直接相连、且可并行**的机制。

Attention 是一次**可导的软检索**：Q 拿着问题去和所有 K 比对，按相似度混合所有 V。用 softmax 而不是 argmax，是因为 argmax 不可导、梯度传不过去。

三个实现要点：

- `/√d_k`：点积方差随维度线性增长（$\mathrm{Var}=d_k$），不缩放会让 softmax 饱和、梯度趋近 0
- mask 填 `-inf` 不填 0：屏蔽发生在 softmax **之前**，`exp(-inf)=0` 而 `exp(0)=1`
- `dim=-1`：`scores` 的行是"谁在问"，要的是每个 query 的分配之和为 1

同时补上了 LayerNorm 与残差连接（Day 3 组装 Block 时用），以及 softmax 本身。

### Day 02 — 多头注意力

一组 Q/K/V 只能定义一种"什么算相似"的标准，面对多种关系会被迫**平均化**。

多头**不是做 8 遍**，而是把 512 维切成 8 份、每份 64 维——总算力和参数量都不变。这个交换划算的原因是：**瓶颈在"能有几种独立的关注模式"，不在"每个模式看得多深"**。

难点全在张量形状：`(B,L,D)` → `view` 拆成 `(B,L,h,d_k)` → `transpose` 挪成 `(B,h,L,d_k)`。把 `h` 放到倒数第三维之后，它自动被当作批次的一部分，8 个头一次算完，无需循环。

`transpose` 只改读取规则不搬内存，所以后面接 `view` 必须先 `contiguous()`。

### Day 03 — 位置编码 + Transformer Block

Attention 的三步计算都与顺序无关（点积只看向量数值、softmax 与顺序无关、求和与加数顺序无关），所以**它把输入当成集合而非序列**——「猫追狗」和「狗追猫」是同一个输入。必须从外部注入位置信息。

正弦编码用不同频率的 sin/cos，**靠前的维度像秒针、靠后的像时针**，组合起来唯一确定一个位置。它同时解决了整数编号的数值无界、归一化方案的含义随长度变化、以及可学习编码无法外推三个问题。

FFN 常被忽略，但它的**参数量是 attention 的两倍**。分工是：

- **Attention 横向**——从别的 token 搬运信息
- **FFN 纵向**——每个位置独立加工，位置之间不通气

Block 的结构是两个子层，各为 `x = x + Sublayer(LayerNorm(x))`。输出形状与输入完全相同，所以能原样堆叠 N 层。

**验证位置编码确实有效的对照实验**（`day03/` 里）：打乱输入顺序后，不加位置编码时输出只是跟着打乱（`allclose` 为 `True`，即置换等变），加了之后输出真正不同（`False`）。

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

详见 [`transformer-essentials.md`](./transformer-essentials.md)。

---

## 进度

- [x] Day 01 — Scaled Dot-Product Attention
- [x] Day 02 — Multi-Head Attention
- [x] Day 03 — 位置编码 + Transformer Block
- [ ] Day 04 — 三种注意力对比 + Decoder（cross-attention 是 VLA 的核心机制）
- [ ] Day 05 — 手搓 mini-GPT 并完成一次真实训练
- [ ] Day 06 — ViT：Transformer 进入视觉，通向 VLA 的必经环节
- [ ] Day 07 — 骨架复习与整理

**当前实现是 Encoder 部分。** 尚缺输入嵌入层、带 cross-attention 的 Decoder、任务头与训练脚本，将随 Day 04–06 补齐。

---

## 参考资料

- Vaswani et al., *Attention Is All You Need* (2017)
- Dosovitskiy et al., *An Image Is Worth 16x16 Words* (ViT, 2020)
- 3Blue1Brown, Neural Networks 系列 Ch.5–7
- Karpathy, *Let's build GPT: from scratch, in code, spelled out*
- 李沐《动手学深度学习》v2

---

## 后续方向

Phase 3 进入具身智能：模仿学习入门 → 在 LIBERO 或 ManiSkill 上复现 Diffusion Policy / ACT。

ACT 的核心机制正好用到这个阶段学的东西——它用一组**可学习的 query 向量**去 cross-attend 观测特征，一次性输出整段动作序列。**创新点就在"Q 从哪来"这个接口上。**