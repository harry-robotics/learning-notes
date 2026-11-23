# Learning Journey

[中文原文](JOURNEY.md) · [Repository home](README.md)

I’m Harry Huang, an Automotive Engineering undergraduate at Wuhan University of Technology. This page follows how I went from building a small Arduino car to studying how robots make sense of their surroundings.

## November 2026 · From robot learning to scene understanding

I’m now studying 3D scene understanding, with a focus on dynamic scene graphs. I first came to embodied AI through robot manipulation and vision-language-action (VLA) models. I wanted to understand how a robot could follow an instruction. That led me to an earlier question in the process: how does a robot know what is around it and what has changed?

My longer-term interests are reliable robot manipulation, sim-to-real transfer and real-world deployment. I’d like to understand how a problem we see during a real task can point back to something we could improve in perception, planning or control.

Since starting research, I’ve updated this repository less often. My research code, experiment records and related materials are kept in my private Research workspace.

## October–November 2026 · Working with AI in research

I’ve started relying more on AI to write code and run experiments. I also talk through my ideas with it. Sometimes it spots something I missed, and I change my mind. Sometimes it gives me code that runs right away, and that’s when I have to pause and ask myself: if it produces the result I expected, will that result actually answer my question?

The skills I want to develop are making sound judgments, deciding what to do next and checking the evidence for myself. Before I run an experiment, I should be able to explain why the question matters and what would make the comparison fair. Afterwards, I should be able to go back to the original records and see exactly what the experiment tested and which explanations are still possible.

One of the harder decisions is when to stop. Once I’ve put time into an idea, it takes some nerve to admit that the question is too broad or that the evidence can’t tell several explanations apart. I want to get better at making that call and bringing what I learned into the next project.

If my name goes on a paper, I’m responsible for the decisions I made and the numbers I report. If someone points to a number and asks where it came from, I should be able to find the original record, explain how it was calculated and say what conclusion it supports. That responsibility is mine even when AI helped write the code.

## September 2026 · Learning to ask a research question

I set up MuJoCo and LIBERO and read surveys on embodied AI, manipulation and VLA models. The surveys helped me see how different groups approached similar problems. I began reading individual papers to see what their experiments actually tested, where the systems struggled and what questions were still open. That gave me a more concrete reason to learn a new method when I needed one.

## July–August 2026 · Getting started with deep learning

I studied computer vision with OpenCV and worked through [CNN](projects/cifar10-cnn/README.md) and [Transformer](phase2.5-transformer/transformer.py) exercises in PyTorch. After studying Transformers, I could explain attention and feed-forward layers in isolation, but I struggled to explain how a whole block worked. Tracing what happened to the input at each layer helped me connect the pieces. I began spending more time checking whether I could explain how a system worked after putting the tutorial away.

## Spring 2026 · Embedded systems

I started with an [Arduino car](https://github.com/harry-robotics/arduino-smart-car) and later explored [ESP32](esp32/day-02-pullup-interrupts-pwm.md). The car responded to Bluetooth commands in my tests, and the obstacle avoidance still needed work. Getting the car onto the floor made it much easier to see which of my assumptions held up. I still think about that when I read about systems that have only been tested in simulation.

*Last updated: 2026-11-23*
