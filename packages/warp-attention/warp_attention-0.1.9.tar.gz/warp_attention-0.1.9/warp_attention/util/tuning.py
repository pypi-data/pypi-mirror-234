import torch
import numpy as np
from warp_attention.util.baseline_tester import test_flash_attn, test_torch_naive
from warp_attention.util.warpat_tester import test_warpat
from warp_attention import num_gears, num_kernel_versions, set_log_level, get_log_level
from tqdm import tqdm
import yaml
import os
import sys
import subprocess
from pathlib import Path
from traceback import print_exc
from time import sleep

warmup_loops = 10
loops = 100
n = 4096

head_dims = [32, 64, 128]
set_log_level(0)

root_dir = Path(__file__).resolve().parent.parent
# print(root_dir)
problematic_path = f"{root_dir}/util/problematic.yaml"
if not Path(problematic_path).exists():
  with open(problematic_path, "w") as f:
    f.write("[]")

def warmup():
  a = torch.randn(4096, 4096, device="cuda:0")
  for i in range(1000):
    c = a @ a


def tune(device=None, log_m_start=4, log_m_stop=11, log_b_start=0, log_b_stop=1, verbose=0):
  if device is None:
    device = "cuda:0"

  with open(problematic_path, "r") as f:
    problematic = yaml.safe_load(f)
  # print(problematic)
  map_to_best_version = torch.zeros(
    num_gears, 
    len(head_dims), 
    2, 
    log_b_stop - log_b_start, 
    log_m_stop - log_m_start, 
    dtype=torch.int
  )
  warmup()
  warmup()

  try:
    counter = 0
    for gear in range(num_gears):
      for is_causal_idx, is_causal in enumerate( (False, True) ):
        for log_m_idx, log_m in enumerate(range(log_m_start, log_m_stop)):
          for log_b_idx, log_b in enumerate(range(log_b_start, log_b_stop)):
            for head_dim_idx, head_dim in enumerate(head_dims):
              m = 2 ** log_m
              b = 2 ** log_b
              # n = 2 ** log_n
              num_heads = 64
              
              query = torch.randn(b, m, num_heads, head_dim, device=device, dtype=torch.half) #* 0.1
              key = torch.randn(b, n, num_heads, head_dim, device=device, dtype=torch.half)  #* 0.1
              value = torch.randn(b, n, num_heads, head_dim, device=device, dtype=torch.half)  #* 0.1

              runtime_flash, output_flash = test_flash_attn(query, key, value, loops=loops, warmup_loops=warmup_loops, return_output=True, is_causal=is_causal, verbose=0)
              runtime_naive, output_naive = test_torch_naive(query, key, value, loops=1, warmup_loops=1, return_output=True, is_causal=is_causal, verbose=0)

              all_runtime = []
              for v in range(num_kernel_versions):
                problem = [v, gear, head_dim, is_causal, b, m]
                if problem in problematic:
                  all_runtime.append(999999)
                  continue
                runtime, error = test_warpat(
                  query.clone(), key.clone(), value.clone(), gear=gear, version=v, loops=loops, is_causal=is_causal,
                  warmup_loops=warmup_loops, runtime_baseline=runtime_flash, output_baseline=output_naive.clone(), verbose=0, return_error=True)
                # print(error)
                if error > 1e-4:
                  all_runtime.append(999999)
                  continue
                all_runtime.append(runtime)
              # print( problem )
              best_v = np.argmin(all_runtime)
              # print(best_v)
              map_to_best_version[gear, head_dim_idx, is_causal_idx, log_b_idx, log_m_idx] = best_v
              runtime = test_warpat(
                query.clone(), key.clone(), value.clone(), gear=gear, version=best_v, loops=loops, is_causal=is_causal,
                warmup_loops=warmup_loops, runtime_baseline=runtime_flash, output_baseline=output_naive.clone(), verbose=verbose)
              # print(best_v)
              # exit()
              
              # print(counter, best_v, gear, log_m_idx, head_dim, is_causal)
              counter += 1
    if verbose > 0:
      print(map_to_best_version.unique())
      for i in range(num_gears):
        print(map_to_best_version[i].unique())


    config = dict()
    config["log_m_start"] = log_m_start
    config["log_m_stop"] = log_m_stop
    config["log_b_start"] = log_b_start
    config["log_b_stop"] = log_b_stop
    config["head_dims"] = head_dims
    config["map_to_best_version"] = map_to_best_version
    
    torch.save(config, f"{root_dir}/assets/map_to_best_version.pt")

  # except RuntimeError:
  except Exception as e:
    print_exc()
    # print(problem)
    problematic.append(problem)
    with open(problematic_path, "w") as f:
      yaml.safe_dump(problematic, f)