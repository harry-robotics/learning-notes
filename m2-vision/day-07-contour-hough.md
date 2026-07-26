# Day 7: 轮廓检测 + 霍夫直线

> 学习日期:5.30
> 核心: 轮廓 vs 边缘 + findContours + 霍夫投票 + 循迹链路

---

## 1. 什么是轮廓【必懂】
- 边缘是"散点", 轮廓是"连续封闭曲线"
- 关键: 边缘是"图像", 轮廓是"坐标点列表"
- 坐标能计算 → 这是轮廓的价值

## 2. 轮廓 vs 边缘【必背 ⭐】
| 维度 | 边缘 | 轮廓 |
|---|---|---|
| 是什么 | 亮度突变点 | 连续封闭曲线 |
| 数据形式 | 黑白图像 | 坐标点列表 |
| 谁产生 | Canny | findContours |
| 能干什么 | 看 | 算面积/中心/外接框 |

## 3. findContours 用法【必懂】
```python
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
- 输入必须是二值化图
- RETR_EXTERNAL = 只要最外层
- CHAIN_APPROX_SIMPLE = 直线只存端点 (省内存)
- 返回 contours 列表, 每个元素是一个轮廓的坐标点数组

## 4. 轮廓能算什么【必懂】
- cv2.contourArea(cnt): 面积 → 用于过滤噪声
- cv2.arcLength(cnt, True): 周长
- cv2.boundingRect(cnt): 外接矩形 → 用于框出物体

## 5. 霍夫变换【必背 ⭐】
- 本质: 投票选直线
- 每个边缘点投票, 票数高的方向 = 真实直线
- 用途: 从散乱边缘里找出直线
- 数学跳过, 调参即可

## 6. HoughLinesP 用法【必懂】
```python
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50,
                        minLineLength=50, maxLineGap=10)
```
- edges: Canny 边缘图
- 1: 距离精度 1 像素
- np.pi/180: 角度精度 1 度
- threshold: 投票阈值, 越高越严格
- minLineLength: 最短线长
- maxLineGap: 容忍线段断裂的距离
- 返回 lines, 每条线 [x1,y1,x2,y2]

## 7. 代码里的新东西
### img.copy()
- NumPy 直接赋值是引用 (共享数据)
- .copy() 创建独立副本
- 用途: 在副本上画图, 保留原图

### if lines is not None:
- 没检测到时返回 None 不是空列表
- 必须先判断, 否则 for 循环报错
- 防御性编程习惯

## 8. 实验室物体检测链路【必背 ⭐⭐⭐】(主线!)
读图 → 灰度 → 高斯 → 二值化 → findContours → 过滤面积 → 算外接框

应用: SLAM 标志识别 / 物体检测 / 深度学习后处理

## 9. 智能车循迹链路【必懂】(赛事用)
读图 → 灰度 → 高斯 → Canny → 霍夫直线 → 算中线 → PID → 电机

## 10. 必背【追加 2 条】
1. 边缘是图像, 轮廓是坐标点列表 (能计算)
2. 智能车循迹链路: 灰度→高斯→Canny→霍夫→PID→电机

## 11. 易错点
| 坑 | 后果 | 修复 |
|---|---|---|
| findContours 喂灰度图 | 报错 | 先二值化 |
| 霍夫 threshold 太低 | 一堆杂线 | 提高阈值 |
| lines 是 None 没判断 | for 循环报错 | 加 if not None |
| 直接在原图画线 | 原图被改 | 用 img.copy() |

## 12. 我的疑问 / 心得
<!-- 自己填:
- 边缘 vs 轮廓的区分理解了吗?
- 霍夫"投票"这个比喻能帮你记住吗?
- 智能车循迹链路这条线串起来了 M1 和 M2, 你看出价值了吗?
-->