import torch
import numpy as np
import matplotlib
from warp_attention import num_gears

from warp_attention.util.baseline_tester import test_torch_naive, test_torch_sdpa, test_flash_attn
from warp_attention.util.warpat_tester import test_warpat
from warp_attention.util.util import mae, attn_flop

matplotlib.use('agg')
from matplotlib import pyplot as plt
from pathlib import Path


# root_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
# root_dir = Path(__file__).resolve().parent.parent


def do(b, m, k, h, ns, is_causal, device, test_function, **func_kwargs):
  all_tflops = []
  for n in ns:
    query = torch.randn(b, m, h, k, device=device, dtype=torch.half) #* 0.1
    key = torch.randn(b, n, h, k, device=device, dtype=torch.half)  #* 0.1
    value = torch.randn(b, n, h, k, device=device, dtype=torch.half)  #* 0.1
    runtime = test_function(
      query, key, value, is_causal=is_causal, loops=100, warmup_loops=10, verbose=0, **func_kwargs)
    
    tflops = attn_flop(b=b, m=m, n=n, k=k, h=h, fma=False, is_causal=is_causal) / runtime
    all_tflops.append(tflops / 1000 ** 4)
  return all_tflops

def compare(save_path, b, m, k, h, is_causal, ns=None, gears=None, device=None):
  if device is None:
    device = "cuda:0"
  device = torch.device(device)
  device_name = torch.cuda.get_device_name(device)
  if ns is None:
    ns = [2 ** i for i in range(7, 15)]
  ns = [n for n in ns if n >= m]

  if gears is None:
    gears = [i for i in range(num_gears)]

  results = {}

  results["flash attention 2"] = do(b, m, k, h, ns, is_causal, device, test_flash_attn)
  if not is_causal:
    results["torch sdpa"] = do(b, m, k, h, ns, is_causal, device, test_torch_sdpa)

  for gear in gears:
    results[f"warp attention gear{gear}"] = do(b, m, k, h, ns, is_causal, device, test_warpat, gear=gear, version=-1)

  for key, value in results.items():
    print(value)
    plt.plot(ns, value, label=key)


  plt.legend()
  plt.title(f"{device_name}\n batch_size={b} head_dim={k} query_seq_len={m} {'causal' if is_causal else ''}")
  plt.xlabel("kv_seq_len")
  plt.ylabel("TFLOPS")
  # device_name = device_name.replace(" ", "_")
  plt.savefig(save_path)
