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
|---|---|---|
| class | 类 | 造对象的「蓝图」，打包数据和方法 |
| instance / object | 实例 / 对象 | 照类造出来的具体东西 |
| self | 自身 | 方法第一个参数，指「当前这个对象」 |
| __init__ | 构造函数 | 造对象时自动运行，负责初始化 |
| method | 方法 | 类里定义的函数 |
| inheritance | 继承 | 子类白拿父类的所有本事 |
| super() | 父类（引用） | `super().__init__()` 先初始化父类 |
| nn.Module | —— | PyTorch 所有模型的基类 |
| forward | 前向（方法） | 定义数据如何流过网络 |
| nn.Linear | 全连接层 | 线性层，内部自动管好 W 和 b |
| fully-connected layer | 全连接层 | 每个输入连到每个输出 |
| ReLU | 修正线性单元 | 激活函数，负数变 0 |
| logits | 原始分数 | 网络输出的未归一化分数 |
| softmax | —— | 把分数转成概率分布 |
| cross-entropy loss | 交叉熵损失 | 分类常用损失；内部含 softmax |
| optimizer | 优化器 | 打包参数更新与清零（如 SGD） |
| SGD | 随机梯度下降 | 最基础的优化器 |
| optimizer.step() | —— | 用梯度更新参数（≈ Day1 手写更新） |
| optimizer.zero_grad() | —— | 清零所有参数梯度 |
| Dataset | 数据集 | 数据的容器 |
| DataLoader | 数据加载器 | 把数据切成 mini-batch 喂入 |
| mini-batch | 小批量 | 每次喂入的一小批样本 |
| batch_size | 批大小 | 每批多少个样本 |
| epoch | 轮次 | 把全部数据过一遍 |
| MNIST | —— | 手写数字数据集（0~9，28×28） |
| transform | 变换 | 数据预处理（如 ToTensor） |
| accuracy | 准确率 | 预测对的比例 |
|---|---|---|
| convolution | 卷积 | 小窗口滑过图片、逐位置加权求和的操作 |
| CNN (Convolutional Neural Network) | 卷积神经网络 | 以卷积为核心的网络，图像任务主力 |
| kernel / filter | 卷积核 / 滤波器 | 那个小权重窗口；权重是学出来的 |
| feature map | 特征图 | 一个核扫完整图的输出，某特征的位置分布图 |
| receptive field | 感受野 | 一个输出值对应输入里多大一块区域 |
| parameter sharing | 参数共享 | 同一个核用于所有位置，CNN 好处的根源 |
| translation invariance | 平移不变性 | 图案在哪都能被同一个核检测到 |
| channel | 通道 | 图像的颜色层：灰度 1、彩色 3 |
| nn.Conv2d | 二维卷积层 | PyTorch 里建卷积层的类 |
| in_channels / out_channels | 输入/输出通道数 | 后者＝用几个核＝出几张特征图 |
| kernel_size | 核大小 | 卷积核的边长，如 3 表示 3×3 |
| NCHW | —— | 图像张量维度约定：batch, channel, height, width |
| batch | 批 | 一次喂入的图片张数 |
| stride | 步幅 | 核每次滑动几格（下一天详讲） |
| padding | 填充 | 给图片周围补边，防止缩小（下一天详讲） |
| nn.Parameter | 可学习参数 | 把张量注册成网络的可训练权重 |
|---|---|---|
| padding | 填充 | 图片四周补 0，防止卷积后尺寸缩小 |
| stride | 步幅 | 卷积核每次滑动几格；越大输出越小 |
| pooling | 池化 | 把特征图切块、每块留一个代表值，压缩信息 |
| max pooling | 最大池化 | 每块取最大值，最常用；无可学习参数 |
| nn.MaxPool2d | 最大池化层 | PyTorch 里的最大池化；默认 stride=窗口大小 |
| in_channels | 输入通道数 | 图片有几层：灰度1/彩色3；由数据决定 |
| out_channels | 输出通道数 | ＝用几个核＝出几张特征图；由设计决定 |
| feature map | 特征图 | 一个核的输出 |
| LeNet | —— | 1998 年第一个成功的 CNN，卷积+池化+全连接范式 |
| feature extractor | 特征提取器 | CNN 前半段（卷积+池化部分） |
| classifier head | 分类头 | CNN 后半段（展平+全连接部分） |
| flatten | 展平 | 把多维特征图拉成一维，交给全连接层 |
|---|---|---|
| Logits | 原始分数 / 对数几率 | 网络最后一层的无约束输出，softmax 的输入 |
| Softmax | 归一化指数函数 | 不译；两步：取 exp、除以总和 |
| Hard-max / Argmax | 硬最大 | 不可导，无法 backward，故不能训练 |
| Shift Invariance | 平移不变性 | logits 加常数输出不变，PyTorch 用它防 exp 溢出 |
| One-hot | 独热 | 只有一个分量为 1 的向量 |
| Saturation | 饱和 | softmax 接近 one-hot 时梯度趋近 0 |
| Attention | 注意力 | 一次可导的「软检索」 |
| Self-Attention | 自注意力 | Q、K、V 均来自同一输入序列 |
| Query / Key / Value | 查询 / 键 / 值 | 论文与代码中一律用 Q/K/V，不译 |
| Scaled Dot-Product Attention | 缩放点积注意力 | "Scaled" 指除以 √d_k |
| Attention Score | 注意力分数 | softmax 之前的原始相似度 |
| Attention Weights | 注意力权重 | softmax 之后的 (seq_q, seq_k) 矩阵，每行和为 1 |
| Soft Retrieval | 软检索 | 与硬检索（argmax，不可导）对立 |
| Causal Mask | 因果掩码 | 下三角，禁止看未来位置 |
| Padding Mask | 填充掩码 | 屏蔽 batch 内为对齐而填充的位置 |
| Inductive Bias | 归纳偏置 | 模型结构自带的先验假设 |
| Locality | 局部性 | CNN 的核心假设之一 |
| Translation Invariance | 平移不变性（卷积） | 参数共享带来的性质，与 softmax 的 shift invariance 不同概念 |
| Receptive Field | 感受野 | 输出单元能「看到」的输入范围 |
| Long-Range Dependency | 长距离依赖 | RNN/CNN 的短板，attention 的主场 |
| Permutation Equivariance | 置换等变性 | self-attention 的固有性质，引出位置编码 |
| Normalization | 归一化 | 统称 |
| Batch Normalization (BatchNorm) | 批归一化 | 跨样本、同通道；nn.BatchNorm2d |
| Layer Normalization (LayerNorm) | 层归一化 | 单样本、跨特征；Transformer 采用 |
| Running Statistics | 滑动统计量 | BatchNorm 推理时使用，train/eval 行为不同的根源 |
| Learnable Parameter | 可学习参数 | 如 γ、β，会进 model.parameters() |
| Residual Connection | 残差连接 | y = F(x) + x |
| Skip Connection | 跳跃连接 | 与残差连接常混用 |
| Identity Mapping | 恒等映射 | F(x) ≈ 0 时残差块退化成的形式 |
| Vanishing Gradient | 梯度消失 | 深层网络的核心优化障碍 |
| Jacobian Matrix | 雅可比矩阵 | 向量对向量的导数；今天只用其形状概念 |
| Broadcasting | 广播 | 张量维度自动扩展规则 |
| In-place Operation | 原地操作 | PyTorch 中带下划线后缀的方法，如 masked_fill_ |
| Random Seed | 随机种子 | 实验可复现性的前提 |
| Invariant Check | 不变量检查 | 如「权重每行和为 1」，研究代码的自检手段 |
| Skeleton Reconstruction | 骨架重建 | 允许查 API，但结构要自己想出来 |
| Attention Pattern | 注意力模式 | 权重矩阵的可视化，3b1b 用的说法 |
| Information Leakage | 信息泄露 | 模型看到了本不该看到的答案；复现类工作最常见的隐藏 bug |
| Teacher Forcing | 教师强制 | 训练时用真实前文而非模型自己的输出，与 causal mask 配套 |
| Autoregressive | 自回归 | 逐个生成、每步都依赖已生成内容的模型（如 GPT） |
|---|---|---|
| Multi-Head Attention (MHA) | 多头注意力 | 并行多组 QKV，各自捕捉一种关系 |
| Head | 头 | 一组独立的 W^Q/W^K/W^V |
| num_heads / h | 头数 | 原论文取 8 |
| d_model | 模型维度 | Transformer 主干特征维，原论文 512 |
| d_k | 每个头的维度 | d_model / num_heads，8 头时为 64 |
| Output Projection (W^O) | 输出投影 | 把各头结果融合，多头之后的必要一步 |
| Concat | 拼接 | 把各头输出首尾相接还原成 d_model |
| Split Heads | 切分头 | (batch, seq, d_model) → (batch, h, seq, d_k) |
| Combine Heads | 合并头 | 上一步的逆操作 |
| view | 视图重塑 | 改形状不复制数据，要求内存连续 |
| reshape | 重塑 | 类似 view，必要时自动复制；调试期更推荐 view |
| contiguous | 连续化 | 真正复制数据使内存顺序与逻辑顺序对齐 |
| Stride | 步长 | 张量在内存中各维度的读取跨度 |
| Memory Layout | 内存布局 | transpose 只改读法不搬数据的原因 |
| Floor Division | 整除 | Python 的 //，结果为整数 |
| Assertion | 断言 | assert，参数进入计算前的合法性检查 |
| Unpacking | 解包赋值 | a, b, _ = x.size() |
| Self-Attention | 自注意力 | mha(x, x, x) |
| Cross-Attention | 交叉注意力 | mha(语言, 图像, 图像)，VLA 的核心机制 |
| Attention Pattern | 注意力模式 | 权重矩阵的可视化 |
| Information Leakage | 信息泄露 | 模型看到不该看的答案 |
| Autoregressive | 自回归 | 逐个生成、每步依赖已生成内容 |
| Teacher Forcing | 教师强制 | 训练时用真实前文，与 causal mask 配套 |