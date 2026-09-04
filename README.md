# Learning Notes

Self-directed learning toward research in **embodied AI**, specifically **Vision-Language-Action (VLA) policy learning**, with autonomous driving as the entry point into embodiment.

Vehicle Engineering undergraduate, Wuhan University of Technology.

---

## What I can do now

- **Transformer from scratch** — attention → multi-head → full block → positional encoding, implemented and verified. Trained a character-level GPT to confirm the pipeline actually learns.
- - **Simulation environment** — MuJoCo + LIBERO configured on WSL2 (RTX 5060, Blackwell). 
  Rendering verified: 128×128 dual-camera output, 25,436 non-zero pixels, full object 
  poses recovered.
- **CNN image classification** — MNIST → CIFAR-10 transfer, with analysis of where the bottleneck comes from.
- **Reproduction debugging** — invariant checks, initial-loss validation, dependency version conflict diagnosis.

**Currently working toward**: reproducing Diffusion Policy / ACT on LIBERO.

---

## Contents

| Directory | Description |
|---|---|
| **[phase2.5-transformer](./phase2.5-transformer)** | Transformer implementation, mini-GPT training, ViT structure |
| **[env](./env)** | Simulation setup and troubleshooting notes (MuJoCo / LIBERO / robosuite) |
| **[projects](./projects)** | Standalone projects: CIFAR-10 classifier, lane detection, feature matching |
| [phase2-CNN-pytorch](./phase2-CNN-pytorch) | PyTorch fundamentals and CNNs |
| [phase1](./phase1) | Classical computer vision |
| [m2-vision](./m2-vision) | OpenCV image processing |
| [esp32](./esp32) | Embedded development (smart car) |

Notes are written in Chinese; code and documentation structure in English.

---

## Three things worth a look

**1. [`phase2.5-transformer/transformer-essentials.md`](./phase2.5-transformer/transformer-essentials.md)**

A distilled summary written after implementing Transformer. The organizing idea: a Transformer is a **residual stream running through the whole network** — attention moves information horizontally across positions, the FFN refines it vertically within each position, alternating for N layers. This single picture explains why the shape must be preserved, why residual connections exist, and why the architecture stacks to 96 layers.

The last section identifies the three interfaces that architecture papers actually modify — **where Q comes from, how the mask is designed, and how inputs are concatenated** — which I use to locate a paper's contribution quickly.

**2. [`env/setup-notes.md`](./env/setup-notes.md)**

Complete troubleshooting record for the LIBERO setup. One generalizable rule came out of it: **when the last frame of a traceback lands inside a third-party library and is an assertion failure, it is almost always a dependency version mismatch rather than incorrect API usage.** In this case, robosuite 1.4.0 could not parse MuJoCo 3.x models and had to be downgraded to 2.3.7.

**3. [`projects/cifar10-cnn`](./projects/cifar10-cnn)**

LeNet transferred from MNIST to CIFAR-10, reaching 52.92% test accuracy. The number is low, and the point of the writeup is why: LeNet is a 1998 architecture missing batch normalization and residual connections. The analysis is in the project README.

---

## How I work

- **Output over input.** Each phase must produce runnable code and verifiable results. Finishing a course does not count as finishing a phase.
- **Record failures.** Troubleshooting notes are kept alongside working code — the environment setup document alone will save days when I move to a lab machine.
- **Separate what to internalize from what to look up.** Explicitly categorizing knowledge as *must internalize / look up when needed / safe to forget* keeps attention on what matters.

More in [`JOURNEY.md`](./JOURNEY.md).

---

## Next

- [ ] Reproduce Diffusion Policy / ACT on LIBERO to baseline level. Note that LIBERO is largely saturated (>95% is standard on Spatial/Goal/Object), so this is a **learning milestone, not a research result**.
- [ ] Analyze failure modes of the reproduction to find a problem worth pursuing.
- [ ] Track VLA research: efficiency, data quality quantification, evaluation methodology.

---

**Contact**: harry.huang.eng@outlook.com
