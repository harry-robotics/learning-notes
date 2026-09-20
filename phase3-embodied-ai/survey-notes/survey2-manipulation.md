# Survey 2: Robot Manipulation

## Survey Information

| Item | Description |
|---|---|
| Topic | Robot Manipulation |
| Research Area | Embodied AI / Robot Learning |
| Purpose | 理解机器人如何学习并执行物理操作 |
| Main Focus | Task Taxonomy, Learning-based Policy, Action Modeling |
| Learning Connection | Diffusion Policy, ACT, VLA, Imitation Learning |

---

# 1. Overview

Robot Manipulation（机器人操作）研究如何让机器人通过身体与环境进行物理交互，并完成目标任务。

相比传统视觉任务，Manipulation 不仅需要理解环境，还需要产生可靠动作。

核心流程：

**Observation → Understanding → Planning → Action Generation → Execution → Feedback**

主要挑战：

- 环境具有不确定性；
- 物体存在物理约束；
- 动作需要连续且稳定；
- 错误会影响后续状态。

因此 Manipulation 是 Embodied AI 从“理解世界”走向“改变世界”的关键方向。

---

# 2. Manipulation Task Taxonomy

机器人操作任务可以按照复杂程度划分：

| Task | Description | Example |
|---|---|---|
| Grasping | 获取物体 | 抓取杯子 |
| Basic Manipulation | 简单物体操作 | 移动、放置 |
| Tool Use | 使用工具完成任务 | 使用夹具 |
| Dexterous Manipulation | 高自由度操作 | 多指机器人手 |
| Deformable Object Manipulation | 柔性物体操作 | 布料、线缆 |
| Mobile Manipulation | 移动与操作结合 | 家庭机器人 |
| Humanoid Manipulation | 人形机器人操作 | 全身协调任务 |

发展趋势：

**Single-task Robot → Multi-task Robot → General-purpose Robot**

---

# 3. Traditional Robot Manipulation Pipeline

传统机器人系统通常采用模块化设计：

**Perception → Planning → Control**

主要模块：

| Module | Function |
|---|---|
| Perception | 获取环境状态 |
| Planning | 规划任务和运动 |
| Control | 执行动作 |

优势：

- 可解释；
- 容易调试；
- 工程可靠性较高。


局限：

- 泛化能力有限；
- 需要人工设计规则；
- 难以适应开放环境。


---

# 4. Learning-based Manipulation

近年来机器人操作逐渐从规则驱动转向数据驱动。

核心思想：

通过机器人数据学习：

Observation → Action

之间的映射。


主要方法：

| Method | Core Idea | Characteristics |
|---|---|---|
| Imitation Learning | 学习专家示范 | 数据需求明确，训练稳定 |
| Reinforcement Learning | 通过奖励优化策略 | 灵活但真实训练成本高 |
| Self-supervised Learning | 利用无标签数据学习 | 降低数据需求 |
| Diffusion Policy | 学习动作分布 | 适合复杂动作生成 |
| Transformer Policy | 建模长序列关系 | 支持多模态输入 |
| VLA | 融合视觉、语言和动作 | 提升语义理解能力 |

---

# 5. Imitation Learning（模仿学习）

Imitation Learning 的核心：

让机器人模仿专家行为。


基本流程：

**Expert Demonstration → Observation-Action Dataset → Policy Learning → Robot Execution**


优势：

| Advantage | Description |
|---|---|
| 不需要设计复杂奖励 | 避免Reward Engineering |
| 适合真实机器人 | 可以直接利用示范数据 |


主要问题：

## Distribution Shift（分布偏移）

训练阶段：

机器人学习专家轨迹。


执行阶段：

机器人产生自己的误差。


误差累积：

状态偏离训练分布 → 动作质量下降 → 任务失败。


---

# 6. Reinforcement Learning（强化学习）

强化学习通过奖励函数优化策略。

基本过程：

**State → Action → Reward → Policy Update**

优势：

- 可以探索未知策略；
- 不依赖人工示范。


挑战：

