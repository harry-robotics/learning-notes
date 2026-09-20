# Survey 3: Vision-Language-Action Models

## Survey Information

| Item | Description |
|---|---|
| Topic | Vision-Language-Action Models |
| Research Area | Embodied AI / Robot Foundation Models |
| Purpose | 理解大模型如何赋予机器人更强的理解和行动能力 |
| Main Focus | VLA Architecture, Data, Planning, Physical Grounding |
| Learning Connection | Robot Learning, Manipulation, Foundation Models |

---

# 1. Overview

Vision-Language-Action (VLA) 是近年来 Embodied AI 中的重要研究方向。

其目标是将：

- Vision（视觉）
- Language（语言）
- Action（动作）

统一到一个模型框架中，使机器人能够理解人类指令，并生成对应动作。


传统机器人系统通常采用：

**Perception → Planning → Control**

不同模块分别完成：

- 环境理解；
- 任务规划；
- 动作执行。


VLA 尝试建立：

**Vision + Language → Action**

的端到端学习方式。

---

# 2. Why VLA Emerged

## Limitations of Traditional Robot Learning

传统机器人方法通常面向：

- 固定环境；
- 固定任务；
- 特定物体。


主要问题：

| Problem | Description |
|---|---|
| Limited Generalization | 难以适应新环境和新任务 |
| Language Understanding | 难理解复杂自然语言指令 |
| System Complexity | 多模块之间存在信息损失 |
| Data Scaling | 难利用大规模数据提升能力 |

例如：

传统系统可能能够完成：

“抓取固定位置的杯子”

但面对：

“把桌上的红色杯子放进厨房柜子”

需要同时理解：

- 语言；
- 场景；
- 目标；
- 动作。


---

# 3. Foundation Models and Robotics

VLA 的发展受到 Vision-Language Model (VLM) 和 Large Language Model (LLM) 的推动。


Foundation Model 提供：

| Capability | Function |
|---|---|
| Visual Understanding | 理解图像内容 |
| Language Understanding | 理解自然语言 |
| Semantic Reasoning | 推理任务目标 |
| Knowledge Transfer | 利用已有知识泛化 |


机器人领域希望进一步加入：

Action Representation（动作表示）

使模型能够从：

理解世界

发展到：

影响世界。

---

# 4. VLA Architecture

目前 VLA 主要分为两类：

| Type | Description |
|---|---|
| Monolithic VLA | 单一模型完成视觉、语言理解和动作生成 |
| Hierarchical VLA | 高层推理和低层动作策略分离 |

---

# 5. Monolithic VLA

## Core Idea

一个模型直接学习：

**Observation + Language Instruction → Action**

类似语言模型：

Text → Token

VLA：

Vision/Language → Action


---

## Advantages

| Advantage | Description |
|---|---|
| Simple Architecture | 减少模块连接 |
| Strong Semantic Ability | 利用大模型知识 |
| Better Generalization Potential | 可以利用大规模预训练 |


---

## Limitations

### Interpretability

模型难以解释：

为什么选择某个动作。


### Physical Grounding

模型可能理解：

“杯子”

但不一定理解：

杯子的重量、稳定性、碰撞关系。


### Control Difficulty

高层语义输出与低层机器人控制之间存在差距。


---

# 6. Hierarchical VLA

## Core Idea

将任务拆分为：

High-level Reasoning → Low-level Policy


例如：

高层：

“把杯子放到桌上”


低层：

生成具体机械臂动作。


---

## Advantages

| Advantage | Description |
|---|---|
| Easier Debugging | 模块更加清晰 |
| Better Interpretability | 更容易理解决策过程 |
| Flexible Deployment | 可以替换不同模块 |


---

## Limitations

模块之间可能产生：

- 信息损失；
- 错误传播；
- 系统复杂度增加。


---

# 7. VLA and Robot Manipulation

VLA 当前主要应用于 Robot Manipulation。

原因：

机器人操作同时需要：

- 视觉理解；
- 语言理解；
- 动作生成。


任务示例：

输入：

“拿起桌上的蓝色盒子”


模型需要完成：

| Step | Capability |
|---|---|
| 1 | 理解语言目标 |
| 2 | 定位目标物体 |
| 3 | 规划操作方式 |
| 4 | 生成动作 |

---

# 8. Current Challenges


## 8.1 Long Horizon Tasks

短任务：

抓取物体

相对容易。


长任务：

整理房间、完成复杂流程

更加困难。


原因：

- 多步骤误差累积；
- 缺少长期记忆；
- 缺少任务恢复机制。


未来需要：

- Memory Mechanism；
- Long-term Planning。


---

## 8.2 Physical Grounding

当前 VLA 主要依赖：

视觉和语言中的统计规律。


问题：

模型可能知道：

“杯子通常在桌子上”

但不一定理解：

“推动杯子会导致它移动或掉落”。


需要增强：

- 3D Understanding；
- Physics Knowledge；
- World Model。


---

## 8.3 Robot Data Scaling

机器人数据相比互联网数据更加困难。


原因：

| Problem | Description |
|---|---|
| High Collection Cost | 需要真实机器人采集 |
| Embodiment Difference | 不同机器人结构不同 |
| Long-tail Distribution | 少见任务不足 |


未来需要：

- 大规模机器人数据集；
- Simulation Data；
- Autonomous Data Collection。


---

## 8.4 Deployment Efficiency

大型 VLA 模型部署需要考虑：

| Challenge | Description |
|---|---|
| Latency | 推理速度 |
| Memory | 模型大小 |
| Hardware | 计算资源限制 |


研究方向：

- Model Compression；
- Quantization；
- Efficient Architecture。


---

# 9. Future Directions


## 9.1 Memory and Long-term Planning

目标：

让机器人能够保存经验，并支持长期任务。


发展方向：

**Interaction → Experience → Memory → Improved Capability**


---

## 9.2 3D/4D Perception

当前 VLA 主要依赖：

2D Image。


但真实机器人需要理解：

- 空间结构；
- 深度信息；
- 物体运动；
- 时间变化。


发展趋势：

**2D Vision → 3D Scene Understanding → 4D Dynamic Perception**


---

## 9.3 Mobile Manipulation

真实环境中的机器人通常需要：

移动 + 操作。


例如：

家庭机器人：

移动到目标位置 → 寻找物体 → 完成操作。


挑战：

- Navigation 与 Manipulation 融合；
- 动态环境适应；
- 全身协调控制。


---

## 9.4 Lifelong Learning

当前模型：

训练完成 → 固定能力。


未来机器人需要：

持续交互 → 获取经验 → 更新能力。


---

# 10. Critical Understanding

VLA 的核心价值：

让机器人拥有更强的：

- 视觉理解能力；
- 语言交互能力；
- 任务泛化能力。


但是，实现通用机器人仍需要解决：

| Capability | Current Limitation |
|---|---|
| Semantic Understanding | 语言和视觉能力较强 |
| Physical Understanding | 物理推理不足 |
| Long-term Execution | 长任务能力不足 |
| Data Scaling | 数据获取困难 |
| Deployment | 计算成本较高 |


未来方向可能需要结合：

**Vision-Language Understanding + World Model + Physical Interaction + Efficient Control**

---

# Learning Summary

VLA 可以理解为：

传统机器人：

**Perception → Planning → Control**

向：

**Vision + Language → Action**

发展的尝试。


它连接了：

- Foundation Models；
- Robot Learning；
- Manipulation；
- World Models。


后续学习重点：

- VLA architecture；
- Robot datasets；
- Action representation；
- 3D/4D perception；
- Efficient deployment。