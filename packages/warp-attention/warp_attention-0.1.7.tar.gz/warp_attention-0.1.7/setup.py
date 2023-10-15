import torch
from setuptools import setup, Extension, find_packages
from torch.utils.cpp_extension import BuildExtension, CppExtension
from pathlib import Path
from warp_attention._version import __version__

proj_dir = Path(__file__).resolve().parent
# src_dir = f"{proj_dir}/csrc"
src_dir = f"csrc"

setup(
  name='warp_attention',
  version=__version__,
  description="Warp attention: hardware efficient implementation of scaled dot product attention.",
  author='demoriarty', 
  packages=find_packages(),
  include_package_data=True,
  keywords = ["transformers", "attention", "scaled dot product attention", "pytorch"],
  # install_requires=[ 
  #   'torch',
  # ],
  include_dirs=[src_dir],
  ext_modules=[
    CppExtension(
      name='warp_attention.warp_attention_torch_cpp', 
      sources=[f"{src_dir}/warpat/warp_attention_api_torch.cpp"],
      libraries=["cuda"],
      library_dirs=["/usr/lib/wsl/lib"],
    )
  ],
  cmdclass={'build_ext': BuildExtension},
)


# warp_attention_cpp = load(name="warp_attention", sources=[f"{src_dir}/warp_attention_api.cpp"], verbose=True)