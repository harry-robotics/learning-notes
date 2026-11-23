# Learning Notes

I'm Harry Huang, an Automotive Engineering undergraduate at Wuhan University of Technology. These are notes and exercises from learning embedded systems, computer vision and deep learning. Most of the notes are in Chinese.

> [!NOTE]
> **Repository status**
>
> Since starting research, I’ve updated this repository less often. It now mainly serves as an archive of my learning notes and practice projects. My research code, experiment records and related materials are kept in my private Research workspace.

**Learning Journey** · [English](JOURNEY.en.md) · [中文](JOURNEY.md)

My current research is in 3D scene understanding, with a focus on dynamic scene graphs: how to represent objects and their changing relationships. Longer term, I'm interested in reliable robot manipulation, sim-to-real transfer and what real-world failures can teach us about perception, planning and control.

## A few places to start

- **ESP32.** [Interrupts and PWM](esp32/day-02-pullup-interrupts-pwm.md) records how I read a button press and varied an LED's brightness. My earlier [Arduino car](https://github.com/harry-robotics/arduino-smart-car) has its own repository with a wiring photo and notes on hardware tests.
- **CNNs in PyTorch.** In the [CIFAR-10 exercise](projects/cifar10-cnn/README.md), I adapted a LeNet-style network for color images. The [training script](projects/cifar10-cnn/train.py) shows where the input channels change and how the feature maps flatten before the first fully connected layer.
- **Transformers in PyTorch.** The [encoder exercise](phase2.5-transformer/transformer.py) includes small checks I can use to understand attention, such as whether each row of attention weights sums to one and which positions a causal mask hides.

## Earlier notes

My [NumPy and OpenCV notes](m2-vision/), [neural network foundations](phase1-foundation/) and [simulation setup notes](env/setup-notes.md) are here as well. The [embodied AI reading notes](phase3-embodied-ai/survey-notes/) include an early look at VLA models.

I use AI for explanations, examples and coding help. In my notes I try to record enough of a check or a mistake that I can revisit it and explain the result myself.
