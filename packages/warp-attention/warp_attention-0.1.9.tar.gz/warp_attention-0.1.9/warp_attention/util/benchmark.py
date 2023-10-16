import torch
from warp_attention.util.baseline_tester import test_torch_naive, test_torch_sdpa, test_flash_attn
from warp_attention.util.warpat_tester import test_warpat
from warp_attention.util.util import mae
from warp_attention import num_kernel_versions
import numpy as np

device = "cuda:0"
# problem_size = (8, 16, 16384*4, 64, 64)
# problem_size = (16, 16, 16384, 64, 64)
problem_size = (1, 4096, 4096, 64, 64)
# problem_size = (1, 4096, 4096, 64, 64)
# problem_size = (1, 1024, 16384, 64, 64)
is_causal = False
b, m, n, k, h = problem_size
query = torch.randn(b, m, h, k, device=device, dtype=torch.half) #* 0.1
key = torch.randn(b, n, h, k, device=device, dtype=torch.half)  #* 0.1
value = torch.randn(b, n, h, k, device=device, dtype=torch.half)  #* 0.1
out = torch.zeros(b, m, h, k, device=device, dtype=torch.half) #* 0.1

warmup_loops = 20
loops = 100

runtime_flash, output_flash = test_flash_attn(query, key, value, loops=loops, warmup_loops=warmup_loops, return_output=True, is_causal=is_causal)
# runtime_naive, output_naive = test_torch_naive(query, key, value, loops=loops, warmup_loops=warmup_loops, return_output=True)
# runtime_sdpa, output_sdpa = test_torch_sdpa(query, key, value, loops=loops, warmup_loops=warmup_loops, return_output=True)

gear = 4
all_runtimes = []
for v in range(num_kernel_versions):
  torch.cuda.synchronize()
  runtime = test_warpat(
    query, key, value, gear=gear, version=v, loops=loops, is_causal=is_causal,
    warmup_loops=warmup_loops, runtime_baseline=runtime_flash, output_baseline=output_flash)
  all_runtimes.append(runtime)

best_runtime = np.min(all_runtimes)
best_version = np.argmin(all_runtimes)

test_warpat(
  query, key, value, gear=gear, version=best_version, loops=loops, is_causal=is_causal,
  warmup_loops=warmup_loops, runtime_baseline=runtime_flash, output_baseline=output_flash)
