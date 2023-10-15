import torch
from torch.nn.functional import normalize
from torch import Tensor

from . import util
from .baseline_tester import attn
from warp_attention import warp_attention_forward

def test_warpat(
    query : Tensor,
    key : Tensor,
    value : Tensor,
    gear: int= 3,
    version: int=0,
    loops = 1,
    warmup_loops = 1,
    verbose = 1,
    is_causal=False,
    epsilon=0,
    runtime_baseline=None,
    output_baseline=None,
    return_output = False,
    return_error = False,
  ):
  batch_size, kv_seqlen, n_heads, head_dim = key.shape
  q_seqlen = query.shape[1]

  
  baseline_kwargs = {
    "query" : query, 
    "key" : key,
    "value" : value,
    "is_causal": is_causal,
  }

  if runtime_baseline is None and output_baseline is None:
    output_baseline, runtime_baseline = util.cuda_timeit(attn, args=baseline_kwargs, loops=loops, warmup_loops=warmup_loops, verbose=0)
  elif output_baseline is None:
    output_baseline = attn(**kwargs)
  elif runtime_baseline is None:
    _, runtime_baseline = util.cuda_timeit(attn, args=baseline_kwargs, loops=loops, warmup_loops=warmup_loops, verbose=0)
  

  output = torch.zeros_like(query)
  kwargs = {
    "query" : query, 
    "key" : key,
    "value" : value,
    "gear" : gear,
    "out": output,
    "version": version,
    "is_causal": is_causal,
  }
  # output = _warp_attention_forward(**kwargs)
  try:
    warp_attention_forward(**kwargs)
    error = util.mae(output, output_baseline).item()

    _, runtime = util.cuda_timeit(warp_attention_forward, args=kwargs, loops=loops, verbose=0, warmup_loops=warmup_loops)
  except RuntimeError:
    error = 0
    runtime = float("inf")

  flops = ( util.attn_flop(b=batch_size, m=q_seqlen, n=kv_seqlen, k=head_dim, h=n_heads, fma=False, is_causal=is_causal)) / runtime
  if verbose > 0:
    print()
    print(f"warp_attention gear={gear}, v={version}: Problem size: batch_size={batch_size}, q_seqlen={q_seqlen}, kv_seqlen={kv_seqlen}, head_dim={head_dim}, n_heads={n_heads}, is_causal={is_causal}")
    print(f"average runtime of {loops} loops: {runtime} sec  TFLOPS: {flops / 1000**4}")
    print(f"{runtime_baseline / runtime * 100}% the speed of baseline")
    print(f"{runtime / runtime_baseline * 100}% the runtime of baseline")


  if (error > epsilon or error != error):
    if verbose > 0:
      print(f"Mean absolute error ({error}) is greater than epsilon ({epsilon})")

  result = runtime
  if return_output and return_error:
    result = (runtime, error, output)
  elif return_output:
    result = (runtime, output)
  elif return_error:
    result = (runtime, error)

  return result