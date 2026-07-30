# Glossary — 我的专业术语表

| English | 中文 | 备注 |
|---|---|---|
| mask | 掩膜 | 黑白模板,白留黑删 |
| region of interest (ROI) | 感兴趣区域 | 只处理关心的区域 |
| bitwise AND | 按位与 | 白色通行证,黑色封条 |
| polygon | 多边形 | |
| vertices | 顶点 | (x,y) 顺序,原点左上 |
| perspective | 透视 | 近宽远窄,所以路面是梯形 |
|---|---|
| slope | 斜率 |
| least squares fitting | 最小二乘拟合 |
| polynomial fit | 多项式拟合 |
| overlay / blend | 叠加 / 混合 |
| weighted sum | 加权求和 |
| English | 中文 | 备注 |
|---|---|---|
| feature point / keypoint | 特征点 | 辨识度高、可重复识别的小地方,通常是角点 |
| corner | 角点 | 往任何方向移动都变,信息最丰富,最独特 |
| detector | 检测器 | 负责找出图里哪些位置是特征点 |
| descriptor | 描述子 | 给每个特征点算的"数字指纹",用于跨图比对 |
| feature matching | 特征匹配 | 靠描述子在两张图里找出同一个点 |
| ORB | ORB | 免费、快的经典特征方法,机器人/SLAM 常用 |
| SIFT | SIFT | 经典特征方法,效果好但曾有专利 |
| robustness | 鲁棒性 | 对旋转/尺度/光照等变化的抗干扰能力 |
| Hamming distance | 汉明距离 | ORB 描述子比对用的距离度量(NORM_HAMMING) |


