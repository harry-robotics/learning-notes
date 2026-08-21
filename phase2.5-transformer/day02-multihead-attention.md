# Day 02｜Multi-Head Attention：把算力切成八份分头使用

> 2026-08-16｜Phase 2.5 Transformer 第 2 天
> 今天没有新数学，全部难点在张量形状。

---

## 一、今天真正想通的一件事

**多头注意力不是"做 8 遍"，而是"把 512 维切成 8 份，每份 64 维"。**

我一开始的直觉是"既然要 8 个头，就把昨天的函数跑 8 遍"——**这个直觉是错的，而且错在最关键的地方**：那样计算量会变成 8 倍，Transformer 根本堆不到几十层。

真实做法是切分：

$$d_k = \frac{d_{model}}{h} = \frac{512}{8} = 64$$

```
单头:  [────────── 512 维 ──────────]   一个头处理全部
8 头:  [64][64][64][64][64][64][64][64]  每个头只管自己那 64 维
```

算一笔账就清楚了：8 个头各做 `(n,64)@(64,n)`，加起来等于 1 个头做 `(n,512)@(512,n)`。**计算量完全相等。**

**参数量也一样**：四个线性层都是 `(512,512)`，形状里根本没出现 `num_heads`。多头是在算完线性变换之后、通过 `view`+`transpose` 在维度上切分实现的——**切分不产生新参数，只是改变了对已有数字的分组解释**。

所以多头在参数和算力上是**免费**的。它没多花钱，只是换了种花法：**把"单头深度"换成了"视角数量"。**

---

## 二、为什么一组 QKV 不够

一组 $W^Q, W^K$ 只能定义**一种**"什么算相似"的标准。但一句话里同时有很多种关系：

| 关系 | 例子 |
|---|---|
| 形容词 → 名词 | fluffy → creature |
| 动词 → 主语 | roamed → creature |
| 动词 → 宾语 | roamed → forest |
| 代词 → 指代对象 | it → creature |

强行用一组的后果是**平均化**：模型被迫学一个"什么关系都能沾一点边"的折中方案，权重变成一坨比较平均的分布，**每一种关系都捕捉得模模糊糊**。

通俗说：一个人同时干八份工作，八份都干不好。

**需要提醒自己**：说"head 1 学形容词、head 2 学动词"只是帮助理解的说法，**不是事实**。没有机制强制分工，分工是训练中自发涌现的，而且实际训练出的头往往对应不上人类能命名的语言学概念。

---

## 三、划算在哪（这是今天最值得记的推理）

每个头从 512 维降到 64 维，表达能力确实下降了。为什么还划算？

**核心：瓶颈不在"每个头看得多深"，而在"能有几个视角"。**

- 一个 512 维的头，对"位置 i 该关注位置 j 多少"**只能给出一个数**，整个序列只有**一个** `(n,n)` 权重矩阵
- 8 个 64 维的头，能给出**8 个独立的** `(n,n)` 矩阵。位置 i 对位置 j 可以在关系 A 上高度关注、同时在关系 B 上完全忽略

**多头把参数从"加深单一视角"重新分配到了"增加视角数量"上。每个头弱在了不构成瓶颈的地方，强在了构成瓶颈的地方。**

> 这类"不增加成本、只重新分配"的设计特别优雅。前提是**找对了瓶颈**——找对瓶颈，改进就可以是免费的。

---

## 四、形状变换（今天的真正难点）

目标：`(batch, seq_len, d_model)` → `(batch, num_heads, seq_len, d_k)`

```
(2, 5, 512)  →view→  (2, 5, 8, 64)  →transpose(1,2)→  (2, 8, 5, 64)
                                                          ↑ 送进注意力
```

**为什么 num_heads 要挪到倒数第三维**：因为昨天的函数全用负索引，**它只认最后两维是 `(seq_len, d_k)`，前面有几维一概当批次处理**。把 heads 放到前面去，8 个头就自动被并行计算，**一行循环都不用写**。

> 昨天"全用负索引"这个决策，今天兑现了。如果昨天写的是 `Q.size(2)`，今天多一维立刻就错。

**算完再变回去**：`transpose` 回来 → `contiguous` → `view` 合并。

### 三个新 API

**`view`**：改形状不复制数据。张量在内存里其实是**一条一维数据流**，"形状"只是分组解释方式。唯一硬性要求是元素总数不变。

**`//`**：整除，结果是整数。用 `/` 会得到 `64.0` 这个浮点数，传给形状参数会报错。这也是为什么 `d_model` 必须能被 `num_heads` 整除。

**`contiguous`**：`transpose` 不真搬内存数据，只改"怎么读"的规则（stride）。所以转置后**逻辑顺序和物理顺序对不上**，而 `view` 恰恰按物理顺序分组——PyTorch 直接禁止，报错。`contiguous()` 就是真复制一份让两者重新对齐。

**规则可以直接背：transpose / permute 之后紧接着 view，就要加 contiguous。**

---

## 五、$W^O$：分头看之后要汇总

拼接出来的 512 维，前 64 维来自 head 1、接下来 64 维来自 head 2……**这 8 段之间还没发生任何交互，只是被摞在一起。**

$W^O$ 是一个 `(512,512)` 线性变换，让输出的每一维都成为 8 个头结果的加权组合，模型自己学"哪个头的信息更重要、怎么融合"。

去掉它能跑（形状对得上），但下一层拿到的是 8 段各说各话的信息，**每层少一次融合机会，堆叠多层后差距累积**。

> **多头负责"分头看"，$W^O$ 负责"汇总"。**

---

