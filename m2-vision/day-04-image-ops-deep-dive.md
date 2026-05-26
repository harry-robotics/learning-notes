# Day 4: 图像基础操作深度补课 (ROI / 灰度 / 二值化 / 多图显示)

> 学习日期: 5.26
> 核心: 不进新内容, 把 Day 3 学过但没透彻的几个点彻底搞清楚
> 状态: 巩固日, 配合期末复习节奏

---

## 1. ROI 切片 img[y1:y2, x1:x2] 【必背 ⭐】

### 1.1 ROI 是什么
- ROI = Region of Interest, 感兴趣区域
- 类比: 全班合照里只截"中间那个人"的脸

### 1.2 切片语法
```python
roi = img[y1:y2, x1:x2]
```

### 1.3 核心坑: 先 y 后 x【必背】
- NumPy 数组第一维是行 → 必须先写 y (行索引)
- 跟数学直觉 [x, y] 相反

### 1.4 图像坐标系图示
```
  (0,0) ──────→ x (列)
    │
    │   ← 原点在左上角
    ↓     y 朝下增长
   y (行)
```

### 1.5 切片实例 (以 480×640 图像为例)
| 切片 | 含义 | 结果 shape |
|---|---|---|
| img[0:100, 0:100] | 左上角 100×100 | (100, 100, 3) |
| img[-100:, -100:] | 右下角 100×100 | (100, 100, 3) |
| img[200:, :] | y=200 以下所有 | (280, 640, 3) |
| img[:, :320] | 左半边 | (480, 320, 3) |

### 1.6 应用场景
- 智能车: 圈出"前方道路"区域做处理
- 车牌识别: 把车牌区域切出来
- 目标跟踪: 每帧切出 ROI

---

## 2. 灰度 vs 二值化 (彻底区分) 【必背 ⭐】

### 2.1 三种图像状态对比
| 类型 | 像素值 | 像素种类 | shape | 视觉 |
|---|---|---|---|---|
| 彩色图 (BGR) | 每通道 0-255 | 256³ ≈ 1670万 | (H, W, 3) | 全彩 |
| **灰度图** | 0-255 单通道 | **256 种** | (H, W) | **256 级明暗渐变** |
| **二值化** | 只有 0 或 255 | **2 种** | (H, W) | **只有纯黑纯白, 无中间灰** |

### 2.2 "灰度图没有颜色" 准确含义
- 准确说法: **只保留亮度, 丢弃色相**
- 不准确说法: "灰度图只有黑白" ❌ (它有 256 级明暗)
- 类比: 老式黑白照片, 能看清明暗轮廓, 看不出红绿蓝

### 2.3 灰度像素值含义
| 像素值 | 视觉 |
|---|---|
| 0 | 纯黑 |
| 50 | 深灰 |
| 128 | 中灰 |
| 200 | 浅灰 |
| 255 | 纯白 |

### 2.4 二值化的"强制压缩"本质
原灰度 → 二值化 (阈值 128):
```
[50, 100, 150, 200] → [0, 0, 255, 255]
深灰 中灰 浅灰 亮灰    黑 黑 白 白
```

### 2.5 cvtColor 转灰度
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# shape: (H, W, 3) → (H, W)  通道维消失!
```

### 2.6 二值化两种写法
```python
# 写法 1: NumPy 布尔索引
binary = (gray > 128).astype(np.uint8) * 255

# 写法 2: OpenCV 函数
ret, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
```

### 2.7 使用场景对比
| 任务 | 用什么 | 原因 |
|---|---|---|
| 显示给人看 | 彩色图 | 视觉舒适 |
| 边缘检测 | 灰度图 | 不需颜色, 省 2/3 计算 |
| 特征点提取 | 灰度图 | 同上 |
| **赛道循迹** | **二值化** | 只需 "赛道 vs 地面" 两类 |
| 车牌识别 | 二值化 | 字符黑底白 |

### 2.8 核心认知【必背】
信息量逐级减少, 处理速度逐级加快:
- 彩色 (3 通道) → 灰度 (1 通道, 256 级) → 二值 (1 通道, 2 级)

---

## 3. OpenCV 基础三件套 (彻底讲透) 【必背 ⭐】

任何 OpenCV 程序的工作流骨架: 读 → 处理 → 显示 → 存

### 3.1 读: cv2.imread()
```python
img = cv2.imread('photo.jpg')
```
- 返回: NumPy 数组 (BGR 顺序, dtype=uint8)
- 路径错返回 None 不报错, 必须检查:
```python
if img is None:
    print("文件读取失败!")
    exit()
