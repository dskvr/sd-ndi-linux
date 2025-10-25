# Installation Guide

## Prerequisites

### System Requirements

- **OS**: Linux (tested on Ubuntu 22.04+, Arch Linux)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (RTX 2060 or better recommended)
- **CUDA**: CUDA 12.1+
- **Python**: 3.10
- **Disk Space**: ~10GB for models and dependencies

### 1. Install NVIDIA CUDA 12.1

**Ubuntu/Debian:**
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install cuda-toolkit-12-1
```

**Arch Linux:**
```bash
sudo pacman -S cuda cuda-tools
```

Add CUDA to your PATH in `~/.bashrc` or `~/.zshrc`:
```bash
export PATH=/opt/cuda/bin:$PATH
export LD_LIBRARY_PATH=/opt/cuda/lib64:$LD_LIBRARY_PATH
```

Verify installation:
```bash
nvcc --version
```

### 2. Install Miniconda (Optional - for conda environments)

Download and install Miniconda for Linux:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Follow the installation prompts and restart your terminal.

### 3. Install NDI SDK

Download the NDI SDK for Linux:
https://ndi.tv/sdk/

Extract and install:
```bash
tar -xvf Install_NDI_SDK_Linux_v*.tar.gz
./Install_NDI_SDK_v*.sh
```

Add NDI library to your system path in `~/.bashrc` or `~/.zshrc`:
```bash
export LD_LIBRARY_PATH="$HOME/Downloads/NDI SDK for Linux/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
```

## StreamDiffusion Installation

### Option 1: Using Conda

#### Step 1: Create Conda Environment

```bash
conda create -n streamdiffusion python=3.10 -y
conda activate streamdiffusion
```

#### Step 2: Install PyTorch with CUDA 12.1

```bash
pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu121
```

Verify CUDA is available:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Should print: `True`

#### Step 3: Install xformers

```bash
pip install xformers==0.0.22.post7
```

#### Step 4: Install Core Dependencies (with --no-deps)

Due to dependency conflicts, install these packages without dependency resolution:

```bash
pip install "numpy<2"
pip install --no-deps "huggingface_hub==0.19.4"
pip install --no-deps "tokenizers==0.14.1"
pip install --no-deps "transformers==4.35.0"
pip install --no-deps "diffusers==0.24.0"
pip install --no-deps "accelerate==0.24.0"
```

Then install supporting dependencies:
```bash
pip install filelock "fsspec>=2023.5.0" "packaging>=20.0" "pyyaml>=5.1"
pip install "regex!=2019.12.17" requests "safetensors>=0.3.1" "tqdm>=4.27"
pip install psutil "typing-extensions>=3.7.4.3"
```

#### Step 5: Install OpenCV and NDI

```bash
pip install ndi-python
pip install "opencv-python<4.8"
pip install "numpy<2"
```

#### Step 6: Clone StreamDiffusion

```bash
cd ~/Projects
git clone https://github.com/cumulo-autumn/StreamDiffusion.git
cd StreamDiffusion
```

#### Step 7: Install StreamDiffusion

```bash
pip install --no-deps -e .
```

#### Step 8: Install TinyVAE

```bash
python -m streamdiffusion.tools.install-tensorrt
```

**Note**: TensorRT compilation takes 5-10 minutes on first run but is cached for subsequent runs.

### Option 2: Using Python venv

#### Step 1: Create venv Environment

```bash
python3.10 -m venv ~/.virtualenvs/streamdiffusion
source ~/.virtualenvs/streamdiffusion/bin/activate
```

#### Step 2-8: Same as conda steps above

Follow steps 2-8 from the conda installation, but use the venv activation command instead of conda activate.

## This Repository Setup

### Clone This Repository

```bash
cd ~/Projects
git clone https://github.com/ktamas77/streamdiffusion-ndi.git
cd streamdiffusion-ndi
```

### Configure Paths

Edit `start.sh` and update these paths for your system:

```bash
# Set Python path - UPDATE THIS to match your environment location
PYTHON_BIN="$HOME/Downloads/.miniconda3/envs/streamdiffusion/bin/python"
# or for venv:
# PYTHON_BIN="$HOME/.virtualenvs/streamdiffusion/bin/python"

# Set StreamDiffusion path - UPDATE THIS to match your StreamDiffusion installation
STREAMDIFFUSION_PATH="$HOME/Projects/StreamDiffusion"
```

Make the script executable:
```bash
chmod +x start.sh
```

## Verification

Test that everything is working:

```bash
# Using conda
conda activate streamdiffusion
python main.py --timeout 3

# Using venv
source ~/.virtualenvs/streamdiffusion/bin/activate
python main.py --timeout 3
```

You should see "Searching for NDI sources..." - if no sources are available, it will exit gracefully.