## 六、完整实现

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0, "d_model 必须能被 num_heads 整除"
        self.d_model, self.num_heads = d_model, num_heads
        self.d_k = d_model // num_heads
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def split_heads(self, x):
        batch, seq_len, _ = x.size()
        x = x.view(batch, seq_len, self.num_heads, self.d_k)
        return x.transpose(1, 2)

    def combine_heads(self, x):
        batch, _, seq_len, _ = x.size()
        x = x.transpose(1, 2).contiguous()
        return x.view(batch, seq_len, self.d_model)

    def forward(self, query, key, value, mask=None):
        Q = self.split_heads(self.W_q(query))
        K = self.split_heads(self.W_k(key))
        V = self.split_heads(self.W_v(value))
        if mask is not None:
            mask = mask.unsqueeze(1)
        out, attn = scaled_dot_product_attention(Q, K, V, mask)
        out = self.combine_heads(out)
        return self.W_o(out), attn
```

**参数量 = 4 × (512×512 + 512) = 1,050,624。** 每个 `nn.Linear(512,512)` 有 `512×512` 个权重（每对输入输出连一根线）加 512 个 bias（每个**输出维度**一个，加到序列里所有 token 上，和卷积的"每个输出通道一个 bias"是同一个道理）。

**`forward` 的参数是三个而不是一个 `x`**，因为要支持 cross-attention：`mha(语言, 图像, 图像)`。写成一个 `x` 的话，VLA 最核心的机制就永远做不了。

---

## 七、cross-attention 跑通了（Day 1 遗留问题的兑现）

```python
lang = torch.randn(2, 5, 512)       # 5 个语言 token
img  = torch.randn(2, 196, 512)     # 196 个图像 patch
out, attn = mha(lang, img, img)     # Q 来自语言，K/V 来自图像

# out:  (2, 5, 512)      长度跟随 Q
# attn: (2, 8, 5, 196)   不是方阵!
```

**一行代码都没改。** 这就是接口设计的回报。

两个要点：
- 权重矩阵**不是方阵**了，是 `5×196` 的长条
- **输出长度跟随 Q 不跟随 K**，5 个语言 token 各拿到一份"与它最相关的图像内容的混合"

**K 和 V 必须都来自图像**，因为它们一一配对：先用 K 判断"这块 patch 是不是我要找的"，选中后取它的 V。分家了就是判断依据和取回内容对不上号。

> 这也解释了 Day 1 的 docstring 为什么把 `seq_len_q` 和 `seq_len_k` 分开写——当时是伏笔。

---

## 八、易错点（我实际踩的坑）

> 以下是这次真实卡住的地方，做完思考题后继续补充。

**1. 以为多头是"跑 8 遍"。**
第一直觉是复制 8 份各算各的，那样计算量 8 倍。真实做法是切分维度，**总算力不变**。这个误解如果不纠正，后面看到"参数量与头数无关"会完全想不通。

**2. 以为 $W^Q$ 是降维变换。**
标准实现里 $W^Q$ 是 `(512,512)`，**维度根本没变**。降维只是分头的副产物。这三个矩阵真正的目的是：分离 Q/K/V 三种冲突的角色，以及**让"什么算相似"本身变成可学习的**。

**3. `contiguous` 什么时候需要，判据搞错过。**
一开始以为是"combine 要、split 不要"。真正的判据是 **"view 之前有没有做过 transpose"**——和函数名无关。split 是 view 在前、transpose 在后，所以不需要；combine 反过来，所以必须要。

---

## 九、两个"不报错但全错"的陷阱

今天新增了两个 Day 1 那类阴险 bug。**都不会报错，都会让 loss 正常下降。**

**陷阱一：`split_heads` 漏掉 `transpose(1,2)`**

形状停在 `(batch, seq_len, num_heads, d_k)`，注意力函数会把 `(8, 64)` 误认成"8 个 token 各 64 维"。

**实际算出来的是：对每个 token，独立地在它自己的 8 个头切片之间做注意力。token 与 token 之间没有任何信息交流**——attention 存在的全部意义没了。

**抓它的手段**：检查权重形状是否为 `(2,8,5,5)`。漏了 transpose 会变成 `(2,5,8,8)`，一眼能看出。

**陷阱二：`mask` 漏掉 `unsqueeze(1)`**

广播时维数不够的一方会**在最前面自动补 1**。

- mask 是 `(1,seq,seq)` → 补成 `(1,1,seq,seq)`，**碰巧正确**
- mask 是 `(batch,seq,seq)` → 补成 `(1,batch,seq,seq)`，**batch 维跑到了 heads 的位置上**
  - `batch ≠ heads` → 报错，运气好
  - **`batch == heads`（比如都是 8）→ 不报错，但每个头被套上了某个样本的 mask，全串了**

**不要依赖自动补维，要显式写出意图。**

---

## 十、重点思考题（艾宾浩斯自测用）

1. **8 头的计算量是单头的几倍？** 用 `(n,512)@(512,n)` vs `(n,64)@(64,n)×8` 算给自己看。
2. **每个头只有 64 维，为什么这个交换划算？** 从"瓶颈在哪"论证。
3. **`contiguous` 的判据是什么？** 说清为什么 split 不需要、combine 需要。
4. **`split_heads` 漏掉 transpose 会算出什么？** 会报错吗？靠什么检查能抓住？
5. **参数量为什么与 num_heads 无关？** 那多头的"成本"体现在哪？

---

## 十一、明天

位置编码 + Transformer Block。要解决的是 Day 1 思考题暴露的那个问题：**self-attention 对输入顺序完全不敏感**，「猫追狗」和「狗追猫」在它眼里是同一个输入。