# Phase 0 · Day 2: Hough 提直线 + 分离左右车道 + 看它崩

> 学习日期: <2026.7.30>
>
> 核心: 从边缘 → 车道线段 → 左右两条车道线 → 画回原图, 并亲眼看传统 CV 崩掉。

---

## 0. 今日复习 (艾宾浩斯 · Day1 +1天)

- 盖住答案, 默答 Day1「必背」4 条 + 思考题 Q1-Q5。
- 重点自测: `bitwise_and` 白区/黑区分别怎样? 为什么用梯形? 答不出的回看 Day1。

我的复习情况:都会
-

---

## 1. 我今天要做什么

昨天我把边缘限制在了道路区域 (`masked_edges`)。今天要:
1. 从这些边缘里**提取直线** (Hough)
2. 把零碎线段**归并成左、右两条车道线** (斜率分组 + 拟合)
3. **画回原图**
4. 换一张有阴影/弯道的图, **看它崩**, 体会传统 CV 的天花板

---

## 2. 复用: Hough 提直线 (Day7 已会)

```python
lines = cv2.HoughLinesP(masked_edges, 1, np.pi/180,
                        threshold=50, minLineLength=50, maxLineGap=100)
```
- 输入是昨天的 `masked_edges`, 输出一堆线段 `(x1,y1,x2,y2)`。
- 每条线取 `line[0]`; `lines` 可能是 None (Day7 的坑)。

---

## 3. 新技能①: 用斜率分离左/右车道 ⭐

### 3.1 斜率的直觉

- 斜率 = (y2 - y1) / (x2 - x1), 表示线段往哪个方向斜。
- **图像 y 轴朝下**, 所以: 左车道从左下往右上 → 斜率**负**; 右车道从右下往左上 → 斜率**正**。
- 坑: 图像 y 朝下, 正负和数学课相反。

### 3.2 分组代码

```python
left_lines = []
right_lines = []

for line in lines:
    x1, y1, x2, y2 = line[0]
    if x2 - x1 == 0:          # 竖直线, 斜率无穷大, 跳过防除零
        continue
    slope = (y2 - y1) / (x2 - x1)
    if slope < -0.5:          # 负 → 左车道
        left_lines.append(line[0])
    elif slope > 0.5:         # 正 → 右车道
        right_lines.append(line[0])
    # |slope| < 0.5 接近水平, 多是噪声, 丢弃
```

- 门槛 ±0.5: 车道线是明显倾斜的, 斜率接近 0 的(水平线)通常是裂缝/阴影/护栏, 过滤掉。
- `x2-x1==0` 跳过: 竖直线算斜率会除零报错。

---

## 4. 新技能②: 多条线段拟合成一条 ⭐

一侧车道现在是一堆短线段, 要拟合成一条完整直线。

```python
def average_line(lines_group, img_height):
    if len(lines_group) == 0:
        return None
    xs, ys = [], []
    for x1, y1, x2, y2 in lines_group:
        xs += [x1, x2]
        ys += [y1, y2]
    k, b = np.polyfit(xs, ys, 1)      # 拟合直线 y = k*x + b
    y1 = img_height                    # 从图像底部
    y2 = int(img_height * 0.6)         # 到画面中部
    x1 = int((y1 - b) / k)             # 由 y=kx+b 反解 x
    x2 = int((y2 - b) / k)
    return (x1, y1, x2, y2)
```

- **`np.polyfit(xs, ys, 1)`**: 最小二乘拟合。第三个参数 `1` = 用直线拟合, 返回斜率 k、截距 b。改成 `2` 就是抛物线(弯道会用到)。
- **反解 x = (y-b)/k**: 我指定要画的 y 范围(底部→中部), 用直线方程算出对应 x, 让两条车道线长度一致、规整。

---

## 5. 新技能③: 画回原图 + 半透明叠加

```python
def draw_lanes(img, left, right):
    line_img = np.zeros_like(img)      # 同大小黑布(三通道, 画彩色线)
    for lane in [left, right]:
        if lane is not None:
            x1, y1, x2, y2 = lane
            cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 8)
    result = cv2.addWeighted(img, 0.8, line_img, 1.0, 0)
    return result
```

- **`cv2.addWeighted(img1, α, img2, β, γ)`**: 按权重混合, `结果 = img1*α + img2*β + γ`。
- 这里原图占 0.8、车道线图占 1.0, 效果是半透明绿线覆盖在路面上, 线和路都看得见。γ=0。

---

## 6. 组装 + 见证崩塌

```python
h_img = img.shape[0]
left = average_line(left_lines, h_img)
right = average_line(right_lines, h_img)
result = draw_lanes(img, left, right)

plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('Lane Detection Result')
plt.axis('off')
plt.show()
```

**关键动作**: 跑通后, 换一张有**阴影 / 弯道 / 磨损车道线**的图重跑。观察它怎么失败(线画歪/画飞/检测不到)。这个失败就是我理解"为什么需要深度学习"的第一手证据。

我看到的崩塌现象:
-

---
## 补充: 代码逐行理解 (我自己的备注)

### 关键概念: 函数的"参数"是占位符