- 真实机器人训练成本高；
- 奖励设计困难；
- 训练过程不稳定。


因此实际机器人中常与：

Simulation

+

Imitation Learning

结合使用。

---

# 7. Diffusion Policy

Diffusion Policy 是近年来机器人操作的重要方法。


核心思想：

将动作生成建模为条件生成过程：

**Observation → Action Distribution**


与传统 Policy 区别：

传统：
Observation → Single Action


Diffusion Policy：

Observation → Possible Action Distribution


优势：

| Advantage | Description |
|---|---|
| 多模态动作 | 可以表示多种合理行为 |
| 复杂任务能力强 | 适合高维动作空间 |
| 稳定性较好 | 在多个操作任务中表现优秀 |


限制：

- 推理速度较慢；
- 需要较多数据；
- 部署成本较高。


---

# 8. ACT（Action Chunking with Transformers）

ACT 是基于 Transformer 的机器人策略学习方法。


核心思想：

不预测单个动作，而是预测动作序列：

**Observation → Action Chunk**

优势：

| Advantage | Description |
|---|---|
| 减少控制频率压力 | 一次生成多个动作 |
| 提高动作连续性 | 减少抖动 |
| 利用Transformer能力 | 建模时间关系 |


与 Diffusion Policy 对比：

| | ACT | Diffusion Policy |
|---|---|---|
| 方法 | Transformer sequence modeling | Diffusion generation |
| 输出 | Action Chunk | Action Distribution |
| 特点 | 高效、结构简单 | 灵活、表达能力强 |

---

# 9. VLA and Manipulation

Vision-Language-Action (VLA) 将视觉语言模型能力引入机器人操作。


传统 Robot Learning：

Image → Action


VLA：

Vision + Language → Action


例如：

输入：

“把桌上的红色杯子放到架子上”


模型需要：

| Capability | Function |
|---|---|
| Vision Understanding | 找到杯子 |
| Language Understanding | 理解任务 |
| Action Generation | 执行动作 |


VLA 提升了机器人处理复杂语言任务的能力。

---

# 10. Current Challenges

## Data Problem

机器人数据难以规模化：

| Problem | Reason |
|---|---|
| High Cost | 真实机器人采集昂贵 |
| Embodiment Difference | 不同机器人结构不同 |
| Long-tail Tasks | 少见任务数据不足 |


---

## Generalization Problem

机器人需要适应：

- 新物体；
- 新环境；
- 新任务。


当前模型容易依赖训练数据分布。

---

## Long Horizon Tasks

简单任务：

抓取一个物体。

复杂任务：

整理房间、完成多步骤操作。


困难原因：

- 多步骤误差累积；
- 缺少长期记忆；
- 缺少任务恢复能力。


---

## Physical Grounding

机器人需要理解：

- 空间关系；
- 物理规律；
- 因果关系。


当前模型可能具有视觉和语言关联能力，但不一定具备真正物理理解。

---

# 11. Future Directions

## Data-efficient Robot Learning

目标：

降低机器人学习的数据成本。

方向：

- Simulation Data
- Self-supervised Learning
- Autonomous Data Collection


## 3D-aware Manipulation

从：

2D Image

发展到：

3D Scene Understanding


关注：

- Depth
- Geometry
- Object Relationship


## Mobile Manipulation

结合：

Navigation + Manipulation


目标：

让机器人在真实环境中移动并完成操作。


## General Robot Policy

探索能够适应多任务、多环境的通用机器人策略。

---

# Learning Summary

Robot Manipulation 可以理解为：

**Perception → Planning → Policy Learning → Action Execution**

其中：

- Perception 负责理解环境；
- Planning 负责任务分解；
- Policy Learning 负责动作生成；
- Control 负责执行。


当前机器人操作的发展路线：

**Rule-based Robotics → Learning-based Policy → Foundation Model-based Robot Intelligence**

后续学习重点：

- Imitation Learning
- Diffusion Policy
- ACT
- Vision-Language-Action Models
- Robot Dataset and Benchmark