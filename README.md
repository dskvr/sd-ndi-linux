# StreamDiffusion NDI Real-time Video Processor

Real-time AI video transformation using StreamDiffusion and NDI (Network Device Interface) for Linux.

Bheaves the same as [stablediffusion-sdi](https://github.com/ktamas77/streamdiffusion-ndi) but with the spyware dependency (and support) removed.

## Overview

This tool captures video from an NDI source, applies real-time AI transformation using StreamDiffusion, and outputs the result as a new NDI stream.

**Pipeline:**
```
NDI Input → StreamDiffusion (img2img) → NDI Output
```

## Features

- List and select from available NDI sources
- Auto-select NDI sources by name (text search)
- Real-time AI-powered video transformation with SD-Turbo
- GPU-accelerated processing with xformers or TensorRT
- Output as NDI stream for integration with OBS, vMix, Wirecast, etc.
- Easy bash script launcher

## System Requirements

- **OS**: Linux (tested on Ubuntu 22.04+, Arch Linux)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (RTX 2060 or better recommended)
- **CUDA**: CUDA 12.1+
- **Python**: 3.10
- **Disk Space**: ~10GB for models and dependencies

## Prerequisites Installation

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

Add CUDA to your PATH in `~/.bashrc`:
```bash
export PATH=/usr/local/cuda-12.1/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.1/lib64:$LD_LIBRARY_PATH
```

Verify installation:
```bash
nvcc --version
```

### 2. Install Miniconda

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

Add NDI library to your system path in `~/.bashrc`:
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
```

## StreamDiffusion Installation

### Step 1: Create Conda Environment

```bash
conda create -n streamdiffusion python=3.10 -y
conda activate streamdiffusion
```

### Step 2: Install PyTorch with CUDA 12.1

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

Verify CUDA is available:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Should print: `True`

### Step 3: Install xformers

```bash
pip install xformers==0.0.22.post7
```

### Step 4: Clone StreamDiffusion v1

```bash
cd ~/Projects
git clone https://github.com/cumulo-autumn/StreamDiffusion.git
cd StreamDiffusion
```

### Step 5: Install StreamDiffusion

```bash
python -m pip install -e .
```

Install TinyVAE (required):
```bash
python -m streamdiffusion.tools.install-tensorrt
```

### Step 6: (Optional) Install TensorRT for Maximum Performance

Install TensorRT for 2-3x faster inference:

```bash
pip install tensorrt==8.6.1 --extra-index-url https://pypi.nvidia.com
pip install polygraphy onnx-graphsurgeon --extra-index-url https://pypi.nvidia.com
```

**Note**: TensorRT compilation takes 5-10 minutes on first run but is cached for subsequent runs.

## This Repository Setup

### Step 1: Clone This Repository

```bash
cd ~/Projects
git clone https://github.com/ktamas77/streamdiffusion-ndi.git
cd streamdiffusion-ndi
```

### Step 2: Install NDI Python Bindings

```bash
conda activate streamdiffusion
pip install ndi-python
```

### Step 3: Configure Paths

Edit `start.sh` and update these paths for your system:

```bash
# Set Python path - UPDATE THIS to match your conda environment location
PYTHON_BIN="$HOME/miniconda3/envs/streamdiffusion/bin/python"

# Set StreamDiffusion path - UPDATE THIS to match your StreamDiffusion installation
STREAMDIFFUSION_PATH="$HOME/Projects/StreamDiffusion/streamdiffusion_repo"
```

Make the script executable:
```bash
chmod +x start.sh
```

## Usage

### Quick Start (Linux)

**Option 1: Interactive Mode**
```bash
./start.sh
```
- Lists all available NDI sources
- Prompts you to select one
- Uses xformers acceleration (fast startup)

**Option 2: Manual Command**
```bash
python main.py --acceleration tensorrt --ndi-source "your-source-name"
```

### Command-line Options

```
--timeout <seconds>          NDI source search timeout (default: 5)
--acceleration <mode>        xformers or tensorrt (default: xformers)
--device <device>            cuda or cpu (default: cuda)
--ndi-source <name>          Auto-select NDI source by name (text search)
--streamdiffusion-path <path> Path to StreamDiffusion repository
```

### Examples

**Auto-select any source containing "obs":**
```bash
python main.py --ndi-source obs
```

**Use TensorRT for maximum performance:**
```bash
python main.py --acceleration tensorrt
```

**Longer search timeout for remote sources:**
```bash
python main.py --timeout 10
```

### Output Stream

The processed video is available as an NDI source named:
```
streamdiffusion-ndi-render
```

Add this as a source in:
- OBS Studio (NDI plugin)
- vMix
- Wirecast
- Any NDI-compatible application

### Example Output

When running, you'll see output like this:

```
Searching for NDI sources (timeout: 5s)...

Found 2 NDI source(s):
  [0] MY-PC (OBS Studio)
  [1] DESKTOP-ABC (vMix - Camera 1)

Select NDI source [0-1]: 0

Selected source: MY-PC (OBS Studio)

Creating NDI receiver...
Creating NDI sender: streamdiffusion-ndi-render

Initializing StreamDiffusion...
  Model: stabilityai/sd-turbo
  Device: cuda
  Resolution: 512x512
  Prompt: cyberpunk, neon lights, dark background, glowing, futuristic
  Acceleration: xformers
StreamDiffusion initialized successfully!

================================================================================
                            STREAMING STARTED
================================================================================
  Input Source:       MY-PC (OBS Studio)
  Input Resolution:   1920x1080
  Internal Resolution: 512x512
  Output Source:      streamdiffusion-ndi-render
  Output Resolution:  1920x1080
  Model:              stabilityai/sd-turbo
  Device:             cuda:0
  Acceleration:       xformers
  Prompt:             cyberpunk, neon lights, dark background, glowing, futuristic
  Negative Prompt:    black and white, blurry, low resolution, pixelated, pixel art, low quality, low fidelity
================================================================================

Press Ctrl+C to stop

2025-10-25 14:23:45 | FPS: 18.34 | RX: 2.45 GB (24.3 MB/s) | TX: 3.12 GB (31.4 MB/s) | Frames: 1834
```

**Stats Legend:**
- **FPS**: Average frames per second since start
- **RX**: Total data received from input source (per-second rate)
- **TX**: Total data sent to output stream (per-second rate)
- **Frames**: Total frames processed

When you press Ctrl+C:
```
Stopping...
Cleaning up...

Processed 1834 frames in 100.0s (18.34 FPS average)
Done!
```

## Acceleration Modes

### xformers (Default)
- **Startup**: Fast (30-60 seconds)
- **Performance**: Good (~15-20 FPS on RTX 3080)
- **Use case**: Quick testing, development

### TensorRT (Recommended)
- **Startup**: Slow first time (5-10 minutes compilation), then fast
- **Performance**: Excellent (~25-35 FPS on RTX 3080)
- **Use case**: Production, maximum performance
- **Note**: Engine is cached after first compilation

## Configuration

Edit `main.py` to customize:

### Prompt (Line 33)
```python
DEFAULT_PROMPT = "cyberpunk, neon lights, dark background, glowing, futuristic"
```

### Negative Prompt (Line 34)
```python
DEFAULT_NEGATIVE_PROMPT = "black and white, blurry, low resolution"
```

### Model (Line 35)
```python
MODEL_ID = "stabilityai/sd-turbo"  # or any Stable Diffusion model
```

### Resolution (Lines 39-40)
```python
WIDTH = 512   # Higher = better quality but slower
HEIGHT = 512
```

### Example Prompts

```python
# Anime style
DEFAULT_PROMPT = "anime style, detailed, vibrant colors, studio quality"

# Oil painting
DEFAULT_PROMPT = "oil painting, classical art style, detailed brushstrokes"

# Sketch
DEFAULT_PROMPT = "pencil sketch, hand-drawn, artistic, detailed lines"

# Watercolor
DEFAULT_PROMPT = "watercolor painting, soft colors, artistic, flowing"
```

## Performance Tips

1. **Use TensorRT** for best performance (2-3x faster than xformers)
2. **Close other GPU applications** (browsers, games, etc.)
3. **Lower resolution** if needed (try 256x256 for maximum speed)
4. **Reduce denoising steps** (line 43: `T_INDEX_LIST = [35, 45]`)
5. **Use SD-Turbo model** (already configured, optimized for speed)

### Expected Performance

| GPU | Resolution | xformers | TensorRT |
|-----|-----------|----------|----------|
| RTX 4090 | 512x512 | ~30 FPS | ~50+ FPS |
| RTX 3080 | 512x512 | ~15 FPS | ~30 FPS |
| RTX 2060 | 512x512 | ~8 FPS | ~15 FPS |

## Troubleshooting

### No NDI sources found
- Ensure NDI SDK is installed
- Check NDI sources are on the same network
- Increase timeout: `python main.py --timeout 10`
- Verify firewall isn't blocking NDI (port 5960)

### ModuleNotFoundError: No module named 'NDIlib'
```bash
pip install ndi-python
```

### CUDA out of memory
- Lower resolution in `main.py` (try 256x256)
- Close other GPU applications
- Reduce batch size (line 44: `FRAME_BUFFER_SIZE = 1`)

### StreamDiffusion import errors
Ensure StreamDiffusion path is correct in `start.sh`:
```bash
STREAMDIFFUSION_PATH="$HOME/Projects/StreamDiffusion/streamdiffusion_repo"
```

Or pass it directly via command line:
```bash
python main.py --streamdiffusion-path "$HOME/Projects/StreamDiffusion/streamdiffusion_repo"
```

### TensorRT compilation fails
- Ensure TensorRT is installed: `pip install tensorrt==8.6.1`
- Make sure CUDA 12.1 is installed
- Try with xformers first to verify setup

### Low FPS
1. Use TensorRT: `--acceleration tensorrt`
2. Lower resolution in `main.py`
3. Check GPU usage with `nvidia-smi`
4. Ensure no other GPU-intensive apps are running

### NDI library not found
If you get an error about NDI libraries not being found:
```bash
sudo ldconfig
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```

## Files

- `main.py` - Main NDI processor script
- `start.sh` - Quick launcher with xformers (interactive)
- `requirements.txt` - Python dependencies

## Architecture

```
main.py
├── NDI Input
│   ├── List available sources (with timeout)
│   ├── Auto-select by name or prompt user
│   ├── Connect to source
│   └── Receive UYVY/RGBA video frames
│
├── Frame Conversion
│   ├── NDI → PIL Image (RGB)
│   └── Resize to model resolution (512x512)
│
├── StreamDiffusion Pipeline
│   ├── Load SD-Turbo model
│   ├── Initialize with acceleration (xformers/TensorRT)
│   ├── Prepare prompts
│   ├── Process img2img transformation
│   └── Return PIL Image
│
├── Frame Conversion
│   ├── PIL Image → RGBA numpy array
│   └── Create NDI VideoFrameV2
│
└── NDI Output
    ├── Create NDI sender
    ├── Send processed frames
    └── Output as "streamdiffusion-ndi-render"
```

## Known Issues

- **Triton warning**: Harmless warning about missing Triton optimization (optional)
- **TensorRT TracerWarnings**: Normal during first-time compilation
- **First frame slow**: Model warmup takes a few seconds
- **FutureWarnings**: Diffusers library deprecation warnings (cosmetic)

## Development

### Environment Variables

Set HuggingFace cache location (optional):
```bash
export HF_HOME=$HOME/.cache/huggingface
```

### Debug Mode

Add verbose logging in `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

Based on StreamDiffusion (Apache 2.0)

## Credits

- [StreamDiffusion](https://github.com/cumulo-autumn/StreamDiffusion) - Real-time diffusion pipeline
- [NDI SDK](https://ndi.tv/) - Network Device Interface
- [Stability AI](https://stability.ai/) - SD-Turbo model
- [xformers](https://github.com/facebookresearch/xformers) - Memory-efficient attention
- [TensorRT](https://developer.nvidia.com/tensorrt) - High-performance inference

## Support

For issues and questions:
- StreamDiffusion: https://github.com/cumulo-autumn/StreamDiffusion/issues
- NDI: https://ndi.tv/support/
- This repo: Create an issue

---

**Tested on:**
- Ubuntu 22.04 LTS
- Arch Linux
- NVIDIA RTX 3080 (10GB VRAM)
- CUDA 12.1
- Python 3.10
- StreamDiffusion v1
