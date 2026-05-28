# Day 3: NumPy 收尾 + OpenCV 入门

> 学习日期:5.25
> 核心: 布尔索引 + uint8 坑 + OpenCV 三件套 + BGR vs RGB

## 1. NumPy 图像相关高频技巧
### 布尔索引 (Mask)
- 用法:
  > `mask = img > 80`(找出大于80的像素位置)
> `print(img[mask])`(用mask提取符合的像素)
> `img([mask])=255`(用mask修改符合的像素)
- 用途：图像二值化，阈值分割，目标检测过滤

### uint8 溢出坑【必背 ⭐】
- 问题:OpenCV里默认就是unit8类型数据（0-255），运算时可能会溢出
- 解决:算之前先转int32,算完再转回unit8
  
```python 
img_int = img.astype(np.int32)
result = img_int + 100         # [300, 320, 340]
result = np.clip(result, 0, 255)  # 限制在 0-255
result = result.astype(np.uint8)  # 转回 uint8
```

### 拼接函数
- concatenate / stack / column_stack 用时查

### BGR vs RGB 历史坑【必背】
- OpenCV 默认 BGR 顺序
- Matplotlib / PyTorch / 大部分库 用 RGB
- 显示前必须 cvtColor(img, COLOR_BGR2RGB)

## 2. OpenCV 环境
- 安装: pip install opencv-python
- BGR vs RGB 坑【必背 ⭐】
  

## 3. OpenCV 三件套【必背 ⭐】
- 读: cv2.imread()
- 显示: plt.imshow (Jupyter 推荐)
- 保存: cv2.imwrite()

## 4. 图像基础操作

### 4.1 ROI 切片 img[y1:y2, x1:x2]【必背】
- 顺序: 先 y 后 x (反直觉!)
- 原因: NumPy shape 是 (H, W, C), 第一维是行
- 应用: 圈出感兴趣区域单独处理

### 4.2 转灰度 cv2.cvtColor【必背】
- 用法: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
- shape 变化: (H, W, 3) → (H, W) 通道维消失
- 用途: 简化数据, 加速算法 (边缘检测/特征点都用灰度)

### 4.3 二值化【必背】
- 简单写法: (gray > T).astype(uint8) * 255
- 标准写法: cv2.threshold(gray, T, 255, cv2.THRESH_BINARY)
- 用途: 突出形状, 分割目标和背景, 智能车循迹
## 5. 思考题闭环
### Q1: 暗像素置黑
### Q2: shape 推理

## 6. 必背【追加 3 条】
1. OpenCV 用 BGR 不是 RGB
2. uint8 运算会溢出, 先 astype(int) 再算
3. 图像 shape (H, W, C), 切片用 [y, x] 不是 [x, y]

## 7. 我的心得
<!-- 自己填 -->
- unit8 的坑小心再小心
- 大部分都是RGB,但是OpenCV是BGR,两者转换时要注意
- ROI 切片顺序: 先 y 后 x

*Last updated: 2026-5-25*