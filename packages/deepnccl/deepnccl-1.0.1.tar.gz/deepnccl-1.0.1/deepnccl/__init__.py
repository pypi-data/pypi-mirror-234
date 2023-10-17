# import aiacc

import os

def get_root_path():
    path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    return path

def enable():
    # set LD_LIBRARY_PATH or LD_PRELOAD to aiacc_nccl
    aiacc_nccl_path = get_root_path()
    aiacc_nccl_so_file = "/libnccl.so.2"
    os.environ["LD_LIBRARY_PATH"] = os.environ.get("LD_LIBRARY_PATH", "") + ":" + aiacc_nccl_path
    os.environ["LD_PRELOAD"] = os.environ.get("LD_PRELOAD", "") + ":" + aiacc_nccl_so_file
    print(f"To enable AIACC_NCCL, you can set env before calling nccl like: \n" +
          f"export LD_LIBRARY_PATH={aiacc_nccl_path}:$LD_LIBRARY_PATH \n" +
          f"export LD_PRELOAD={aiacc_nccl_so_file}:$LD_PRELOAD \n"
    )
    return True

def support_cuda_arch():
    return "sm70,sm80"

