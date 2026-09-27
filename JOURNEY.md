# Learning Journey

> 这份文件记录我在学习与科研训练过程中形成的**思考方式、方法论调整与阶段性决策**，而不是知识本身。
>
> 技术知识、代码与公开学习笔记放在各 phase / topic 文件夹中。
>
> 我越来越相信：
>
> **真正长期积累的不是“我学过多少内容”，而是“我如何判断应该学什么、研究什么，以及如何把问题推进到可验证”。**

---

# 背景

- **专业背景**：车辆工程
- **长期方向**：Embodied AI / Robot Learning
- **长期目标**：成为能够同时发现研究问题、完成实验并构建真实系统的 engineer-researcher
- **学习模式**：AI 辅助 + 产出驱动 + 问题驱动 + 持续迭代
- **当前阶段（2026.9）**：
  - 已完成深度学习与 Transformer 基础训练
  - 已完成 MuJoCo + LIBERO 仿真环境搭建
  - 已从“学习技术”进入“研究问题探索与筛选”阶段

车辆工程背景不再被视为需要“摆脱”的东西。

相反，它提供了对：

- 物理系统
- 传感器
- 运动
- 机械约束
- 真实部署

的直觉。

未来真正重要的不是刻意维持某个专业标签，而是把这些系统理解转化为研究优势。

---

# 学习方法演化记录

## v1.0 — 启动期（2026 春，Day 1-2）

- 一开始想“什么都学下来”
- 笔记里堆满细节
- 每一个概念都担心以后会用到

### 教训

信息不是越多越好。

真正有限的是：

**注意力、时间和认知带宽。**

如果没有判断标准，学习会变成无限扩展的信息收集。

---

## v1.1 — 引入“四象限分类”（Day 3 起）

每天结束后将内容区分为：

| 类型 | 学习要求 |
|---|---|
| 操作必须熟练 | 需要能够独立使用 |
| 操作跟一遍即可 | 建立基本操作印象 |
| 知识重点理解 | 需要形成心智模型 |
| 知识无需记忆 | 知道存在即可 |

### 效果

开始主动分配认知带宽，而不是默认所有知识同等重要。

---

## v2.0 — 关键转折：AI 时代学什么（2026.5）

### 困惑

Python 基础学习很快，而 C 指针、底层细节明显更费力。

与此同时，AI 已经能够生成大量代码。

于是第一次认真思考：

> 如果 AI 会写代码，我真正应该训练什么？

### 结论

1. **机械式写代码的价值下降，但理解和判断代码的价值上升**
2. 要内化的是：
   - 判断标准
   - 系统结构
   - 工程纪律
   - Debug 思维
3. AI 是脚手架，不是替代品
4. 如果没有自己的内部模型，就无法判断 AI 的输出是否正确
5. **Debug 能力 > 默写能力**

### 行动

不再把“从零默写代码”当作主要学习指标。

开始更重视：

- 能不能读懂陌生实现
- 能不能定位错误
- 能不能修改已有系统
- 能不能解释为什么这样设计

---

## v3.0 — 两个旋钮：讲什么 vs 讲多深（2026.8）

暑假进入深度学习后，遇到新的问题：

> 内容越来越多，但学完之后没有重点，也无法清晰讲出来。

后来意识到这里其实有两个独立变量。

| 旋钮 | 调整方向 | 判断标准 |
|---|---|---|
| **讲什么** | 往少了调 | 对未来研究、实验或工程有没有实际价值？ |
| **讲多深** | 不许随意降低 | 一旦决定保留，就理解到没有关键障碍 |

### 核心认知

> **精简的对象应该是知识点数量，而不是单个知识点的理解质量。**

“知道结论但不知道原因”会产生夹生知识。

这种知识在遇到：

- 新任务
- 新模型
- 新错误
- 新论文

时几乎无法迁移。

---

## v3.1 — 并列知识记不住，因果链才记得住（2026.8）

学完 Transformer 后发现：

> 每一个知识点单独都懂，但无法串起来，也无法自然讲出来。

原因：

笔记按时间顺序记录，最终留下的是一堆**并列结论**。

而人的理解更依赖：

> **结构与因果关系。**

例如 Transformer，与其记住几十条零散结论，不如建立一个核心画面：

> Transformer 是一条持续传递的信息主干。
>
> Attention 在 token 之间横向交换信息；
>
> FFN 在每个 token 内独立加工；
>
> Residual 保证信息主干始终存在。

一旦这个结构真正建立：

