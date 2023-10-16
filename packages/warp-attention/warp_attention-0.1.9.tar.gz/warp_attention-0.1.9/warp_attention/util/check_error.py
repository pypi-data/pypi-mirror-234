import argparse
import torch
from .baseline_tester import test_flash_attn
from .warpat_tester import test_warpat
from warp_attention import num_gears, num_kernel_versions


device = "cuda:0"

def parse_args(parser):
  parser.add_argument(
    "--q-seq-len", "-m",
    type=int,
    default=1,
  )
  parser.add_argument(
    "--kv-seq-len", "-n",
    type=int,
    default=1,
  )
  parser.add_argument(
    "--num-heads", "-h",
    type=int,
    default=1,
  )
  parser.add_argument(
    "--head-dim", "-k",
    type=int,
    default=1,
  )
  parser.add_argument(
    "--version", "-v",
    type=int,
    default=1,
  )
  parser.add_argument(
    "--gear", "-g",
    type=int,
    default=1,
  )
  parser.add_argument(
    "--is-causal", "-c",
    type=bool,
    default=False,
  )

  args = parser.parse_args()
  return args

# command = f"python {file_dir}/check_error.py -m {m} -n {n} -h {num_heads} -k {head_dim} -c {is_causal} -v {v} -g {gear}"
# if subprocess.run(command, shell=True).returncode != 0:
#   continue

if __name__ == "__main__":
  parser = argparse.ArgumentParser(add_help=False)
  args = parse_args(parser)

  query = torch.randn(1, args.q_seq_len, args.num_heads, args.head_dim, device=device, dtype=torch.half) #* 0.1
  key = torch.randn(1, args.kv_seq_len, args.num_heads, args.head_dim, device=device, dtype=torch.half)  #* 0.1
  value = torch.randn(1, args.kv_seq_len, args.num_heads, args.head_dim, device=device, dtype=torch.half)  #* 0.1
  out = torch.zeros(1, args.q_seq_len, args.num_heads, args.head_dim, device=device, dtype=torch.half) #* 0.1

  runtime = test_warpat(
    query, key, value, gear=args.gear, version=args.version, loops=1, is_causal=args.is_causal,
    warmup_loops=1, runtime_baseline=0, output_baseline=0, verbose=0)