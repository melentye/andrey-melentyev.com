Title: PlaidML on Apple Metal benchmark
Tags: plaidml, amd, intel, gpu, apple metal, opencl, performance
Summary: Comparison of PlaidML performance using OpenCL and Apple Metal backends.

Thought I'd help PlaidML to benchmark [Apple Metal](https://developer.apple.com/metal/) backend which
was [recently announced](http://vertex.ai/blog/accelerated-deep-learning-on-macos).
It looks like on Intel GPUs there's somewhat of a performance penalty using Apple Metal compared to OpenCL
while on Radeon Pro 555 (which also happens to be the only remotely powerful GPU I have around) the execution
time improved from 15.3 seconds to 9.46 on average.

Device | Backend | Mean Execution (s) | Stddev Execution (s) |
------ | ------- | ------------------ | -------------------- |
metal_intel_hd_graphics_5000.0 | Metal | 30.3884871 | 0.3806514578 |
hd_graphics_5000.0 | OpenCL  | 28.92962003 | 0.772196669 |
metal_intel(r)_hd_graphics_630.0 | Metal | 41.36494128 | 0.1281149304 |
intel(r)_hd_graphics_630.0 | OpenCL | 26.78535573 | 0.1107274138 |
metal_amd_radeon_pro_460.0 | Metal | **9.464677016** | 0.4562651004 |
amd_radeon_pro_555_compute_engine.0 | OpenCL | **15.30082059** | 0.02495138757 |

## Measurements

Three devices, six runs each: three on OpenCL and three on Metal.

* MacBookAir6,2, Intel HD Graphics 5000 1536 MB
* MacBookPro14,3, Intel HD Graphics 630 1536 MB
* MacBookPro14,3, Radeon Pro 555 2048 MB

Device | Compile | Execution | Execution per example
------ | ------- | --------- | ---------------------
metal_intel_hd_graphics_5000.0 | 5.274222136 | 30.82639313 | 0.03010389954
metal_intel_hd_graphics_5000.0 | 0.78429389 | 30.20231009 | 0.02949444344
metal_intel_hd_graphics_5000.0 | 0.7879936695 | 30.13675809 | 0.02943042782
hd_graphics_5000.0 | 3.790126085 | 28.50454235 | 0.02783646714
hd_graphics_5000.0 | 3.435862064 | 28.46335888 | 0.02779624891
hd_graphics_5000.0 | 3.327329874 | 29.82095885 | 0.02912203013
metal_amd_radeon_pro_460.0 | 3.464589834 | 9.987387896 | 0.009753308492
metal_amd_radeon_pro_460.0 | 0.538659811 | 9.146244049 | 0.008931878954
metal_amd_radeon_pro_460.0 | 0.5391671658 | 9.260399103 | 0.009043358499
amd_radeon_pro_555_compute_engine.0 | 2.78721118 | 15.32924485 | 0.01496996568
amd_radeon_pro_555_compute_engine.0 | 0.5374057293 | 15.28253198 | 0.01492434763
amd_radeon_pro_555_compute_engine.0 | 0.5268480778 | 15.29068494 | 0.01493230951
metal_intel(r)_hd_graphics_630.0 | 6.320588112 | 41.4576509 | 0.04048598721
metal_intel(r)_hd_graphics_630.0 | 0.6090488434 | 41.21875095 | 0.04025268648
metal_intel(r)_hd_graphics_630.0 | 0.5894200802 | 41.41842198 | 0.04044767772
intel(r)_hd_graphics_630.0 | 3.034727097 | 26.70475197 | 0.02607885934
intel(r)_hd_graphics_630.0 | 0.5449151993 | 26.73970509 | 0.02611299325
intel(r)_hd_graphics_630.0 | 0.5301389694 | 26.91161013 | 0.02628086926
