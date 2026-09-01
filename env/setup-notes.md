# 仿真环境装配记录

日期：2026-09-01
机器：WSL2 Ubuntu 22.04 / RTX 5060 Laptop 8GB

## 最终可用配置

- 渲染后端：`export MUJOCO_GL=egl`
- 主环境 `~/venvs/embodied` (Python 3.10)：torch 2.13+cu130, mujoco 3.12, gymnasium
- LIBERO 环境 `~/venvs/libero` (Python 3.10)：torch 2.13+cu130, **mujoco 2.3.7**, robosuite 1.4.0, numpy 1.22.4
- 激活：`source ~/venvs/<name>/bin/activate`
- LIBERO 配置文件：`~/.libero/config.yaml`

验证通过：LIBERO 环境创建 + 渲染，128x128 图像非零像素 25436。

## 五个关键结论

1. **不要用 conda 装包**。conda 的 HTTP 层超时阈值极紧，curl 能通它也连不上。
   改用 venv + pip + 清华源，全程顺利。

2. **不要照抄 LIBERO README 的 torch 版本**。官方写 `torch==1.11.0+cu113`，
   那是 2022 年的组合，不支持 RTX 5060 (Blackwell)。装最新版 torch 完全正常。

3. **必须降级 mujoco 到 2.3.7**。robosuite 1.4.0 (2023) 读不了 mujoco 3.x 的模型，
   报 `assert joint_type in (mjJNT_HINGE, mjJNT_SLIDE)` AssertionError。
   → 通用规律：**traceback 最后一层落在第三方库内部且是断言失败，
     十有八九是依赖之间版本不匹配，不是自己用错 API。**

4. **ManiSkill 放弃**。SAPIEN 依赖 Vulkan，WSL2 的 NVIDIA 驱动缺 Vulkan 图形库
   (`vulkaninfo` 只见 llvmpipe)，连 `obs_mode='state'` 都无法创建环境。
   LIBERO 走 MuJoCo/EGL，不受影响。

5. **调试时不要加 `2>/dev/null`**。LIBERO 首次运行会交互式询问数据集路径，
   屏蔽输出后表现为"程序卡住无响应"，实际是在等输入。

## 网络规律（当日最大时间损耗来源）

- 国内域名 / 纯本地计算 → Clash 切「直连」
- GitHub / HuggingFace / PyTorch 官方源 → Clash 切「规则」
- 全局 TUN 会把国内源也绕到海外，速度可跌至几十 B/s
- 换 VPN 客户端会残留路由（`198.18.x.x` 网关），需 `wsl --shutdown` 清理
- `curl -I` 成功不代表能下大文件（HEAD 请求几百字节，撑不了长连接）
- 下载时看 curl 的 **Current Speed** 列，几十 B/s 就立刻换方案，别等

## 踩过的坑

| 报错 | 原因 | 解法 |
|---|---|---|
| `CMake must be installed` | egl_probe 需编译 | `apt install cmake build-essential` |
| conda 各种 timeout | conda HTTP 层问题 | 改用 venv + pip |
| `Failed to find Vulkan ICD` | WSL 缺 Vulkan 库 | 放弃 ManiSkill |
| `assert joint_type in (...)` | mujoco 3.x 与 robosuite 1.4 不兼容 | `pip install mujoco==2.3.7` |
| Gymnasium 渲染全黑 | 形状正确但非零像素为 0 | 不影响主线，接口可用即可 |
| `D3D12: Removing Device` + 黑屏 | EGL 初始化抢占 GPU | WSL2 正常现象，忽略 |

## 待办

- [ ] 下载 LIBERO 数据集（几十 GB，需稳定网络）
  `python benchmark_scripts/download_libero_datasets.py --datasets libero_spatial --use-huggingface`
