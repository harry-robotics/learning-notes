"""
mini_gpt.py —— 字符级语言模型，Phase 2.5 的第一次真实训练

用法:
    python3 mini_gpt.py

依赖 transformer.py (同目录)
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F

from transformer import TransformerBlock


# ===========================================================================
# 数据: 不下载任何东西, 直接用内嵌文本
# 想换成更长的文本, 把 TEXT 替换掉即可 (比如 tinyshakespeare)
# ===========================================================================

TEXT = """
to be or not to be that is the question
whether tis nobler in the mind to suffer
the slings and arrows of outrageous fortune
or to take arms against a sea of troubles
and by opposing end them to die to sleep
no more and by a sleep to say we end
the heartache and the thousand natural shocks
that flesh is heir to tis a consummation
devoutly to be wished to die to sleep
to sleep perchance to dream ay theres the rub
for in that sleep of death what dreams may come
when we have shuffled off this mortal coil
must give us pause theres the respect
that makes calamity of so long life
""" * 40


class CharDataset:
    """字符 <-> 整数 ID 的相互转换"""

    def __init__(self, text):
        self.chars = sorted(set(text))
        self.vocab_size = len(self.chars)
        self.stoi = {c: i for i, c in enumerate(self.chars)}
        self.itos = {i: c for i, c in enumerate(self.chars)}
        self.data = torch.tensor([self.stoi[c] for c in text], dtype=torch.long)

    def encode(self, s):
        return torch.tensor([self.stoi[c] for c in s], dtype=torch.long)

    def decode(self, ids):
        return ''.join(self.itos[int(i)] for i in ids)

    def get_batch(self, batch_size, block_size, device):
        """随机取 batch_size 段文本, 输入和目标错开一位"""
        ix = torch.randint(len(self.data) - block_size - 1, (batch_size,))
        x = torch.stack([self.data[i:i + block_size] for i in ix])
        y = torch.stack([self.data[i + 1:i + block_size + 1] for i in ix])
        return x.to(device), y.to(device)


# ===========================================================================
# 模型
# ===========================================================================

class MiniGPT(nn.Module):
    def __init__(self, vocab_size, d_model=128, num_heads=4,
                 d_ff=512, num_layers=4, max_len=128):
        super().__init__()
        self.max_len = max_len
        # 新部件一: 把字符 ID 变成向量 (本质是一张可学习的查找表)
        self.token_emb = nn.Embedding(vocab_size, d_model)
        # 可学习位置编码 —— GPT/BERT/ViT 都用这个而非正弦编码
        self.pos_emb = nn.Embedding(max_len, d_model)

        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff, dropout=0.1)
            for _ in range(num_layers)
        ])
        self.ln_f = nn.LayerNorm(d_model)
        # 新部件二: 把向量变回"下一个字符是谁"的分数
        self.head = nn.Linear(d_model, vocab_size)

    def forward(self, idx):
        """idx: (B, L) 整数 ID -> logits: (B, L, vocab_size)"""
        B, L = idx.shape
        assert L <= self.max_len, f"序列长度 {L} 超过 max_len {self.max_len}"

        pos = torch.arange(L, device=idx.device)
        x = self.token_emb(idx) + self.pos_emb(pos)      # 语义 + 位置

        # causal mask: 位置 i 只能看到 <= i, 否则会看到答案
        mask = torch.tril(torch.ones(L, L, device=idx.device)).unsqueeze(0)

        for blk in self.blocks:
            x, _ = blk(x, mask)
        return self.head(self.ln_f(x))

    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=1.0):
        self.eval()
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.max_len:]             # 超长就截断
            logits = self(idx_cond)[:, -1, :]             # 只要最后一个位置
            probs = F.softmax(logits / temperature, dim=-1)
            next_id = torch.multinomial(probs, num_samples=1)   # 按概率采样
            idx = torch.cat([idx, next_id], dim=1)
        self.train()
        return idx


# ===========================================================================
# 训练
# ===========================================================================

def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"device: {device}")

    ds = CharDataset(TEXT)
    print(f"文本长度 {len(TEXT):,}  词表大小 {ds.vocab_size}")

    block_size, batch_size = 64, 32
    model = MiniGPT(ds.vocab_size, max_len=block_size).to(device)
    n_param = sum(p.numel() for p in model.parameters())
    print(f"参数量 {n_param:,}")

    # 关键自检: 随机模型对每个字符给相同概率, 交叉熵应约为 ln(vocab_size)
    x, y = ds.get_batch(batch_size, block_size, device)
    with torch.no_grad():
        loss0 = F.cross_entropy(
            model(x).view(-1, ds.vocab_size), y.view(-1)
        ).item()
    print(f"\n初始 loss {loss0:.3f}   理论值 ln({ds.vocab_size}) = "
          f"{math.log(ds.vocab_size):.3f}")
    print("两者接近 -> causal mask 正常, 没有答案泄露\n")

    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)

    for step in range(1, 2001):
        x, y = ds.get_batch(batch_size, block_size, device)

        # 训练循环五步, 和 MNIST 时一字不差
        logits = model(x)
        loss = F.cross_entropy(logits.view(-1, ds.vocab_size), y.view(-1))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if step % 200 == 0:
            print(f"step {step:4d}  loss {loss.item():.3f}")

    # 生成
    print("\n--- 生成结果 ---")
    start = ds.encode("to be").unsqueeze(0).to(device)
    out = model.generate(start, max_new_tokens=200, temperature=0.8)
    print(ds.decode(out[0].tolist()))


if __name__ == "__main__":
    torch.manual_seed(0)
    train()