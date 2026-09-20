# Survey 1: Embodied AI Overview

## Survey Information

| Item | Description |
|---|---|
| Topic | Embodied AI Overview |
| Paper ID | arXiv:2407.06886 |
| Research Area | Embodied AI / Robot Intelligence |
| Purpose | 建立具身智能领域整体认知框架 |
| Main Focus | Robot, Simulator, Perception, Interaction, Agent, Sim-to-Real |
| Reading Goal | 理解 Embodied AI 的主要研究方向和技术体系 |

---

# 1. Overview

Embodied AI（具身智能）研究如何让智能体（Agent）通过物理载体（Embodiment）与环境进行交互，并完成感知、理解、决策和行动。

与传统人工智能不同，Embodied AI 不仅关注模型是否能够处理信息，还关注智能体是否能够：

- 理解真实环境；
- 根据目标制定策略；
- 执行动作；
- 根据反馈调整行为。

基本流程：

**Environment → Perception → Understanding → Planning → Action → Feedback**

---

# 2. Survey Taxonomy

该综述主要从以下几个方向介绍 Embodied AI：

| Research Area | Main Question |
|---|---|
| Robots | 智能体依赖什么物理平台？ |
| Embodied Simulator | 如何构建训练和测试环境？ |
| Embodied Perception | 如何理解环境？ |
| Embodied Interaction | 如何与人和环境交互？ |
| Embodied Agent | 如何自主完成任务？ |
| Sim-to-Real Adaptation | 如何从仿真迁移到现实？ |

整体结构：

**Robot + Simulator → Perception → Interaction → Agent → Real-world Deployment**

---

# 3. Robots

Robot 是 Embodied AI 的物理载体。

常见机器人类型：

| Robot Type | Characteristics |
|---|---|
| Robotic Arm | 主要用于 Manipulation 任务 |
| Mobile Robot | 具备移动能力 |
| Quadruped Robot | 强运动能力 |
| Humanoid Robot | 接近人体结构 |
| Autonomous Vehicle | 面向动态移动环境 |

不同机器人之间的主要差异：

- Embodiment（身体结构）
- Sensor Configuration（传感器配置）
- Action Space（动作空间）

这些差异也是机器人数据难以直接共享的重要原因。

---

# 4. Embodied Simulator

Simulator 为 Embodied AI 提供低成本、可重复的训练环境。

主要分为：

| Type | Description |
|---|---|
| General Simulator | 通用机器人仿真环境 |
| Real Scene Based Simulator | 基于真实场景构建的环境 |

主要作用：

- 生成训练数据；
- 测试算法；
- 降低真实机器人实验成本。

但是 Simulation 与 Reality 之间仍存在差异：

- Visual Gap（视觉差异）
- Physics Gap（物理差异）
- Interaction Gap（交互差异）

---

# 5. Embodied Perception

Embodied Perception 研究智能体如何理解环境。

主要方向：

| Direction | Description |
|---|---|
| Active Visual Perception | 主动获取视觉信息 |
| Visual SLAM | 定位与地图构建 |
| 3D Scene Understanding | 理解三维空间结构 |
| Visual Language Navigation (VLN) | 根据语言完成导航 |

核心问题：

> 智能体如何从传感器信息中形成对环境的有效表示？

发展趋势：

**2D Vision → 3D Understanding → 4D Dynamic Perception**

---

# 6. Embodied Interaction

Embodied Interaction 关注智能体如何影响环境并与其他主体交互。

主要任务：

| Task | Description |
|---|---|
| Embodied Question Answering (EQA) | 根据环境信息回答问题 |
| Grasping | 获取物体 |
| Manipulation | 操作环境对象 |
| Human-Robot Interaction | 与人协作 |

Perception 与 Interaction 的区别：

| Module | Question |
|---|---|
| Perception | 世界是什么？ |
| Interaction | 如何改变世界？ |

例如：

识别桌上的杯子：

Perception

拿起杯子：

Interaction

---

# 7. Embodied Agent

Embodied Agent 研究如何让机器人自主完成复杂任务。

主要包括两个层次：

## Task Planning

核心问题：

**What should the agent do?**

例如：

任务：

“准备一杯咖啡”

任务分解：

寻找杯子 → 加入咖啡 → 倒水


常见方法：

- LLM Planning
- VLM Planning
- Symbolic Planning


## Action Planning

核心问题：

**How should the agent do it?**

例如：

- 如何移动机械臂？
- 如何生成轨迹？
- 如何控制动作？

常见方法：

- API-based Action
- Learned Policy
- VLA Model

---

# 8. Sim-to-Real Adaptation

Sim-to-Real 研究如何将仿真环境中的能力迁移到真实世界。

主要方向：

| Approach | Description |
|---|---|
| Simulation Data | 使用大量仿真数据训练 |
| Real-world Data | 使用真实机器人数据 |
| Domain Adaptation | 缩小仿真与现实差异 |
| World Model | 学习环境变化规律 |

核心挑战：

真实世界具有：

- 不确定性；
- 长尾情况；
- 复杂交互。

---

# 9. Important Challenges

## Data Scaling

机器人数据相比互联网数据更加难以规模化。

原因：

- 采集成本高；
- 需要真实机器人；
- 不同机器人存在差异。


## Generalization

机器人需要面对：

- 未见物体；
- 未见环境；
- 未见任务。


## Physical Understanding

当前模型可以理解视觉和语言信息，但仍需要进一步增强：

- 空间理解；
- 因果关系；
- 物理规律理解。


## Long Horizon Tasks

复杂任务需要：

- 长期规划；
- 记忆能力；
- 错误恢复。


---

# 10. Future Directions

## General-purpose Robot Intelligence

目标：

构建能够适应多任务、多环境的通用机器人系统。


## Scalable Embodied Data

需要：

- 更大规模机器人数据；
- 更丰富任务覆盖；
- 更高效数据采集方式。


## World Model

目标：

让机器人学习环境动态规律，并预测未来状态。


## Multimodal Physical Interaction

未来机器人需要融合：

- Vision
- Language
- Touch
- Force

实现更加完整的环境理解。

---

# Learning Summary

通过该综述，可以建立 Embodied AI 的整体认知框架：

**Robot + Simulator → Perception → Interaction → Agent → Sim-to-Real**

其中：

- Perception 负责理解环境；
- Interaction 负责与环境产生作用；
- Agent 负责任务规划和决策；
- Sim-to-Real 负责实际部署。

这篇综述的主要价值是帮助建立领域地图，为后续深入学习：

- Robot Manipulation
- Diffusion Policy
- Vision-Language-Action Models
- World Models

提供基础。