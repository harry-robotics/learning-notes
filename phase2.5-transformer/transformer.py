"""
Transformer Encoder —— 完整实现
Day 1~3 全部内容的整合版本

用法:
    python3 transformer.py

依赖: torch
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


# ===========================================================================
# 1. Scaled Dot-Product Attention
#    一次可导的"软检索": Q 去问所有 K, 按相似度混合所有 V
# ===========================================================================

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q: (..., seq_len_q, d_k)
    K: (..., seq_len_k, d_k)
    V: (..., seq_len_k, d_v)
    mask: (..., seq_len_q, seq_len_k), 1 可见 / 0 屏蔽
    返回: (..., seq_len_q, d_v), (..., seq_len_q, seq_len_k)

    全程负索引 -> 前面有几个维度都不管, 自动当批次处理
    """
    d_k = Q.size(-1)
    # 除以 sqrt(d_k): 点积方差随维度线性增长, 不缩放会让 softmax 饱和
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    if mask is not None:
        # 填 -inf 而非 0: 屏蔽发生在 softmax 之前, exp(-inf)=0
        scores = scores.masked_fill(mask == 0, float('-inf'))
    # dim=-1: 每个 query 的注意力分配之和为 1
    attn_weights = F.softmax(scores, dim=-1)
    return attn_weights @ V, attn_weights


# ===========================================================================
# 2. Multi-Head Attention
#    把 d_model 切成 h 份并行, 总算力不变, 换来 h 种独立的关注模式
# ===========================================================================

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0, "d_model 必须能被 num_heads 整除"
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def split_heads(self, x):
        """(B, L, D) -> (B, h, L, d_k)   把 h 挪到前面, 让它变成"批次"的一部分"""
        batch, seq_len, _ = x.size()
        return x.view(batch, seq_len, self.num_heads, self.d_k).transpose(1, 2)

    def combine_heads(self, x):
        """(B, h, L, d_k) -> (B, L, D)   transpose 之后接 view, 必须先 contiguous"""
        batch, _, seq_len, _ = x.size()
        x = x.transpose(1, 2).contiguous()
        return x.view(batch, seq_len, self.d_model)

    def forward(self, query, key, value, mask=None):
        """
        三个来源分开写, 才能支持 cross-attention:
          self  : mha(x, x, x)
          cross : mha(语言, 图像, 图像)
        """
        Q = self.split_heads(self.W_q(query))
        K = self.split_heads(self.W_k(key))
        V = self.split_heads(self.W_v(value))

        if mask is not None:
            mask = mask.unsqueeze(1)   # 给 num_heads 维显式留位置, 不依赖自动补维

        out, attn = scaled_dot_product_attention(Q, K, V, mask)
        return self.W_o(self.combine_heads(out)), attn


# ===========================================================================
# 3. Position-wise Feed-Forward
#    attention 只搬运信息, FFN 负责逐位置加工
# ===========================================================================

class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)      # 升维
        self.linear2 = nn.Linear(d_ff, d_model)      # 降回原维
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # nn.Linear 只作用在最后一维 -> 天然"逐位置独立", 无需额外处理
        return self.linear2(self.dropout(F.relu(self.linear1(x))))


# ===========================================================================
# 4. Positional Encoding
#    attention 对顺序完全不敏感, 必须从外部注入位置信息
# ===========================================================================

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        # 等价于 1 / 10000^(2i/d), 用 exp-log 改写避免数值溢出
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)   # 偶数维
        pe[:, 1::2] = torch.cos(position * div_term)   # 奇数维

        # buffer: 不可学习, 但随 model.to(device) 一起搬运
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        return self.dropout(x + self.pe[:, :x.size(1)])


# ===========================================================================
# 5. Transformer Block (Pre-LN)
#    形状保持 -> 可以原样堆叠 N 层
# ===========================================================================

class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attn = MultiHeadAttention(d_model, num_heads)
        self.ff = FeedForward(d_model, d_ff, dropout)
        self.ln1 = nn.LayerNorm(d_model)    # 两个 LN 各有独立的 gamma/beta,
        self.ln2 = nn.LayerNorm(d_model)    # 不能复用同一个
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # 子层一: 位置之间交流
        h = self.ln1(x)
        attn_out, attn_w = self.attn(h, h, h, mask)
        x = x + self.dropout(attn_out)      # 残差旁路保持干净 = Pre-LN

        # 子层二: 每个位置独立加工
        x = x + self.dropout(self.ff(self.ln2(x)))
        return x, attn_w


