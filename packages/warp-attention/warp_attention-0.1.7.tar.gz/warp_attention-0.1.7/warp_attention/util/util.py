import torch
import time
import numpy as np
from os import path

def cuda_synchronize(device = None, stream : torch.cuda.Stream = None):
  if stream is not None:
    stream.synchronize()
  else:
    torch.cuda.synchronize(device)

def cuda_timeit(func, args={}, loops=1, stream=None, verbose=1, warmup_loops=1, setup=None):
  assert loops >= 1
  # warmup
  if setup is not None:
    func_args = setup(args)
  else:
    func_args = args
  for _ in range(warmup_loops):
    func(**func_args)

  all_runtime = []
  cuda_synchronize(stream=stream)
  for i in range(loops):
    if setup is not None:
      func_args = setup(args)
      cuda_synchronize(stream=stream)
    else:
      func_args = args

    cuda_synchronize(stream=stream)
    start_time = time.perf_counter()
    result = func(**func_args)
    cuda_synchronize(stream=stream)
    runtime = time.perf_counter() - start_time
    all_runtime.append(runtime)

  average_runtime = sum(all_runtime) / loops
  if verbose > 0:
    print(f"{func.__qualname__}: {loops} loops, {average_runtime} sec per loop")
  return result, average_runtime

def bmm_flop(b, m, n, k, fma=True):
  return b * m * n * k * (int(not fma) + 1)

def attn_flop(b, m, n, k, h, is_causal=False, fma=True):
  return bmm_flop(b * h, m, n, k, fma=fma) * 2 - (bmm_flop(b * h, m, m, k, fma=fma) if is_causal else 0)

def mse(a, b):
  return (a - b).pow(2).mean()

def mae(a, b):
  return (a - b).abs().mean()

def get_absolute_path(*relative_path):
  relative_path = path.join(*relative_path)
  return path.join(path.dirname(__file__), relative_path)