- **定义函数** = 写菜谱: `def average_line(lines_group, img_height)` 里的 `lines_group`、`img_height` 只是**占位名**, 不代表任何真实数据。
- **调用函数** = 真做饭: `left = average_line(left_lines, h_img)` 这一刻, 才把真实的 `left_lines` 塞进占位符 `lines_group`。
- 所以 `left`/`right` 不是凭空来的: 它们是**调用函数后, return 的结果被等号存下来**。

### Python 语法备忘

- `a = []`: 建一个空列表(清单)。
- `a.append(x)`: 往列表末尾加一项。
- `a += [x, y]`: 把 x、y 接到列表 a 末尾。
- `x1, y1, x2, y2 = line[0]`: 解包 —— 一次性把 4 个数拆给 4 个变量。
- `continue`: 跳过本次循环, 直接进入下一次(这里用来跳过竖直线防除零)。
- `if lane is not None:`: 判断这条线存在才处理(某侧没检测到线时会是 None)。

### 三段核心代码在干嘛 (一句话版)

- **斜率分组**: 按斜率正负, 把杂乱线段分进"左""右"两个清单, 扔掉竖直线和水平噪声。
- **average_line**: 把一侧的短线段拆成散点 → `np.polyfit(xs, ys, 1)` 拟合成一条直线 → 指定上下端 y、反解 x → 返回一条完整车道线。
- **draw_lanes**: 另建黑布画绿线 → `cv2.addWeighted` 把线半透明叠回原图。

### 关键函数备忘

- `np.polyfit(xs, ys, 1)`: 用直线拟合散点, 返回斜率 k、截距 b。参数 `1`=直线, `2`=抛物线(弯道会用)。
- `cv2.addWeighted(img1, α, img2, β, γ)`: 混合两图, 结果 = img1×α + img2×β + γ。用来做半透明叠加。
- `cv2.line(图, 起点, 终点, 颜色, 粗细)`: 在图上画线段。

---

## 7. 本日术语 (记进 glossary.md)

| English | 中文 |
|---|---|
| slope | 斜率 |
| least squares fitting | 最小二乘拟合 |
| polynomial fit | 多项式拟合 |
| overlay / blend | 叠加 / 混合 |
| weighted sum | 加权求和 |

---

## 8. 思考题 (从易到难)

### Q1 (易)
为什么左车道线的斜率是负的? (提示: 图像 y 轴方向)

我的答案:y轴向下为正方向

### Q2 (中)
分组时为什么要过滤掉斜率绝对值小于 0.5 的线段?

我的答案:斜率接近 0 的线段是接近水平的线,而真正的车道线在透视下都是明显倾斜的。接近水平的线通常是干扰——路面裂缝、阴影边界、护栏横条、远处的地平线等。过滤掉 |斜率|<0.5 的,就能把这些噪声排除,只保留像车道线的倾斜线段,避免它们污染后面的拟合

### Q3 (中)
`np.polyfit(xs, ys, 1)` 里的 `1` 改成 `2` 会发生什么? 什么时候我会想用 2?

我的答案:1 是用一次多项式(直线)拟合,2 是用二次多项式(抛物线)拟合。改成 2 后,拟合出来的是一条能弯曲的曲线。当路是弯道时就想用 2(甚至更高次),因为直线拟合不了曲线

### Q4 (难·判断 bug)
如果去掉 `if x2 - x1 == 0: continue`, 可能会怎样?

我的答案:会有除零风险。斜率算式是 (y2-y1)/(x2-x1),当线段是竖直线时 x2-x1==0,除以 0 会让程序报错(ZeroDivisionError)崩溃。

### Q5 (难·思辨)
换一张带阴影的图后车道线检测崩了。用一两句话说清: 传统 CV 卡在哪一步、为什么深度学习能解决?

参考答案:传统 CV 卡在它是一套人手工设计、写死的规则——固定的 Canny 阈值、固定的 ROI 梯形、"车道线一定是明显倾斜的直线、左负右正"这些假设。一旦真实场景不满足这些假设(弯道不是直线、阴影让阈值失效、光照变化),整套规则就失效,而且没法靠调几个参数覆盖所有情况。深度学习能解决,是因为它不靠人写死规则,而是从大量各种场景(直路、弯道、阴影、夜晚……)的数据里,自己学出"什么是车道线"的判据,从而能泛化到没手动处理过的新情况。

---

## 9. 我的必背

| # | 内容 |
|---|---|
| 1 | 图像 y 轴朝下 → 左车道斜率负、右车道斜率正 |
| 2 | 算斜率前先防除零 (x2-x1==0 跳过) |
| 3 | `np.polyfit(xs,ys,1)` 拟合直线, 返回斜率 k 和截距 b |
| 4 | `cv2.addWeighted` 做半透明叠加 |

---

## 10. 我踩的坑 / 易错点

| 坑 | 后果 | 修复 |
|---|---|---|
| 斜率正负判反 | 左右车道分错组 | 图像 y 朝下, 和数学相反 |
| 没防除零 | 竖直线段报错 | `if x2-x1==0: continue` |
| polyfit 传入空列表 | 某侧没线时报错 | 先判断 `len==0` 返回 None |
| addWeighted 两图尺寸/通道不一致 | 报错 | line_img 用 `zeros_like(img)` |

---

## 11. 我的心得

传统cv不仅内容多且杂，得到的效果还是建立在必须非常符合模型的图片基础上，因此在物理世界的应用绝对很有限，这就让我更加迫不及待进入Deep Learning的学习中了。


---

*Last updated: <2026.7.30>*