# ===========================================================================
# 6. Transformer Encoder
# ===========================================================================

class TransformerEncoder(nn.Module):
    def __init__(self, d_model=512, num_heads=8, d_ff=2048,
                 num_layers=6, max_len=5000, dropout=0.1):
        super().__init__()
        self.pos_enc = PositionalEncoding(d_model, max_len, dropout)
        # 必须用 ModuleList, 普通 list 里的层不会被注册
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        self.ln_final = nn.LayerNorm(d_model)   # Pre-LN 架构需要一个收尾归一化

    def forward(self, x, mask=None):
        """x: (B, L, d_model) -> (B, L, d_model)"""
        x = self.pos_enc(x)
        attn_maps = []
        for blk in self.blocks:
            x, attn_w = blk(x, mask)
            attn_maps.append(attn_w)
        return self.ln_final(x), attn_maps


# ===========================================================================
# 工具函数
# ===========================================================================

def make_causal_mask(seq_len, device=None):
    """下三角, 位置 i 只能看到 <= i 的位置。返回 (1, L, L)"""
    return torch.tril(torch.ones(seq_len, seq_len, device=device)).unsqueeze(0)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


# ===========================================================================
# 自检
# ===========================================================================

if __name__ == "__main__":
    torch.manual_seed(0)

    B, L, D, H, FF, N = 2, 10, 512, 8, 2048, 6
    model = TransformerEncoder(D, H, FF, N)
    x = torch.randn(B, L, D)

    # --- 形状保持 ---
    out, maps = model(x)
    assert out.shape == x.shape
    print(f"[1] 形状保持        {tuple(x.shape)} -> {tuple(out.shape)}")
    print(f"    注意力图 {len(maps)} 层, 每层 {tuple(maps[0].shape)}")

    # --- 权重归一化 ---
    s = maps[0].sum(dim=-1)
    assert torch.allclose(s, torch.ones_like(s), atol=1e-5)
    print("[2] 每个 query 的权重和为 1")

    # --- causal mask ---
    mask = make_causal_mask(L)
    _, maps_m = model(x, mask)
    upper = maps_m[0][0, 0].triu(diagonal=1)
    assert upper.abs().max() < 1e-8
    print("[3] causal mask 生效, 上三角全为 0")

    # --- cross-attention ---
    mha = MultiHeadAttention(D, H)
    lang, img = torch.randn(B, 5, D), torch.randn(B, 196, D)
    out_c, attn_c = mha(lang, img, img)
    print(f"[4] cross-attention  out {tuple(out_c.shape)}  "
          f"attn {tuple(attn_c.shape)}  <- 非方阵, 长度跟随 Q")

    # --- 位置编码确实打破了置换等变性 ---
    blk = TransformerBlock(D, H, FF, dropout=0.0).eval()
    pe = PositionalEncoding(D, dropout=0.0).eval()
    xs = torch.randn(1, 4, D)
    perm = torch.tensor([2, 0, 3, 1])
    with torch.no_grad():
        a, _ = blk(xs)
        b, _ = blk(xs[:, perm, :])
        c, _ = blk(pe(xs))
        d, _ = blk(pe(xs[:, perm, :]))
    print(f"[5] 无位置编码 -> 置换等变: {torch.allclose(b, a[:, perm, :], atol=1e-5)}")
    print(f"    有位置编码 -> 置换等变: {torch.allclose(d, c[:, perm, :], atol=1e-5)}")

    # --- 参数量 ---
    blk1 = TransformerBlock(D, H, FF)
    n_attn = count_parameters(blk1.attn)
    n_ff = count_parameters(blk1.ff)
    print(f"[6] 单层  attention {n_attn:,}  FFN {n_ff:,}  "
          f"(FFN 约为 attention 的 {n_ff/n_attn:.1f} 倍)")
    print(f"    整个模型 {count_parameters(model):,}")

    # --- 梯度能传到第一层 ---
    out, _ = model(x)
    out.sum().backward()
    g = model.blocks[0].attn.W_q.weight.grad
    assert g is not None and g.abs().max() > 0
    print("[7] 梯度成功回传到第 0 层")