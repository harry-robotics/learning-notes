# Phase 0 · Day 1: 传统 CV 车道线检测项目 (一)

> 学习日期: <2026.7.28>
>
> 核心: 复用 Day1-7 流水线 + 新技能【多边形 ROI 掩膜 + 位运算】
>
> 我的定位: 桥梁项目第一天。今天要做到"只保留道路区域的边缘", 为明天用 Hough 提直线做准备。

---

## 0. 我在建什么 / 为什么建

- **目标**: 输入一张道路图, 输出画着车道线的图。这是我第一个完整项目。
- **我做它的三个理由**:
  1. 把散的 Day1-7 拧成一个能跑的东西 (巩固)
  2. 亲眼看它在阴影/弯道上崩掉, 体会传统 CV 的天花板, 想清楚为什么要上深度学习
  3. 一个能写进简历/竞赛/套磁的作品
- **完整流水线** (今天做前 4 步):

```
读图 → 灰度 → 高斯 → Canny → 【ROI 掩膜】→ (明天) Hough → 平均左右车道线 → 画回原图
                              ↑ 今天的新东西
```

---

## 1. 复用: 流水线前三步 (已会, 快速过)

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('road.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)      # 转灰度
blur = cv2.GaussianBlur(gray, (5, 5), 0)          # 高斯降噪
edges = cv2.Canny(blur, 50, 150)                  # 边缘检测
```

- 这三步是 Day 3-6 的内容, 不再展开。
- 记住: `edges` 是**单通道**边缘图, shape 是 (H, W) —— 第 2 节要用到这点。

---

## 2. 新技能: 多边形 ROI 掩膜 ⭐⭐

### 2.1 为什么要做

- Canny 会把**整张图**的边缘都找出来 —— 天空、路边的树、旁边车道、护栏, 全是边缘。但我只关心**正前方这条路**。
- 用 Day 4 的矩形切片 `img[y1:y2, x1:x2]` 不行: 因为透视关系, 摄像头里的路面是一个**梯形**(近宽远窄), 矩形框不住, 还会框进没用的东西。
- 所以需要一个能框住**任意多边形(梯形)**的工具 —— 这就是 ROI 掩膜 (mask)。

### 2.2 掩膜的思想

一句话: 做一张同样大小的"黑白模板", 想保留的区域涂白(255)、其余全黑(0), 再和边缘图叠加, 只有白区的边缘被留下。

分三步, 每步一个新函数。

### 2.3 第一步: 造一张全黑画布 `np.zeros_like`

```python
mask = np.zeros_like(edges)
```
- `np.zeros_like(edges)`: 造一个和 `edges` 形状、类型都一样、但全是 0 的数组。
- **我最容易踩的坑**: 要用 `zeros_like(edges)` 而不是 `zeros_like(img)`。因为 `edges` 是单通道 (H,W), `img` 是三通道 (H,W,3); 掩膜必须和要叠加的对象**通道一致**, 否则第三步会报错。

### 2.4 第二步: 把梯形涂白 `cv2.fillPoly`

```python
h, w = edges.shape
vertices = np.array([[
    (int(0.1 * w), h),              # 左下
    (int(0.45 * w), int(0.6 * h)),  # 左上
    (int(0.55 * w), int(0.6 * h)),  # 右上
    (int(0.9 * w), h)               # 右下
]], dtype=np.int32)

cv2.fillPoly(mask, vertices, 255)
```
- `cv2.fillPoly(画布, 顶点, 颜色)`: 把顶点围成的多边形填成指定颜色 (255=白)。
- **顶点用比例 (0.1*w 这种) 定义**, 不写死像素 —— 换一张不同尺寸的图也能自适应。
- 两个坑: 顶点要 `dtype=np.int32` (坐标是整数); `vertices` 外面有**两层括号** `[[...]]` (fillPoly 收的是"一组多边形")。

### 2.5 第三步: 叠加 `cv2.bitwise_and`

```python
masked_edges = cv2.bitwise_and(edges, mask)
```

**我要真懂 `bitwise_and`(按位与), 不是抄 API**:
- 它对**每个像素**做按位与。边缘图和掩膜里像素非 0 即 255。
- 255 的二进制是 `11111111`, 0 是 `00000000`。按位与: 两位都为 1 才得 1。
- 于是: `255 AND 255 = 255`(白区边缘 → 原样保留); `任何值 AND 0 = 0`(黑区边缘 → 清零)。
- **净效果**: 掩膜白的地方边缘穿过去, 黑的地方边缘被抹掉 → 只剩梯形道路区域内的边缘。
- 记忆钩子: 掩膜像一张**镂空的纸**盖在边缘图上, 只有镂空(白)处能看到下面的边缘。

### 2.6 看效果

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(edges, cmap='gray');        axes[0].set_title('1. Canny edges')
axes[1].imshow(mask, cmap='gray');         axes[1].set_title('2. ROI mask')
axes[2].imshow(masked_edges, cmap='gray'); axes[2].set_title('3. Masked edges')
for ax in axes:
    ax.axis('off')
plt.show()
```
预期: 第 1 张满图边缘 → 第 2 张一个白梯形 → 第 3 张只剩梯形内的边缘。

---

## 3. 本日术语 (记进 glossary.md)

| English | 中文 |
|---|---|
| mask | 掩膜 |
| region of interest (ROI) | 感兴趣区域 |
| bitwise AND | 按位与 |
| polygon | 多边形 |
| vertices | 顶点 |
| perspective | 透视 |

---

## 4. 思考题 (从易到难)

### Q1 (易)
车道线检测为什么要先做 ROI 掩膜? 不做会怎样?

我的答案:边缘检测出来的不是所有都要，只要车道线。

### Q2 (中)
`bitwise_and` 里, 掩膜是黑色(0)的地方, 边缘图会变成什么? 用"按位与"规则解释为什么。

我的答案:变成黑色。任何值AND 0 = 0.

### Q3 (中)
为什么 ROI 用**梯形**而不是**矩形**? 和摄像头的什么特性有关?

我的答案:因为透视（perspective)

