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
|---|---|---|
| model | 模型 | 用来做预测的函数形式，决定有哪些参数 |
| neural network | 神经网络 | 一堆神经元分层连接；本质是可调参数的函数 |
| neuron | 神经元 | 加权求和 + 偏置，再过激活函数 |
| weight (w) | 权重 | 决定某个输入有多重要的参数，训练中更新 |
| bias (b) | 偏置 | 整体平移量，类比一次函数的截距 |
| parameter | 参数 | 模型要"学"的量（w、b），训练中会变 |
| input / feature | 输入 / 特征 | 外界给定的 x，训练中不改 |
| linear regression | 线性回归 | ŷ = w·x + b，最简单的单层神经网络 |
| activation function | 激活函数 | 对加权和做的变换；线性回归用恒等激活 |
| identity activation | 恒等激活 | 原样输出、什么都不做 |
| forward pass | 前向传播 | 由输入算出预测 ŷ 的过程 |
| prediction (ŷ) | 预测值 | 模型的输出，ŷ 读作 "y-hat" |
| loss function | 损失函数 | 量化"预测有多差"的函数，越小越好 |
| MSE (mean squared error) | 均方误差 | L = (1/n)Σ(ŷ−y)²，线性回归常用损失 |
| broadcasting | 广播 | NumPy 自动扩展形状做逐元素运算 |
| vectorization | 向量化 | 用数组整体运算代替 for 循环，效率高 |
|---|---|---|
| optimization | 优化 | 调参数使损失最小的过程（训练的核心） |
| gradient | 梯度 | 损失对参数的导数；指向"损失上升最快"方向 |
| derivative | 导数 | 函数在某点的变化率 / 斜率 |
| gradient descent | 梯度下降 | 沿负梯度方向更新参数，让损失下降 |
| update rule | 更新公式 | w := w − lr · ∂L/∂w |
| learning rate (lr) | 学习率 | 每步走多大；太大→震荡/发散，太小→太慢 |
| hyperparameter | 超参数 | 人为设定、模型不自学的量（如 lr、epochs） |
| epoch | 轮次 | 把全部训练数据完整过一遍算一个 epoch |
| convergence | 收敛 | 参数 / 损失逐渐稳定到最优附近 |
| divergence | 发散 | 损失越来越大（常因学习率太大） |
| convex | 凸函数 | "碗状"曲面，只有一个最低点 |
| local minimum | 局部最小值 | 曲面某个坑底，不一定是全局最优 |
| global minimum | 全局最小值 | 整个损失曲面真正的最低点 |
| chain rule | 链式法则 | 复合函数求导法则，梯度计算的基础 |
| feature scaling | 特征缩放 | 把特征归一化，让训练更稳定 |
|---|---|---|
| backpropagation | 反向传播 | 用链式法则从损失往回、高效算出所有参数梯度的算法 |
| chain rule | 链式法则 | 复合函数求导：依赖链上各段局部导数连乘 |
| computational graph | 计算图 | 把一次计算拆成"操作节点"构成的图 |
| forward pass | 前向传播 | 从输入算到损失，并存下中间量 |
| backward pass | 反向传播（过程）| 从损失往输入方向，逐节点求梯度 |
| local gradient | 本地梯度 | 某节点"输出对输入"的导数，只跟该节点有关 |
| upstream gradient | 上游梯度 | 从损失一路连乘、传到当前节点的梯度 |
| sigmoid | sigmoid 函数 | σ(z)=1/(1+e⁻ᶻ)，把实数压到 (0,1) |
| sigmoid derivative | sigmoid 导数 | σ'(z)=σ(z)(1−σ(z))=a(1−a) |
| gradient checking | 梯度检验 | 用数值梯度验证反向传播推导是否正确 |
| numerical gradient / finite difference | 数值梯度 / 有限差分 | (L(w+ε)−L(w−ε))/(2ε) 近似导数 |
| intermediate value | 中间量 | 前向算出、反向要复用的中间结果（如 z、a）|
|---|---|---|
| multilayer perceptron (MLP) | 多层感知机 | 含至少一个隐藏层的前馈神经网络 |
| hidden layer | 隐藏层 | 输入层和输出层之间的中间层 |
| activation function | 激活函数 | 给网络引入非线性的函数 |
| nonlinearity | 非线性 | 让网络能表达弯曲/复杂关系的性质 |
| ReLU (rectified linear unit) | 修正线性单元 | max(0,z)，现代隐藏层默认激活 |
| tanh | 双曲正切 | 输出 (−1,1)，零中心的 S 型激活 |
| dead ReLU | 死亡 ReLU | 神经元恒落负区间、导数恒 0、不再更新 |
| vanishing gradient | 梯度消失 | 梯度经多层连乘趋近 0，前层学不动 |
| exploding gradient | 梯度爆炸 | 梯度连乘后变得极大 |
| matrix multiplication (@) | 矩阵乘法 | X@W，按矩阵乘法规则；区别于逐元素 * |
| element-wise (*) | 逐元素运算 | 对应位置分别运算 |
| weight matrix | 权重矩阵 | 一层的权重，形状 (输入维, 输出维) |
| feedforward | 前馈 | 信息从输入单向流向输出 |
|---|---|---|
| training loop | 训练循环 | 前向 → 损失 → 反向 → 更新，反复迭代 |
| from scratch | 从零实现 | 不依赖框架，手写前向和反向传播 |
| backward pass (MLP) | 反向传播（多层）| 逐层用"上游 × 本地梯度"算出各参数梯度 |
| ReLU backward | ReLU 反向 | 梯度只在 z>0 处通过，乘 (z>0) 掐断负区间 |
| transpose (.T) | 转置 | 矩阵行列互换，用于让梯度矩阵形状对上 |
| axis=0 | 沿样本维 | np.sum 按第 0 维求和（把各样本梯度加总）|
| keepdims | 保持维度 | 求和后保留原维数，便于后续广播 |
| batch | 批 | 一次前向/反向所用的一组样本 |
| Tensor | 张量 | PyTorch 的多维数组，能上 GPU、能自动求导 |
| autograd | 自动微分 | PyTorch 自动求梯度的机制 |
| requires_grad | （是否）需要梯度 | 张量属性，`True` 表示追踪其梯度 |
| computation graph | 计算图 | 记录运算过程的图，反向传播沿它求导 |
| backward | 反向（传播） | 张量方法 `.backward()`，触发自动求导 |
| gradient | 梯度 | 求导结果，存在 `.grad` 属性里 |
| scalar | 标量 | 单个数（0 维张量）；`backward()` 只能对标量调用 |
| forward pass | 前向传播 | 由输入算出预测/loss 的过程 |
| epoch | （训练）轮次 | 把全部训练数据过一遍算一个 epoch |
| learning rate | 学习率 | 每步参数更新的步长，常记作 `lr` |
| MSE (Mean Squared Error) | 均方误差 | 常用回归损失：误差平方的平均 |
| in-place operation | 原地操作 | 直接改原张量，PyTorch 里以下划线结尾（如 `zero_()`） |
| no_grad | 无梯度（上下文） | `torch.no_grad()`，块内运算不建计算图 |
| detach | 分离 | 把张量从计算图中剥离出来 |
| device | 设备 | 张量所在位置：CPU 或 GPU，只是「地址标签」 |
| CPU | 中央处理器 | 核少但强，擅长复杂串行任务 |
| GPU | 图形处理器 | 核多但弱，擅长海量简单运算并行 |
| CUDA | —— | NVIDIA 的 GPU 计算平台；`torch.cuda.is_available()` 检测 |
| broadcasting | 广播 | 不同形状张量做逐元素运算时的自动对齐机制 |
