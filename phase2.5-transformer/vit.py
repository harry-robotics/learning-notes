"""
vit.py —— Vision Transformer 结构

只验证前向流程和形状, 不训练。
理由: 从零训练 ViT 在小数据上效果差且耗时长, 实际工作中一律用预训练权重。
理解"图像怎么变成 token"才是重点。

用法:
    python3 vit.py

依赖 transformer.py (同目录)
"""

import torch
import torch.nn as nn

from transformer import TransformerBlock


class PatchEmbedding(nn.Module):
    """
    图像 -> token 序列

    理论上三步: 切成 16x16 的块 -> 每块拉平 -> 线性变换
    实现上一步: 一个 kernel=16, stride=16 的卷积
              (核不重叠地扫过整图, 每次覆盖恰好一个 patch)
    两者数学等价。
    """

    def __init__(self, img_size=224, patch_size=16, in_channels=3, d_model=768):
        super().__init__()
        assert img_size % patch_size == 0, "图像尺寸必须能被 patch 大小整除"
        self.num_patches = (img_size // patch_size) ** 2      # 14*14 = 196
        self.proj = nn.Conv2d(in_channels, d_model,
                              kernel_size=patch_size, stride=patch_size)

    def forward(self, x):
        # (B,3,224,224) -> (B,768,14,14) -> (B,768,196) -> (B,196,768)
        return self.proj(x).flatten(2).transpose(1, 2)


class ViT(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_channels=3,
                 num_classes=1000, d_model=768, num_heads=12,
                 d_ff=3072, num_layers=12, dropout=0.1):
        super().__init__()
        self.patch_embed = PatchEmbedding(img_size, patch_size,
                                          in_channels, d_model)
        n_patches = self.patch_embed.num_patches

        # CLS token: 一个额外的可学习 token, 专门用来汇总全图信息
        self.cls_token = nn.Parameter(torch.zeros(1, 1, d_model))
        # 可学习位置编码, 长度 = patch 数 + 1 (CLS 也需要位置)
        self.pos_emb = nn.Parameter(torch.zeros(1, n_patches + 1, d_model))
        nn.init.trunc_normal_(self.cls_token, std=0.02)
        nn.init.trunc_normal_(self.pos_emb, std=0.02)

        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, num_classes)

    def forward(self, x, return_attn=False):
        B = x.size(0)

        x = self.patch_embed(x)                              # (B, 196, 768)
        cls = self.cls_token.expand(B, -1, -1)               # (B, 1, 768)
        x = torch.cat([cls, x], dim=1)                       # (B, 197, 768)
        x = x + self.pos_emb

        attn_maps = []
        for blk in self.blocks:
            x, a = blk(x)                                    # 无 mask, 全可见
            if return_attn:
                attn_maps.append(a)

        x = self.ln_f(x)
        logits = self.head(x[:, 0])                          # 只取 CLS 位置
        return (logits, attn_maps) if return_attn else logits


if __name__ == "__main__":
    torch.manual_seed(0)

    # 小一号的配置, 便于快速验证
    model = ViT(img_size=224, patch_size=16, num_classes=10,
                d_model=192, num_heads=3, d_ff=768, num_layers=4)

    x = torch.randn(2, 3, 224, 224)

    # 逐步看形状
    pe = model.patch_embed
    print(f"输入图像       {tuple(x.shape)}")
    print(f"卷积之后       {tuple(pe.proj(x).shape)}      <- (B, d_model, 14, 14)")
    print(f"patch token    {tuple(pe(x).shape)}       <- {pe.num_patches} 个 patch")

    logits, maps = model(x, return_attn=True)
    print(f"加 CLS 之后    (2, {pe.num_patches + 1}, 192)")
    print(f"注意力权重     {tuple(maps[0].shape)}  <- 197x197 方阵")
    print(f"输出 logits    {tuple(logits.shape)}")

    n = sum(p.numel() for p in model.parameters())
    print(f"\n参数量 {n:,}")
    print("\n注意: 中间的 Transformer Block 和 Day 3 写的完全一样, 一行没改。")
    print("ViT 的贡献不是新结构, 而是证明了图像切 patch 后标准 Transformer 直接可用。")