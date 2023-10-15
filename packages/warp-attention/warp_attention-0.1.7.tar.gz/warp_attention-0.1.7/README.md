# WarpAttention: Faster Than Light Inference

**WarpAttention** is a highly efficient CUDA implementation of the scaled dot product attention from "Attention is All You Need", designed for fast inference during typical chatting scenarios, where the history (sequence length of key/value) is much longer than the length of the current input (sequence length of query). 

## Compatibility
Currently WarpAttention supports all Ampere GPUs on 64 bit windows/linux.
Recommended CUDA driver version: 531.14 or later
Recommended Pytorch version: 2.0.1+cu118 or later

## Installation
```bash
pip install warp-attention
```

## Quick Start

There are 2 different input modes:

### fixed sequence length

In this case, all sequences in batch are assumed to be equal length, and the input tensors must be 4 dimensional.

```python
from warp_attention import _warp_attention_forward

query = torch.randn(batch_size, q_max_seq_len, num_heads, head_dim, device="cuda", dtype=torch.half)
key = torch.randn(batch_size, kv_max_seq_len, num_heads, head_dim, device="cuda", dtype=torch.half)
value = torch.randn(batch_size, kv_max_seq_len, num_heads, head_dim, device="cuda", dtype=torch.half)

out = _warp_attention_forward(
  query=query,
  key=key,
  value=value,
  is_causal=False
)
```

### variable sequence length

In this case, either or both query and key&value can be variable sequence length. When an input has variable sequence length, it needs to be a 3 dimensional tensor, and the user will need to provide 2 additional tensors to specify the boundaries and lengths of the sequences within the batch. Here is an example where key&value are 3 dimensional:


```python
from warp_attention import _warp_attention_forward

kv_seq_start = torch.arange(batch_size, device="cuda", dtype=torch.long) * kv_max_seq_len
kv_seq_len = torch.randint(kv_max_seq_len, size=(batch_size,) , device="cuda", dtype=torch.long)
kv_total_seq_len = kv_max_seq_len * batch_size

# query = torch.randn(q_total_seq_len, num_heads, head_dim)
query = torch.randn(batch_size, q_max_seq_len, num_heads, head_dim, device="cuda", dtype=torch.half)

key = torch.randn(kv_total_seq_len, num_heads, head_dim, device="cuda", dtype=torch.half)
value = torch.randn(kv_total_seq_len, num_heads, head_dim, device="cuda", dtype=torch.half)

out = warp_attention_forward(
  query=query,
  key=key,
  value=value,
  is_causal=False,
  kv_seq_start=kv_seq_start,
  kv_seq_len=kv_seq_len,
  kv_max_seq_len=kv_max_seq_len,
)
```

In this example, we allocated `kv_max_seq_len` tokens worth of memory for each sequence in the batch, and assumed a random portion of it is actually being used. This means the remaining (allocated but unused) portion of key&value will be treated as paddings and ignored during attention computation. Users could also allocate different amount of memory for differet sequences in batch. Here's an example where we preallocate different amount of memory for different sequences in query, and assume there's no padding:

```python
q_seq_len = torch.randint(1, q_max_seq_len, size=(batch_size,), device="cuda", dtype=torch.long)
q_seq_start = q_seq_len.cumsum(dim=0) - q_seq_len[0]
query = torch.randn(q_seq_len.sum().item(), num_heads, head_dim, device="cuda", dtype=torch.half)

out = warp_attention_forward(
  query=query,
  key=key,
  value=value,
  is_causal=False,
  kv_seq_start=kv_seq_start,
  kv_seq_len=kv_seq_len,
  kv_max_seq_len=kv_max_seq_len,
  
  q_seq_start=q_seq_start,
  q_seq_len=q_seq_len,
  q_max_seq_len=q_max_seq_len,
)
```

### Gear
Gear is used to control the speed and precision of warp attention. There are in total 5 gear levels, with 0 being the most accurate, and 4 being the fastest. You can specify gear during each call:

```python
warp_attention_forward(
  query=query,
  key=key,
  value=value,
  gear=3
)
```

Or change the global default gear for all future calls:
```python
from warp_attention import set_default_gear
set_default_gear(3)
```

## Speed Comparison
to be continued