### Q4 (难·判断 bug)
下面代码会报错, 为什么? (提示: `img` 和 `edges` 的 shape 差别)
```python
mask = np.zeros_like(img)          # 这里是 img
cv2.fillPoly(mask, vertices, 255)
masked = cv2.bitwise_and(edges, mask)
```

我的答案:因为 img 是三通道 (H,W,3),edges 是单通道 (H,W)。这样 mask 是三通道,而 bitwise_and(edges, mask) 要求两个输入尺寸/通道一致

### Q5 (难·迁移)
如果摄像头位置抬高了, 拍到的路面区域整体上移, 我该怎么调 `vertices`?

我的答案:路面在画面里整体上移,意味着梯形要往上挪。思路是把顶点的 y 值整体调小(y 越小越靠上),尤其顶边那两个点(远处)往上收;必要时底边的 y 也从 h 稍微抬一点。核心是让梯形重新罩住上移后的路面区域,再跑一次看白梯形对不对得上。
---

## 5. 我的必背

| # | 内容 |
|---|---|
| 1 | ROI 掩膜三步: `np.zeros_like` 造黑布 → `fillPoly` 涂白 → `bitwise_and` 叠加 |
| 2 | 掩膜必须和目标**通道一致** (边缘图单通道 → 用 `zeros_like(edges)`) |
| 3 | `bitwise_and`: 白(255)处保留, 黑(0)处清零 |
| 4 | 顶点 `dtype=np.int32`, 且外面两层括号 `[[...]]` |

---

## 6. 我踩的坑 / 易错点

| 坑 | 后果 | 修复 |
|---|---|---|
| `zeros_like(img)` 造三通道掩膜 | bitwise_and shape 不匹配报错 | 用 `zeros_like(edges)` |
| vertices 用 float | fillPoly 报错 | `dtype=np.int32` |
| vertices 少一层括号 | fillPoly 报错 | `[[ (x,y), ... ]]` |
| 顶点写死像素 | 换图就不对 | 用 w/h 比例定义 |

---
