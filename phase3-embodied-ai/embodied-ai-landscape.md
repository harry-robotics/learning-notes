# Embodied AI Research Landscape

## Overview

Embodied AI（具身智能）研究如何让智能体（Agent）通过物理载体（Embodiment）与环境进行交互，并完成感知、理解、决策和行动。

与传统 AI 系统相比，Embodied AI 不仅关注模型的信息处理能力，还关注智能体如何在真实世界中行动，并通过环境反馈不断调整行为。

整体闭环：

**Environment → Perception → Understanding → Planning → Action → Feedback**

---

# 1. Embodied AI System Architecture

一个典型 Embodied AI 系统可以划分为以下模块：

| Module | Function | Typical Methods |
|---|---|---|
| Perception（感知） | 获取并理解环境信息 | Computer Vision, 3D Understanding, VLM |
| Planning（规划） | 根据目标制定任务策略 | LLM Planning, VLM Planning |
| Action Modeling（动作建模） | 将任务转化为具体动作 | Imitation Learning, Reinforcement Learning, Diffusion Policy, VLA |
| Control（控制） | 执行底层运动控制 | Motion Control, Robot Control |

整体过程：

**Environment → Perception → Planning → Action Modeling → Control → Environment Feedback**

这些模块共同构成从“理解世界”到“改变世界”的过程。

---

# 2. Main Research Directions

## 2.1 Embodied Perception（具身感知）

Embodied Perception 研究智能体如何获得并理解环境信息。

主要方向：

| Direction | Description |
|---|---|
| Visual Perception | 从视觉输入中提取环境信息 |
| 3D Scene Understanding | 理解空间结构和物体关系 |
| Active Perception | 主动获取更有效的信息 |
| Visual Language Navigation (VLN) | 根据语言指令完成导航 |

核心问题：

> 智能体如何形成对环境的有效表示？

研究趋势：

**2D Vision → 3D Understanding → 4D Dynamic Perception**

---

## 2.2 Embodied Interaction（具身交互）

Embodied Interaction 关注智能体如何与人和环境产生交互。

主要任务：

| Task | Description |
|---|---|
| Embodied Question Answering (EQA) | 根据环境信息回答问题 |
| Grasping | 获取物体 |
| Manipulation | 操作环境中的对象 |
| Human-Robot Interaction | 与人进行协作 |

简单理解：

| Concept | Question |
|---|---|
| Perception | 世界是什么？ |
| Interaction | 如何影响世界？ |

---

## 2.3 Embodied Agent（具身智能体）

Embodied Agent 研究如何让机器人自主完成复杂任务。

主要包括：

## Task Planning（任务规划）

核心问题：

**What should the agent do?**

例如：

目标：

“准备一杯咖啡”

任务分解：

寻找杯子 → 加入咖啡 → 倒水

常见方法：

- LLM Planning
- VLM Planning
- Symbolic Planning


## Action Planning（动作规划）

核心问题：

**How should the agent do it?**

例如：

- 如何移动机械臂？
- 如何生成动作轨迹？
- 如何控制机器人执行？

常见方法：

- Imitation Learning
- Reinforcement Learning
- Diffusion Policy
- VLA Policy

---

# 3. Robot Manipulation（机器人操作）

Robot Manipulation 是 Embodied AI 实现物理交互的重要方向。

主要任务：

| Task | Example |
|---|---|
| Grasping | 抓取物体 |
| Basic Manipulation | 移动、放置 |
| Dexterous Manipulation | 灵巧操作 |
| Deformable Object Manipulation | 柔性物体操作 |
| Mobile Manipulation | 移动平台上的操作 |

发展趋势：

**Single Task → Multi-task → Open-world Manipulation**

---

# 4. Vision-Language-Action (VLA)

Vision-Language-Action（VLA）是近年来 Embodied AI 的重要方向。

目标：

将：

- Vision（视觉）
- Language（语言）
- Action（动作）

结合，使机器人能够理解自然语言指令并生成对应行为。


例如：

输入：

“把桌上的红色杯子放到架子上”

模型需要完成：

语言理解 → 目标定位 → 任务规划 → 动作生成


VLA试图推动机器人从：

“执行固定程序”

发展到：

“理解任务并自主行动”。

---

# 5. Sim-to-Real Adaptation（仿真到现实迁移）

Sim-to-Real 研究如何将仿真环境中学习到的能力迁移到真实世界。

主要挑战：

| Challenge | Description |
|---|---|
| Visual Gap | 仿真与现实视觉差异 |
| Physics Gap | 动力学和物理规律差异 |
| Data Gap | 数据分布差异 |

Simulation 的优势：

- 数据生成成本低；
- 环境可重复；
- 方便算法测试。

---

# 6. Current Challenges

## Data Scaling

机器人数据相比互联网数据更难获取。

主要问题：

- 数据采集成本高；
- 不同机器人之间存在差异；
- 长尾任务覆盖不足。


## Generalization

机器人需要适应：

- 新物体；
- 新环境；
- 新任务。


## Physical Understanding

当前模型能够处理视觉和语言信息，但仍需要增强对真实物理规律的理解。


## Long Horizon Tasks

复杂任务需要：

- 长期规划；
- 记忆能力；
- 错误恢复能力。


## Deployment Efficiency

大型模型实际部署需要考虑：

- 推理速度；
- 内存占用；
- 硬件限制。

---

# 7. Future Directions

## World Model（世界模型）

目标：

让模型学习环境变化规律，并预测未来状态。

核心问题：

不仅知道：

“现在是什么”

还需要理解：

“执行某个动作后会发生什么”。

---

## 3D/4D Perception

研究方向：

**2D Image Understanding → 3D Scene Understanding → 4D Dynamic World Understanding**

关注：

- 空间结构；
- 时间变化；
- 物体交互。


---

## Lifelong Learning（持续学习）

目标：

让机器人通过持续交互积累经验，并不断提升能力。


---

## General-purpose Robot Intelligence

探索能够适应多任务、多环境的通用机器人智能系统。

---

# Learning Summary

Embodied AI 可以理解为一个完整智能系统：

**Environment → Perception → Understanding → Planning → Action → Feedback**

不同研究方向主要解决其中不同环节：

| Research Area | Main Question |
|---|---|
| Perception | 如何理解环境？ |
| Planning | 如何决定任务？ |
| Manipulation | 如何操作世界？ |
| VLA | 如何连接视觉、语言和动作？ |
| World Model | 如何预测环境变化？ |
| Sim-to-Real | 如何从仿真走向现实？ |

通过建立领域地图，可以进一步学习：

- Robot Learning
- Diffusion Policy
- Vision-Language-Action Models
- 3D/4D Perception
- World Models
