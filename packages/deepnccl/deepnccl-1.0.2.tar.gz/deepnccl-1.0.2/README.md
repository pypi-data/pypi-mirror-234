# AIACC-NCCL

Optimized primitives for inter-GPU communication on Aliyun machines.

## Introduction

AIACC-NCCL is an AI-Accelerator communication framework for NVIDIA-NCCL.
It implements optimized all-reduce, all-gather, reduce, broadcast, reduce-scatter, all-to-all, as well as any send/receive based communication pattern.
It has been optimized to achieve high bandwidth on aliyun machines using PCIe, NVLink, NVswitch, as well as networking using InfiniBand Verbs, eRDMA or TCP/IP sockets.

## Install

To install AIACC NCCL on the system, create a package then install it as root as follow two methods:

- method1: rpm/deb (Recommended)
```sh
# Centos:
wget http://mirrors.aliyun.com/aiacc/aiacc-nccl/aiacc_nccl-1.0.rpm
rpm -i aiacc-nccl-1.0.rpm
# Ubuntu:
wget http://mirrors.aliyun.com/aiacc/aiacc-nccl/aiacc_nccl-1.0.deb
dpkg -i aiacc-nccl-1.0.deb
```
- method2: python-offline
```sh
wget http://mirrors.aliyun.com/aiacc/aiacc-nccl/aiacc_nccl-2.0.0.tar.gz
pip install aiacc_nccl-2.0.0.tar.gz
# notes: must download and then pip install, cannot merge in oneline `pip install aiacc_xxx_url` 
# Both method1 and method2 can run concurrently.
```

- method3: python-pypi
```sh
pip install aiacc_nccl==2.0
```

## Usage

After install aiacc-nccl package, you need do nothing to change code!


## Environment

* ***AIACC_FASTTUNING***: Enable Fasttuning for LLMs, default=1 is to enable.
* ***NCCL_AIACC_ALLREDUCE_DISABLE***: Disable allreduce algo, default=0 is to enable.
* ***NCCL_AIACC_ALLGATHER_DISABLE***: Disable allgather algo, default=0 is to enable.
* ***NCCL_AIACC_REDUCE_SCATTER_DISABLE***: Disable reduce_scatter algo, default=0 is to enable.
* ***AIACC_UPDATE_ALGO_DISABLE***: Disable update aiacc nccl algo from aiacc-sql-server, default=0 is to enable.

## Performance

AIACC-NCCL can speedup the nccl performance on aliyun EGS(GPU machine), for example instance type 'ecs.ebmgn7ex.32xlarge' is A100 x 8 GPU and using network eRdma.

| GPU(EGS)    | Collective     | Nodes   | Network   | Speedup(nccl-tests) |
|-------------|----------------|---------|-----------|---------------------|
| A100 x 8    | all_gather     | 2-10    | VPC/eRdma | 30%+                |
| A100 x 8    | reduce_scatter | 2-10    | VPC/eRdma | 30%+                |
| A100 x 8    | all_reduce     | 2-10    | VPC/eRdma | 20%                 |
| V100 x 8    | all_reduce     | 2-20    | VPC       | 60%+                |
| A10  x 8    | all_reduce     | 1       | -         | 20%                 |


## Copyright

All source code and accompanying documentation is copyright (c) 2015-2020, NVIDIA CORPORATION. All rights reserved.
All modifications are copyright (c) 2020-2024, ALIYUN CORPORATION. All rights reserved.