- 为什么形状需要保持
- 为什么有残差
- 为什么 LayerNorm 放在某个位置
- 为什么模型可以不断堆深

很多细节会自然成为推论。

### 因此形成三层学习节奏

1. **走完整教学**
   - 建立背景、前提和概念关系

2. **提炼总结**
   - 删除不重要内容
   - 只保留真正需要进入长期记忆的部分

3. **跨模块串联**
   - 将多个主题重新组织成统一心智模型

---

## v3.2 — 抄写 ≠ 生成，但生成也未必必要（2026.9）

### 触发

旅游一周没有复习，回来以后发现很多知识无法顺畅调用。

最开始以为问题在于：

> “我从来没有完全脱离参考从零写过代码。”

一度考虑进行“无参考手写复现周”。

后来重新分析后取消。

### 新判断

- 跟着教程逐行敲代码，本质仍然是抄写
- 从零手写本身不是科研或工程的最终目标
- 实际研究通常会：
  - 使用已有库
  - 修改已有代码
  - 调用 AI
  - 基于 baseline 继续开发

真正不可替代的是：

| 能力 | 要求 |
|---|---|
| **读** | 快速理解陌生实现和标准版本的差异 |
| **改** | 知道需求变化后应该修改哪里 |
| **调** | 出现错误时能够定位原因并解释后果 |

### 但仍有一个前提

> 无法在工作记忆中调用的知识，也无法真正参与思考。

所以：

- 架构主线
- tensor / shape flow
- 模型输入输出接口
- 训练与推理基本机制

仍然需要形成内部模型。

只是：

**不再要求逐字复写代码。**

### 另一个重要认知

> 实践最大的价值不是“把操作练熟”，而是制造真实失败。

真实失败会暴露：

> 我以为自己懂，但实际上没有理解的地方。

这种诊断能力是单纯复习无法替代的。

---

## v4.0 — 从“学习知识”进入“寻找研究问题”（2026.9）

这是到目前为止最大的一次阶段变化。

完成 Transformer、mini-GPT、PyTorch、CNN、MuJoCo、LIBERO 等基础训练后，继续学习更多技术已经不再是最优路径。

真正的问题开始变成：

> **Embodied AI 中什么问题值得研究？**

于是研究流程从：

```text
学技术
↓
学更多技术
↓
再学更多技术
```

改变为：

```text
建立领域地图
↓
理解研究问题
↓
筛选 Candidate Problem
↓
针对真正需要的问题再学习方法
```

### 核心变化

以前：

> “我还缺什么知识？”

现在：

> “我要解决的问题需要什么知识？”

学习开始由任务倒逼。

---

## v4.1 — Survey 不是终点，而是入口（2026.9）

通过 Embodied AI、Robot Manipulation、VLA 等 survey 建立第一版领域地图后，意识到：

Survey 最大的作用不是：

> 告诉我最终应该研究什么。

而是：

> 帮我建立问题空间的坐标系。

因此形成新的探索顺序：

```text
Survey / Landscape
↓
Research Problem Landscape
↓
Problem Map
↓
Candidate Research Problems
↓
SOTA / Benchmark / Gap Verification
↓
Research Question
↓
Experiment
```

这和一开始“看到一个热门模型就想复现”的方式有本质不同。

---

## v4.2 — 方法不是方向，研究应该从 Problem 开始（2026.9）

在 Embodied AI 探索中，一个重要纠正是：

不能把：

- Diffusion Policy
- ACT
- VLA
- World Model

直接当成最终研究问题。

例如：

- **Diffusion Policy** 是一种 policy generation 方法；
- **ACT** 是一种基于 Action Chunking 的 policy 方法；
- **VLA** 是一种模型 / 系统范式；
- **World Model** 是一类状态表示、预测和决策机制。

真正需要问的是：

> 机器人为什么失败？

以及：

> 哪个能力缺口还没有被解决？

然后才考虑：

> 什么方法可能解决它？

因此形成：

```text
Research Challenge
↓
Research Problem
↓
Hypothesis
↓
Method
```

而不是：

```text
热门 Method
↓
强行找问题
```

---

## v4.3 — AI 不应该替代科研判断，但应该大幅压缩信息搜索（2026.9）

早期曾担心：

> 如果 AI 帮我搜索和总结论文，我是不是失去了科研训练？

后来认识到：

AI 时代真正的科研能力不是：

> 手工完成所有信息搜索。

而是：

> 知道什么可以委托给 AI，以及哪些结论必须自己判断。

