try:
  import torch
except ImportError:
  print("pytorch is not installed.")
  exit()

from torch import Tensor
from typing import Optional
from pathlib import Path
from ._version import __version__
import platform
import math

def log_next_power_of_2(x):
  return 0 if x == 0 else math.ceil(math.log2(x))

try:
  from warp_attention.warp_attention_torch_cpp import create_module, set_log_level, get_log_level

  _proj_dir = Path(__file__).resolve().parent
  _assets_dir = _proj_dir / "assets"
  _default_gear = 4


  if platform.system() == "Linux":
    _kernel_map = {
      "8.0": f"{_assets_dir}/warp_attn_forward_sm80.cubin",
      "8.6": f"{_assets_dir}/warp_attn_forward_sm86.cubin",
    }

  elif platform.system() == "Windows":
    _kernel_map = {
      "8.0": f"{_assets_dir}/warp_attn_forward_sm80_win.cubin",
      "8.6": f"{_assets_dir}/warp_attn_forward_sm86_win.cubin",
    }

  _kernel_config = None
  _kernel_module = None
  _map_to_best_version = None
  num_kernel_versions = None
  num_gears = None
  
  def _load_assets():
    global _kernel_config
    global _kernel_module
    global _map_to_best_version
    global num_kernel_versions
    global num_gears

    _kernel_config = torch.load(_assets_dir / "kernel_config.pt")
    _kernel_module = create_module(_kernel_config, _kernel_map)
    if Path(_assets_dir / "map_to_best_version.pt").exists():
      _map_to_best_version = torch.load(_assets_dir / "map_to_best_version.pt")
    else:
      _map_to_best_version = None
    num_kernel_versions = _kernel_config.shape[3]
    # max_gear = _kernel_config.shape[2] - 1
    num_gears = _kernel_config.shape[2]

  def set_default_gear(new_gear):
    global _default_gear
    _default_gear = new_gear
  
  def get_default_gear():
    return _default_gear

  def _pick_best_version(
      b: int,
      m: int,
      head_dim: int,
      gear: int,
      is_causal: bool
    ):

    def get_log_index(val, log_start, log_stop):
      log_val = log_next_power_of_2(val)
      log_val = max(log_val, log_start )
      log_val = min(log_val, log_stop-1 )
      log_idx = log_val - log_start
      return log_idx

    if _map_to_best_version is not None:
      # log_m = log_next_power_of_2(m)
      # log_m = max(log_m, _map_to_best_version["log_m_start"] )
      # log_m = min(log_m, _map_to_best_version["log_m_stop"]-1 )
      log_m_idx = get_log_index(m, _map_to_best_version["log_m_start"], _map_to_best_version["log_m_stop"])
      log_b_idx = get_log_index(b, _map_to_best_version["log_b_start"], _map_to_best_version["log_b_stop"])
      head_dim_idx = _map_to_best_version["head_dims"].index(head_dim)

      version = _map_to_best_version["map_to_best_version"][gear, head_dim_idx, int(is_causal), log_b_idx, log_m_idx]

      return version
    else:
      return 0


  def warp_attention_forward(
      query: Tensor,
      key: Tensor,
      value: Tensor,
      scale: Optional[float] = None,
      out: Optional[Tensor] = None,
      gear: Optional[int] = None,
      version: int = -1,
      is_causal: bool = False,
      q_seq_start: Optional[Tensor] = None,
      q_seq_len: Optional[Tensor] = None,
      kv_seq_start: Optional[Tensor] = None,
      kv_seq_len: Optional[Tensor] = None,
      q_max_seq_len: int = -1,
      kv_max_seq_len: int = -1,
    ):
    if out is None:
      out = torch.zeros_like(query)
    if scale is None:
      scale = query.shape[-1] ** (-0.5)
  
    if query.ndim == 4:
      m = query.shape[1]
      b = query.shape[0]
    elif q_max_seq_len != -1:
      m = q_max_seq_len
      b = q_seq_start.shape[0]
    else:
      m = q_seq_len.max().item()
      b = q_seq_start.shape[0]
    head_dim = query.shape[-1]
    
    if version == -1:
      version = _pick_best_version(b, m, head_dim, gear, is_causal)
    
    if gear == -1 or gear is None:
      gear = _default_gear

    assert 0 <= version <= num_kernel_versions, f"version should be between 0 and {num_kernel_versions}"
    assert 0 <= gear < num_gears, f"gear should be between 0 and {num_gears}"

    has_q_start = False
    if query.ndim == 3:
      assert isinstance(q_seq_start, Tensor) and isinstance(q_seq_len, Tensor)
      has_q_start = True
      
    has_kv_start = False
    if key.ndim == 3:
      assert isinstance(kv_seq_start, Tensor) and isinstance(kv_seq_len, Tensor)
      assert value.ndim == 3
      has_kv_start = True

    stream = torch.cuda.current_stream()

    _kernel_module.run(
      query, key, value, out, 
      q_seq_start if has_q_start else query, 
      q_seq_len if has_q_start else query, 
      kv_seq_start if has_kv_start else key, 
      kv_seq_len if has_kv_start else key, 
      scale, gear, version, is_causal, has_q_start, has_kv_start, stream.cuda_stream,
      q_max_seq_len, kv_max_seq_len
    )
    return out

  _load_assets()

except ImportError:
  print("warp attention is installed incorrectly.")