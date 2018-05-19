Title: Hardware acceleration for deep learning
Tags: deep learning, cpu, gpu, tpu, nvidia, amd, intel
Summary: A bird's-eye view on the hardware acceleration for training deep neural networks.

This is the first post in a series on deep learning model training infrastructure. The preliminary list of topics:

* Hardware acceleration for deep learning (this post).
* Software stack and deep learning framework support for GPUs.
* Scaling up: using multiple GPUs on a single machine.
* Scaling out: distributed training.

## Problem statement

People working with neural networks may not always like it when their work is described as a "pile of linear algebra",
but thinking of deep learning systems this way helps to understand the importance of hardware acceleration.

<figure>
  <img src="{attach}static/images/xkcd-machine-learning.png" alt="ML is a pile of linear algebra"/>
  <figcaption>Figure 1. <a href="https://xkcd.com/1838/">xkcd</a> comic half-jokingly refers to ML
  system as a pile of linear algebra.</figcaption>
</figure>

A popular computer vision neural network architecture VGG-16, for example,
[requires](http://imatge-upc.github.io/telecombcn-2016-dlcv/slides/D2L1-memory.pdf) an order of 10<sup>10</sup>
floating-point operations (FLOPs) for a single forward pass - mostly matrix multiplications and additions. Training
a neural network on a dataset of N samples for E epochs will require N * E forward passes and as many backward
passes.

The large total amount of computation makes it necessary for the researchers and engineers to optimise the performance:
it makes a huge difference whether model training takes an hour or a full day, shorter cycles allow for faster
experimentation and therefore shorter time until hypotheses are <s>dis</s>proven.

### Processing units

So we need a lot of computational power, that's cool - computers have **central processing units** (CPUs), what if we
were to use one? Unfortunately, CPUs are not that great at running a massive amount of floating-point operations
simultaneously. Luckily for DL practitioners, parallel floating-point computation is something that
**graphical processing units** (GPUs) are good at! Yes, the same computer parts we use to play video games. 

It turns out that GPUs:

* Can perform **more floating-point operations per second** (FLOPS) than CPUs.
* Have better **memory bandwidth**, i.e. GPU cores read data from GPU RAM and write it back faster.

These advantages come with tradeoffs:

* The GPUs have a much more **limited amount of memory**, it ranges between 16GB and 24GB for newer models, while for a CPU
  it is not impossible to get a machine with 1TB RAM.
* An additional step is required to **transfer data into the GPU memory** from system RAM.

<figure>
  <img src="{attach}static/images/cpu-vs-gpu.png" width="309" height="198" alt="CPU and GPU number of cores and clock speed"/>
  <figcaption>Figure 2. CPUs usually have just a few cores, while GPUs may have thousands.
  CPUs, however, have higher clock speed per core. All in all, GPUs can perform more FLOPs per second.
  Excuse lack of ticks on the plot, the absolute values are not important here.</figcaption>
</figure>

In 2016, Google announced **Tensor Processing Unit** (TPU) - hardware specifically designed to accelerate
deep learning workloads, sometimes referred to as ASIC - application specific integrated circuit. It is not available for
purchase, instead, it can be rented via Google Cloud Platform. Such TPU offers better performance compared to top GPUs
while keeping the total training costs
[very reasonable](https://blog.riseml.com/comparing-google-tpuv2-against-nvidia-v100-on-resnet-50-c2bbb6a51e5e). At
the moment of writing, the only DL framework supporting TPUs is TensorFlow, but PyTorch dev team is
[working on integration too](https://twitter.com/soumithchintala/status/963072442510974977).

Intel [announced](https://ai.intel.com/intel-nervana-neural-network-processors-nnp-redefine-ai-silicon/) **Nervana**
neural network processor, an ASIC for machine learning, in 2017 but so far hasn't delivered one.

### Improved parallelism in modern CPUs

Newer CPU models support **Advanced Vector Extensions** (AVX). AVX is a single instruction multiple data (SIMD)
instruction set, meaning that the cores can perform the same operation on multiple data points simultaneously,
similar to how GPU does it.

<figure>
  <img src="{attach}static/images/intel-skylake-cpu.jpg" height="200" width="200" alt="Intel Core i7 CPU"/>
  <figcaption>Figure 3. Intel Core i7 6700K Skylake CPU supports AVX2.
  Photo by <a href="https://commons.wikimedia.org/wiki/User:Sting">Eric Gaba</a>.</figcaption>
</figure>

Intel's top processor at the time of writing is Xeon Phi 7290, code name Knights Landing.
It features 72 cores with AVX-512 and has a peak performance of 3456 double-precision giga-floating point
operations per second (DP GFLOPS) which is comparable to that of NVIDIA Tesla K80 GPU from 2014 yet
significantly lower than 7800 DP GFLOPS in latest NVIDIA Tesla V100 GPU. However, we're no longer looking
at an order of magnitude difference between CPU and GPU  as it was the case [before](https://www.karlrupp.net/2016/08/flops-per-cycle-for-cpus-gpus-and-xeon-phis/).

## GPU manufacturers

Two major manufacturers of high-end GPUs are **NVIDIA** and **AMD**. As of mid-2018, NVIDIA is a de facto standard
when it comes to GPU acceleration for deep learning. This is mainly due to its mature software ecosystem which
in turn leads to wide support by deep learning frameworks. The largest cloud providers, AWS, GCP and Azure, 
all offer virtual machines with NVIDIA GPUs. There's also a number of smaller vendors such as Paperspace, Crestle
or Floydhub that allow renting NVIDIA GPUs. Google Colab [offers GPUs for free](https://medium.com/deep-learning-turkey/google-colab-free-gpu-tutorial-e113627b9f5d),
Kaggle has recently [announced GPU-powered kernels](https://www.kaggle.com/dansbecker/running-kaggle-kernels-with-a-gpu),
both platforms use NVIDIA Tesla K80 GPUs.

For AMD GPUs, to my knowledge, there's just one provider called [GPUEater](https://www.gpueater.com/).

Even though it is theoretically possible to utilise **Intel** GPUs for deep learning via OpenCL, the performance
will not be competitive with NVIDIA and AMD.

## What does it all mean

In practice, it means that you never not want to use the GPU or TPU for deep learning. The exact speed up to expect
from using a GPU vs. a CPU depends on the network architecture, input pipeline design and other factors, but an order of
magnitude improvement in training performance is not an exception. 

The reality is that in order to be able to focus on the actual modelling, it'll have to be an NVIDIA GPU or Google
TPU because of the software support. It is possible to get a GPU for free for a short period of time on Kaggle or Colab.
Renting from cloud providers is a viable option for more serious experiments, and buying can be a good idea depending on
the usage patterns.

In the next post, we will look at the software ecosystem for the GPUs and how deep learning frameworks support the hardware.
