Title: Like top, but for GPUs
Tags: deep learning, gpu
Modified: 2018-01-21 16:46
Summary: Monitoring GPU (Graphical Processing Unit) utilization for deep learning.

Machine learning and deep learning workloads often involve heavy computation. Sometimes it'll be enough to run it
on the CPU (Central Processing Unit), but some types of models such as neural networks and gradient boosted trees
benefit greatly from running on GPU (Graphical Processing Unit). Because shorter experiment iterations are always
preferred (the time of the data scientist/engineer costs money), using GPUs and making sure they are utilised
efficiently is important. In this post we take a look at the tools available for monitoring the GPU usage, focusing
on NVIDIA hardware and GNU/Linux.

## nvidia-smi

[nvidia-smi](https://developer.nvidia.com/nvidia-system-management-interface) is the de facto standard tool when it
comes to monitoring the utilisation of NVIDIA GPUs. It is an application that queries the
[NVML](https://developer.nvidia.com/nvidia-management-library-nvml) (NVIDIA Management Library).
It's installed together with the [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads).

<figure>
  <img src="{attach}static/images/nvidia-smi-screenshot.png" alt="nvidia-smi screenshot"/>
  <figcaption>Example output of nvidia-smi command showing one GPU and a process using it.</figcaption>
</figure>

Let's dig into the output: it seems to have a header with nvidia-smi version and CUDA driver version, both of those
things can be found in other places but it's nice to have them available so quickly without going through the
installed OS packages or Linux kernel module listings.

    :::text
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |===============================+======================+======================|
    |   0  Tesla K80           On   | 00000000:00:1E.0 Off |                    0 |
    | N/A   83C    P0   151W / 149W |   2259MiB / 11439MiB |     97%      Default |
    +-------------------------------+----------------------+----------------------+

The top part of the output has information on each GPU, in the example above there's just one but the
tool supports displaying metrics for multiple GPUs as well. We can see that the GPU is "Tesla K80" which matches
our expectations for the AWS EC2 p2.xlarge instance type. The "0" to the left of the device name is the index
of the GPU, it is the same identifier as we will see in the bottom table in the output. **Perf** with value "P0"
means that the device is set up for maximum performance, rather than for lowest power consumption. The temperature
is 83 degrees Celsius which is not cold but far from being worriesome. I trust AWS to manage the cooling in their
datacenters and would only pay attention to the temperature of my own hardware.

**Persistence-M** stands for "Persistence Mode" where "On" means that the driver will remain loaded even when no apps
are using the GPU. **Pwr:Usage/Cap** is not something I'd pay attention to in case of cloud computing but it's funny
to see the usage exceeding the capacity.

**Disp.A** is for "Display Active" and "Off" means that there isn't a display using the device which again makes sense
for a virtual machine. **Bus-Id** is the GPU's PCI bus ID which by itself is of little interest to the end-user but can
be used to filter nvidia-smi output and only show the stats for a particular device. **Memory-Usage** is one of my
favourites, it shows the amount of memory allocated by the applications out of total amount of memory. Note that
TensorFlow for example would by default pre-allocate most of the GPU memory without actually using it. See
[this post](https://stackoverflow.com/questions/34199233/how-to-prevent-tensorflow-from-allocating-the-totality-of-a-gpu-memory)
if that's not desired.

**Volatile Uncorr. ECC** is a counter of uncorrectable ECC memory errors since the last driver load. **GPU-Util**
indicates that over the last polling interval the GPU was utilised 96% of the time. A low value here can indicate that
GPU is underused which can be the case if the code spends a lot of time in other places (reading mini-batches
from disk for example). **Compute M.** indicates the shared access mode where the default setting allows multiple
clients to access the CPU concurrently.

    :::text
    +-----------------------------------------------------------------------------+
    | Processes:                                                       GPU Memory |
    |  GPU       PID   Type   Process name                             Usage      |
    |=============================================================================|
    |    0      4631      C   ...naconda3/envs/toxic-comments/bin/python  2248MiB |
    +-----------------------------------------------------------------------------+

The table in the bottom part of the nvidia-smi output describes the processes that are currently using the GPUs:

* **GPU** refers to the index of the device that we observed in the upper left table. It is useful in case of multi-GPU
  setup and allows to see which device in particular is used where.
* **PID** is the process ID, handy when there are multiple processes working with the GPU.
* **Type** where "C" is for "Compute", "G" is for graphics and "C+G" is when the process uses the GPU for both.
* **Process name** is self-explanatory and can be found in ps or top by using the PID.
* **GPU Memory Usage** is how much GPU memory does this particular process use. Interesting to see that the total usage
  of 2259MiB is slightly greater than the sum of "all" per-process usages of 2248MiB.

All of these metrics are described in more details in the nvidia-smi manual page.

### Not just monitoring

nvidia-smi is more than just a monitoring tool, in fact, it supports changing some of the settings we looked at such as
persistence and compute modes. It also has a daemon to speed up the queries. Refer to the man page if you want to know
more.

### Interactive usage

Running nvidia-smi continuously can be done in two ways:

* Built-in `--loop` flag:

        :::shell-session
        $ nvidia-smi --loop=1

    works nicely to report the metrics every second, but appends each update to the stdout instead
    of rewriting the previous values.

* `watch` command available on most Unix-like OS is another option:

        :::shell-session
        $ watch --interval 1 nvidia-smi

    invokes nvidia-smi every second and re-draws the output on the screen.

In both cases, use Ctrl+C to quit the refresh loop.

### Machine-readable output

nvidia-smi can produce files XML and CSV output. The following command produces a CSV line per second with a short
summary of the processes using the GPU:

    ::::shell-session
    $ nvidia-smi --format=csv,noheader \
        --query-compute-apps=timestamp,gpu_name,pid,used_memory \
        --loop=1
    2018/01/21 18:54:28.513, Tesla K80, 4631, 2248 MiB
    2018/01/21 18:54:29.513, Tesla K80, 4631, 2248 MiB
    2018/01/21 18:54:30.513, Tesla K80, 4631, 2248 MiB
    2018/01/21 18:54:31.514, Tesla K80, 4631, 2248 MiB

The output can be redicted to a file using the `--filename=FILE` command-line argument and then consumed by a
monitoring tool of your choice that supports CSV input.

## Nvtop

> [Nvtop](https://github.com/Syllo/nvtop) stands for NVidia TOP, a (h)top like task monitor for
> NVIDIA GPUs. It can handle multiple GPUs and print information about them in a htop familiar way.

<figure>
  <img src="{attach}static/images/nvtop-screenshot.png" alt="Nvtop screenshot"/>
  <figcaption>Nvtop screenshot showing one GPU and a process using it.</figcaption>
</figure>

## gpustat

[gpustat](https://github.com/wookayin/gpustat) offers a minimalistic view of the GPU usage. It is a Python app
using NVML and can be easily installed with pip.

<figure>
  <img src="{attach}static/images/gpustat-screenshot.png" alt="gpustat screenshot"/>
  <figcaption>gpustat screenshot showing one GPU and a process ran by 'ubuntu' user utilising it.</figcaption>
</figure>

I found that
`watch --color --no-title --interval=1 gpustat --color` command is a reasonably good choice: it keeps the colour
output of gpustat, refreshes every second and hides the title with current time which `watch` adds by default
(it's not needed because gpustat prints a timestamp itself).

## Other top-like utilities for NVIDIA

There are more projects aiming to have a familiar top-like interface for GPU usage stats:

* [nvidia_gpu_top](https://github.com/JesseBuesking/nvidia_gpu_top) - a Python app that queries NVML.
* [nvidia-top](https://github.com/abhishekbajpayee/nvidia-top) - a Python wrapper around nvidia-smi.

## Tools for AMD and Intel GPUs

Due to the lack of support of AMD and Intel GPUs in particular or OpenCL in general by modern machine learning
and deep learning frameworks, I will limit the section to some references.

* [radeontop](https://github.com/clbr/radeontop) for AMD devices.
* [intel-gpu-tools](https://01.org/linuxgraphics) for Intel cards.

Both tools are available as packages in Debian and Ubuntu.
