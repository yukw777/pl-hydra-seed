import subprocess
import re

from packaging import version

"""
Many libraries that depend on CUDA require special handling when installing
due to the limitations of Python's package management system. This script
manually installs them.
"""

PYTORCH_INSTALL_CMD_MAP = {
    "cpu": "torch==1.10.2+cpu "
    "-f https://download.pytorch.org/whl/cpu/torch_stable.html",
    "11.3": "torch==1.10.2+cu113 "
    "-f https://download.pytorch.org/whl/cu113/torch_stable.html",
    "10.2": "torch==1.10.2",
}


completed_process = subprocess.run(
    "nvcc --version", shell=True, capture_output=True, text=True
)

if completed_process.returncode != 0:
    # CUDA not installed, install CPU versions of dependencies
    cuda_version = "cpu"
else:
    m = re.search(r"release (\d+\.\d)", completed_process.stdout)
    if m is not None:
        parsed_version = version.parse(m.group(1))
        if parsed_version >= version.parse("11.3"):
            # Install dependencies for CUDA 11.3
            cuda_version = "11.3"
        elif parsed_version >= version.parse("10.2") and parsed_version < version.parse(
            "11.0"
        ):
            # Install dependencies for CUDA 10.2
            cuda_version = "10.2"
# PyTorch
subprocess.run(
    f"python -m pip install {PYTORCH_INSTALL_CMD_MAP[cuda_version]}",
    shell=True,
    check=True,
)