### AI 更适合

- 大规模 literature mining
- 文献整理
- paper matrix
- benchmark 收集
- 方法关系梳理
- 代码辅助
- 实验辅助

### 人必须负责

- 判断问题是否重要
- 判断论文证据是否支持结论
- 判断哪些 gap 值得研究
- 提出 hypothesis
- 决定实验设计
- 对研究结果负责

AI 的价值是：

> **Information Compression**

而不是：

> **Research Judgment Replacement**

---

## v4.4 — 五个问题地图后：不同方向可能在解决同一个底层问题（2026.9）

第一轮研究问题探索覆盖了多个 Embodied AI 方向。

在继续细分后发现：

很多看起来属于不同领域的问题实际上高度交叉。

例如：

```text
Perception
↓
Representation
↓
Generalization
↓
World State
↓
Prediction
↓
Planning
```

它们并不是彼此完全独立的模块。

一个研究问题往往可以从：

- 不同研究社区
- 不同技术路径
- 不同实验层级

切入。

### 新的认识

以后不应该只问：

> “这个问题属于哪个方向？”

更重要的是问：

> **它真正试图解决的底层能力缺口是什么？**

因此开始做：

**Cross-direction Candidate Consolidation**

把重复或高度相似的问题重新压缩。

---

## v4.5 — 科研系统应该服务执行，而不是替代执行（2026.9）

随着文件、AI 工作流、知识库逐渐完善，又出现一个新的风险：

> 不断优化科研流程本身。

于是确立原则：

> **Research system should support research execution, not replace it.**

以后：

- 文件结构够用就冻结；
- 模板能支撑工作就不反复设计；
- 学习深度由当前研究问题决定；
- 每一项工作都要问：
  - 是否让问题更清楚？
  - 是否让实验更接近？
  - 是否让论文更接近？

如果答案都是否定的：

> 就不应该继续投入大量时间。

---

# 当前科研训练方法

截至 2026.9，目前形成的 provisional workflow：

```text
1. Domain Landscape
   ↓
2. Research Problem Landscape
   ↓
3. Literature Mining
   ↓
4. Candidate Research Problems
   ↓
5. Cross-direction Consolidation
   ↓
6. Systematic Research Opportunity Verification
   ↓
7. Research Question
   ↓
8. Hypothesis
   ↓
9. Baseline / Experiment
   ↓
10. Analysis / Writing
```

这还不是最终科研方法论。

只有真正经历：

- baseline
- experiment
- failure
- iteration
- paper writing

以后，才有资格进一步完善。

---

# 关键决策记录

## 决策 1：选择 ESP32 作为工程入门（2026 春）

### 候选

- ESP32
- STM32
- Raspberry Pi

最终选择：

**ESP32**

### 当时理由

- 入门门槛低
- 硬件成本低
- 生态成熟
- 可以快速获得完整系统经验

### 2026.9 复盘

具体 API 已经很少直接使用。

但这些经验一直保留：

- 资源约束
- 并发
- 非阻塞思维
- 硬件行为与软件假设不一致
- Debug 实体系统

所以：

> 选它没有问题。

真正需要调整的是：

> 不应该在入门技术上停留过久。

---

## 决策 2：暑假转向深度学习与具身智能（2026.7）

原计划：

```text
ROS2
↓
SLAM
↓
CARLA
↓
自动驾驶系统
```

后来意识到：

真正最感兴趣的问题是：

**Embodied Intelligence**

于是改为：

```text
Deep Learning
↓
Transformer
↓
Robot Learning
↓
Embodied AI
```

C++、ROS2、SLAM 并没有被永久删除。

而是调整为：

> 当真实研究 / 工程任务需要时，再由任务倒逼学习。

---

## 决策 3：重新理解车辆工程背景（2026.8–9）

早期曾尝试将 driving 作为主要 embodiment 入口，以最大程度利用车辆背景。

进入 Embodied AI Research Problem Exploration 后，判断进一步变化：

> 不应该为了“保持专业一致性”强行限制研究问题。

车辆工程真正提供的是：

- 对物理系统的理解
- 传感器与空间直觉
- 机械与运动约束意识
- 对真实世界部署复杂度的认识

这些能力可以迁移到：

- robot manipulation
- mobile robots
- autonomous systems
- embodied perception

因此未来的研究问题选择以：

> **Scientific Value + Feasibility + Personal Interest**

为核心。

车辆背景作为优势，而不是边界。

---