```

### 3.2 显示: plt.imshow + cvtColor

**为什么不用 cv2.imshow?**
- 它需要 GUI 窗口
- WSL / Jupyter 没原生窗口 → 卡死

**正确显示规则**:
| 图像类型 | 写法 |
|---|---|
| OpenCV 彩色图 (BGR) | plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) |
| 灰度图 | plt.imshow(gray, cmap='gray') |
| 二值化图 | plt.imshow(binary, cmap='gray') |

**为什么转 RGB?**
- OpenCV 历史遗留用 BGR
- Matplotlib 用 RGB
- 不转的话蓝变红、红变蓝

**为什么灰度要 cmap='gray'?**
- 不加默认彩虹色板, 灰度图变绿紫渐变 → 视觉灾难

### 3.3 存: cv2.imwrite()
```python
cv2.imwrite('output.png', img)
```
- 扩展名决定格式: .jpg / .png / .bmp
- 保存的也是 BGR
- 若之前转过 RGB, 存前要转回 BGR

---

## 4. Matplotlib 多图对比 (CV 调试标配) 【必懂】

### 4.1 标准模板
```python
fig, axes = plt.subplots(行数, 列数, figsize=(宽, 高))
axes[i].imshow(...)
axes[i].set_title('...')
plt.show()
```

### 4.2 plt.subplots() 参数
- 第 1 参数: 行数
- 第 2 参数: 列数
- figsize: 画布大小 (宽英寸, 高英寸)
- 返回 fig (画布对象) 和 axes (子图数组)

### 4.3 axes 是什么?
- 本质: NumPy 数组, 装着多个子图对象
- 单行单列 → axes 是 1D, 用 axes[i]
- 多行多列 → axes 是 2D, 用 axes[i, j]

### 4.4 一个常见混淆: axes vs axis
| 容易混的 | 含义 |
|---|---|
| axes[0/1/2] | **Matplotlib 子图们** (axis 的复数) |
| np.sum(M, axis=0/1) | **NumPy 聚合方向** |

两者完全不相关, 名字相近巧合而已。

### 4.5 plt.show() 的作用
- 之前的 imshow / set_title 都是 "在画布上画"
- plt.show() 触发 "把画好的画布渲染出来"
- 类比: 写 PPT 最后点"播放"

### 4.6 完整对比示例 (Day 3 实战代码)
```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
axes[0].set_title('原图')
axes[1].imshow(gray, cmap='gray')
axes[1].set_title('灰度')
axes[2].imshow(binary, cmap='gray')
axes[2].set_title('二值化')
plt.show()
```

效果: 一行 3 张并排小图, 上方有标题, 用于对比处理前后。

### 4.7 多行多列写法预告
```python
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
# axes.shape = (2, 3)
axes[0, 0].imshow(img1)
axes[1, 2].imshow(img6)
```

---

## 5. 嵌套函数调用 (从内往外读) 【必懂】

### 5.1 嵌套写法
```python
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
```

### 5.2 等价的展开写法
```python
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
```

两种完全等价, 嵌套更紧凑, 展开更清晰。

### 5.3 阅读规则
**从最内层括号开始执行**, 一层一层往外。

---

## 6. 本日核心判断标准 【必背】

| 看到什么 | 知道是什么 |
|---|---|
| img[y1:y2, x1:x2] | 切 ROI, **y 在前 x 在后** |
| (H, W, 3) → (H, W) | 转灰度后通道维消失 |
| 像素值 0 或 255 | 二值化, 只有 2 种 |
| plt.imshow(img) 不转 RGB | ❌ 颜色会反 |
| plt.imshow(gray) 不加 cmap | ❌ 变彩虹色 |
| cv2.imshow() 在 Jupyter | ❌ 会卡死 |
| AI 写 img[x, y] | ❌ 顺序反 |
| 转灰度后 img[:, :, 0] | ❌ 灰度图没通道维, 会报错 |

---

## 7. 易错点汇总

| 坑 | 现象 | 修复 |
|---|---|---|
| ROI 切片用 [x, y] | 切出来位置不对 | 改 [y, x] |
| 灰度图当彩色处理 | shape 报错 | 检查 shape 是 2 维还是 3 维 |
| BGR 不转 RGB 显示 | 颜色反 | 加 cvtColor |
| 灰度图不加 cmap | 变彩虹色 | 加 cmap='gray' |
| 在 Jupyter 用 cv2.imshow | 卡死 | 改 plt.imshow |
| imread 不检查返回值 | None 报错 | if img is None |
| uint8 直接加运算 | 溢出回绕 | astype int32 再算 |

---

## 8. 我的疑问 / 心得 / 踩过的坑

<!-- 自己填:
- ROI 切片 [y, x] 顺序你卡了多久才记住?
- 第一次看到灰度图显示, 视觉感受?
- "灰度有 256 级渐变" 和 "二值化只有 2 级" 这个区分用了什么类比帮自己记?
- 嵌套函数读起来还顺吗?
- 哪个点是 AI 写代码时你能立刻指出错误的?
-->
- 一直都是在用OpenCV(BGR)处理图像，只是借用Matplotlib工具显示图像
- 彩色（256^3）vs 灰度（256）只有亮度 vs 二值化（2）只有黑白