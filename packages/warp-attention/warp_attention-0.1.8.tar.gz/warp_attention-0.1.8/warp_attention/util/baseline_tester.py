import torch
from torch.nn.functional import normalize
from torch import Tensor
from torch.nn.functional import scaled_dot_product_attention
from flash_attn import flash_attn_func

from . import util

# @torch.jit.script
# def attn(query: Tensor, key: Tensor, value: Tensor):
#   key: []
#   return query.clone()
#   head_dim = query.shape[-1]

#   query = query.transpose(1, 2) #[batch_size, n_heads, q_seqlen, head_dim]
#   key = key.transpose(1, 2).transpose(2, 3) #[batch_size, n_heads, head_dim, kv_seqlen]
#   value = value.transpose(1, 2) #[batch_size, n_heads, kv_seqlen, head_dim]
#   a = query @ key # [batch_size, n_heads, q_seqlen, kv_seqlen]
#   a = a * (head_dim ** -0.5)
#   # s = a.half()
#   # s_max = s.max(dim=-1, keepdim=True).values
#   # s = (s - s_max).exp()
#   # s = normalize(s, p=1.0, dim=-1).half()
#   s = a.softmax(dim=-1)

#   o = s @ value # [batch_size, n_heads, q_seqlen, head_dim]
#   return o.transpose(1, 2)


def attn(query: Tensor, key: Tensor, value: Tensor, is_causal: bool=False):
  # key: []
  # return query.clone()
  head_dim = query.shape[-1]
  q_seqlen = query.shape[1]
  kv_seqlen = key.shape[1]

  query = query.transpose(1, 2) #[batch_size, n_heads, q_seqlen, head_dim]
  key = key.transpose(1, 2).transpose(2, 3) #[batch_size, n_heads, head_dim, kv_seqlen]
  value = value.transpose(1, 2) #[batch_size, n_heads, kv_seqlen, head_dim]
  a = query @ key # [batch_size, n_heads, q_seqlen, kv_seqlen]
  a = a * (head_dim ** -0.5)
  # s = a.half()
  # s_max = s.max(dim=-1, keepdim=True).values
  # s = (s - s_max).exp()
  # s = normalize(s, p=1.0, dim=-1).half()
  if is_causal:
    mask = torch.zeros(1, 1, q_seqlen, kv_seqlen, device=query.device, dtype=query.dtype) + float("-inf")
    mask = mask.triu(kv_seqlen - q_seqlen + 1)
    # plt.imshow(mask.cpu()[0,0])
    # plt.show()
    a = a + mask
  s = a.softmax(dim=-1)

  o = s @ value # [batch_size, n_heads, q_seqlen, head_dim]
  return o.transpose(1, 2)

def test_torch_naive(
    query : Tensor,
    key : Tensor,
    value : Tensor,
    loops = 1,
    warmup_loops = 1,
    verbose = 1,
    is_causal=False,
    return_output = False,
    **kwargs
  ):
  batch_size, kv_seqlen, n_heads, head_dim = key.shape
  q_seqlen = query.shape[1]


  kwargs = {
    "query" : query, 
    "key" : key,
    "value" : value,
    "is_causal": is_causal,
  }
  output = attn(**kwargs)

  _, runtime = util.cuda_timeit(attn, args=kwargs, loops=loops, verbose=0, warmup_loops=warmup_loops)

  flops = util.attn_flop(b=batch_size, m=q_seqlen, n=kv_seqlen, k=head_dim, h=n_heads, fma=False, is_causal=is_causal) / runtime

  if verbose > 0:
    print()
    print(f"pytorch naive: Problem size: batch_size={batch_size}, q_seqlen={q_seqlen}, kv_seqlen={kv_seqlen}, head_dim={head_dim}, n_heads={n_heads}")
    print(f"average runtime of {loops} loops: {runtime} sec  TFLOPS: {flops / 1000**4}")

  if return_output:
    return runtime, output
  else:
    return runtime
  
def test_torch_sdpa(
    query : Tensor,
    key : Tensor,
    value : Tensor,
    loops = 1,
    warmup_loops = 1,
    verbose = 1,
    is_causal=False,
    return_output = False,
    **kwargs
  ):
  batch_size, kv_seqlen, n_heads, head_dim = key.shape
  q_seqlen = query.shape[1]
  query = query.transpose(1, 2)
  key = key.transpose(1, 2)
  value = value.transpose(1, 2)

  kwargs = {
    "query" : query, 
    "key" : key,
    "value" : value,
    "dropout_p": 0,
    "is_causal": is_causal,
  }
  output = scaled_dot_product_attention(**kwargs)
  output = output.transpose(1, 2)

  _, runtime = util.cuda_timeit(scaled_dot_product_attention, args=kwargs, loops=loops, verbose=0, warmup_loops=warmup_loops)

  flops = util.attn_flop(b=batch_size, m=q_seqlen, n=kv_seqlen, k=head_dim, h=n_heads, fma=False, is_causal=is_causal) / runtime

  if verbose > 0:
    print()
    print(f"pytorch sdpa: Problem size: batch_size={batch_size}, q_seqlen={q_seqlen}, kv_seqlen={kv_seqlen}, head_dim={head_dim}, n_heads={n_heads}")
    print(f"average runtime of {loops} loops: {runtime} sec  TFLOPS: {flops / 1000**4}")

  if return_output:
    return runtime, output
  else:
    return runtime
  
def test_flash_attn(
    query : Tensor,
    key : Tensor,
    value : Tensor,
    loops = 1,
    warmup_loops = 1,
    verbose = 1,
    is_causal=False,
    return_output = False,
    **kwargs
  ):
  batch_size, kv_seqlen, n_heads, head_dim = key.shape
  q_seqlen = query.shape[1]


  kwargs = {
    "q" : query, 
    "k" : key,
    "v" : value,
    "causal": is_causal,
  }
  output = flash_attn_func(**kwargs)

  _, runtime = util.cuda_timeit(flash_attn_func, args=kwargs, loops=loops, verbose=0, warmup_loops=warmup_loops)

  torch.cuda.synchronize()
  flops = util.attn_flop(b=batch_size, m=q_seqlen, n=kv_seqlen, k=head_dim, h=n_heads, fma=False, is_causal=is_causal) / runtime

  if verbose > 0:
    print()
    print(f"flash attention 2: Problem size: batch_size={batch_size}, q_seqlen={q_seqlen}, kv_seqlen={kv_seqlen}, head_dim={head_dim}, n_heads={n_heads}")
    print(f"average runtime of {loops} loops: {runtime} sec  TFLOPS: {flops / 1000**4}")

  if return_output:
    return runtime, output
  else:
    return runtime