## 决策 4：智能车竞赛 `[待最终确认]`

原计划：

2027 年全国大学生智能汽车竞赛。

### 重新评估原因

- 大量线下调车
- 硬件维护成本高
- 与当前 Research Problem Exploration 的直接关系有限

### 当前原则

如果时间资源冲突：

> 优先能形成科研闭环和长期研究能力的工作。

最终是否参加仍根据科研进展和实际机会决定。

---

## 决策 5：不再把“多学一点”作为进入科研的前置条件（2026.9）

以前总觉得：

> Transformer 学完以后，还应该先把 IL、RL、Diffusion、VLA 全学完再开始科研。

现在判断：

这是错误顺序。

新的原则：

> **先发现问题，再针对问题学习方法。**

否则学习永远不会结束。

---

# 道心动摇时刻

## 时刻 1：AI 都能写代码，我学这些有意义吗？（2026.5）

见 v2.0。

最终结论：

> 写代码本身价值发生变化，但工程判断力没有贬值。

---

## 时刻 2：ESP32 对未来方向有用吗？（2026.5）

最终认识：

很多 API 会过期，但：

- 工程约束
- Debug
- 系统思维

不会。

---

## 时刻 3：学了一堆但讲不出来（2026.8）

最终认识：

> 问题不是知识数量，而是知识结构。

从：

> “并列知识点”

转向：

> “因果心智模型”

---

## 时刻 4：一周不复习就忘了很多（2026.9）

最终认识：

遗忘本身不等于学习失败。

真正有价值的是：

> 哪些东西经过时间后仍然可以重新推导？

于是开始用遗忘反向诊断：

- 哪些只是短期记忆
- 哪些已经形成结构理解

---

## 时刻 5：科研探索会不会一直停留在“准备阶段”？（2026.9）

随着 Survey、Landscape、Compute Literacy、Problem Map 越做越多，开始意识到：

> “准备科研”本身也可能成为拖延真正科研的一种方式。

于是设定新的退出条件：

一旦 Candidate Research Problems 经过：

- SOTA
- benchmark
- resource
- novelty-space

核查并收敛，就必须进入：

> **Baseline + Experiment**

而不是重新做一轮更大的 Landscape。

---

# 学习资产

## 公开仓库

- `harry-robotics/learning-notes`
- `harry-robotics/arduino-smart-car`

## 私有科研仓库

- `Research`

私有仓库用于保存：

- 未公开 research analysis
- candidate selection
- research hypotheses
- experiment plans
- AI-assisted literature synthesis
- research decisions

公开仓库只保存：

- 技术知识
- 学习笔记
- 教程
- 公开 reproduction
- 方法论总结

---

# 阶段性产出

| 时间 | 产出 |
|---|---|
| 2026.5 | ESP32 嵌入式基础、智能小车项目 |
| 2026.6–7 | OpenCV、车道线检测、特征匹配 |
| 2026.7–8 | PyTorch、CNN、CIFAR-10 |
| 2026.8 | Transformer from scratch、mini-GPT |
| 2026.9 | MuJoCo + LIBERO 环境配置 |
| 2026.9 | Embodied AI / Manipulation / VLA survey 阅读 |
| 2026.9 | Embodied AI Landscape |
| 2026.9 | Research Problem Landscape |
| 2026.9 | 五个研究问题方向第一轮 Literature / Problem Map |
| 2026.9 | Cross-direction Candidate Consolidation |
| 2026.9 | 准备进入 Systematic Research Opportunity Verification |

---

# 当前阶段

当前已经正式从：

**Learning Preparation**

进入：

# Research Problem Discovery

下一阶段重点不再是扩大学习范围，而是：

```text
Candidate Research Problems
↓
SOTA / Benchmark / Resource Verification
↓
Research Question
↓
Baseline
↓
Experiment
```

---

# 给未来自己的话

如果你以后已经在真正做论文、跑实验，甚至已经读博或进入行业，请记得：

最开始真正困难的并不是：

> “某个模型怎么实现？”

而是：

> “我到底应该把时间花在哪里？”

一路上很多方法都被推翻过：

- 从“什么都学”
- 到“只学重要内容”
- 从“从零写代码”
- 到“读改调”
- 从“先学完再科研”
- 到“由问题倒逼学习”

真正值得保留的是：

> **不断修正自己的能力。**

也请未来的自己继续检查：

> 现在使用的方法，是否仍然服务当前目标？

如果没有：

> 继续迭代。

---

*Last updated: 2026-09-27*