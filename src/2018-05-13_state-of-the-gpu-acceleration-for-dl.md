Title: State of the GPU acceleration for deep learning
Tags: deep learning, gpu, tensorflow, theano, chainer, pytorch, plaidml, rocm, cuda, opencl, nvidia, amd, cupy, apple metal
Status: draft
Summary: Bird's-eye view on the graphical processing unit (GPU) and tensor processing unit (TPU) training acceleration support in modern deep learning frameworks.

## Problem statement

People in the industry may not always like it when the result of their work is reduced to a "pile of linear algebra",
but thinking of deep learning systems this way helps understand the importance of hardware acceleration.

<figure>
  <img src="{attach}static/images/xkcd-machine-learning.png" alt="ML is a pile of linear albegra"/>
  <figcaption>Figure 1. <a href="https://xkcd.com/1838/">xkcd</a> comic half-jokingly describes ML
  system as a pile of linear algebra.</figcaption>
</figure>

A popular computer vision neural network architecture VGG-16, for example,
[requires](http://imatge-upc.github.io/telecombcn-2016-dlcv/slides/D2L1-memory.pdf) order of 10<sup>10</sup>
floating-point operations (FLOPs) for a forward pass - mostly matrix multiplications and additions. Training a
neural network on a dataset of N samples for E epochs will require N * E forward passes and as many backward
passes.

The large total amount of computation is the reason why researchers and engineers seek to optimise the performance:
it makes a huge difference whether model training takes half an hour or a day, shorter cycles allow for faster
experimentation and therefore shorter time until hypotheses are <s>dis</s>proven.

### Processing units

So we need a lot of compute, that's cool - computers have a **central processing unit** (CPU), what if we were to
use one? Unfortunately, CPUs are not that great at running a massive amount of floating-point operations simultaneously.
Luckily for DL practitioners, parallel floating-point computation is something that **graphical processing units**
(GPUs) are good at! Yes, the same computer parts we use to play video games. 

It turns out that GPUs:

* Can perform **more floating-point operations per second** (FLOPS) than CPUs.
* Have better **memory bandwidth**, i.e. GPU cores read data from GPU RAM and write it back faster.

These advantages come with tradeoffs:

* The GPUs have much more **limited amount of memory**, it ranges between 16GB and 24GB for newer models, while for a CPU
  it is not impossible to get a machine with 1TB RAM.
* An additional step is required to **transfer data into the GPU memory** from system RAM.

<figure>
  <img src="{attach}static/images/cpu-vs-gpu.png" width="309" height="198" alt="CPU and GPU number of cores and clock speed"/>
  <figcaption>Figure 2. CPUs usually have just a few cores, while GPUs may have thousands.
  CPUs, however, have higher clock speed per core. All in all, GPUs can perform more FLOPs per second.
  Excuse lack of ticks on the plot, the absolute values are not important here.</figcaption>
</figure>

In 2016 Google announced their **tensor processing units** (TPUs) - hardware specifically designed to accelerate
deep learning workloads. It is not available for purchase, instead it can be rented via Google Cloud Platform.
Arguably, NVIDIA's latest model Tesla V100 is also a TPU: it features Tensor cores that were developed for deep
learning performance.

### Improved parallelism in modern CPUs

Newer CPU models support **Advanced Vector Extensions** (AVX). AVX is a single instruction multiple data (SIMD)
instruction set, meaning that the processor can perform the same operation on multiple data points simultaneously,
similar to how GPU does it.

<figure>
  <img src="{attach}static/images/intel-skylake-cpu.jpg" height="200" width="200" alt="Intel Core i7 CPU"/>
  <figcaption>Figure 3. Intel Core i7 6700K Skylake CPU, supports AVX2.
  Photo by <a href="https://commons.wikimedia.org/wiki/User:Sting">Eric Gaba</a>.</figcaption>
</figure>

Intel's top processor at the time of writing is Xeon Phi 7290, code name Knights Landing.
It features 72 cores with AVX-512 and has peak performance of 3456 double-precision giga floating-point
operations per second (DP GFLOPS) which is comparable to that of NVIDIA Tesla K80 GPU from 2014 and
significantly lower than 7800 DP GFLOPS in latest NVIDIA Tesla V100 GPU. However, we're no longer looking
at an order of magnitude difference between CPU and GPU  as it was the case [before](https://www.karlrupp.net/2016/08/flops-per-cycle-for-cpus-gpus-and-xeon-phis/).

## GPU manufacturers

NVIDIA
AMD

## What does it all mean

In practice it means that you never not want to use the GPU or TPU for deep learning. Buy one or
rent one, this will drastically reduce the feedback loop

# Apple Metal

> Metal 2 provides near-direct access to the graphics processing unit (GPU)

# HSA

Heterogeneous System Architecture

# NVCC

NVIDIA CUDA compiler - a proprietary LVVM-based compiler from single-source host+device CUDA language extensions 
code to X86 and device binary. Host code compilation is delegated while device code is compiled by NVCC.

# HIP

* HIP C++ language with C++11 features, API similar to CUDA
* The code is portable across NVIDIA and AMD platforms

# HCC: Heterogeneous Compute Compiler

An open-source Clang/LLVM-based compiler from C++ 11/14 to X86 and HSAIL (HSA Intermediate Language).
It produces code where parallelisable parts are offloaded to the GPU while the rest is running on CPU.
The X86 code generation is delegated to other compilers.

# Chainer

Chainer is an open source deep learning framework with a Python API. It supports dynamic computation graphs
and it was the inspiration behind PyTorch. Under the hood Chainer uses CuPy when CUDA is available and
falls back to NumPy when it's not.

CuPy is a NumPy-like API accelerated with CUDA so natually it is designed to run on NVIDIA hardware.
However, CuPy v5 feature list includes an item "AMD GPU support in CuPy via HIP/ROCm".

I personally am very impressed by Chainer's architecture, clean API and the quality of documentation,
despite the fact that it's not backed by any of the tech giants, unlike all other deep learning frameworks.
Look at all the amazing things in their [release notes and roadmap](https://chainer.org/announcement/2018/04/17/released-v4.html).
