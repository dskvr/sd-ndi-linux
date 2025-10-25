# StreamDiffusion NDI Real-time Video Processor

Real-time AI video transformation using StreamDiffusion and NDI (Network Device Interface) for Windows.

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
- Easy Windows batch file launchers

## System Requirements

- **OS**: Windows 10/11
- **GPU**: NVIDIA GPU with 8GB+ VRAM (RTX 2060 or better recommended)
- **CUDA**: CUDA 12.1+
- **Python**: 3.10
- **Disk Space**: ~10GB for models and dependencies

## Prerequisites Installation

### 1. Install NVIDIA CUDA 12.1

Download and install CUDA Toolkit 12.1:
https://developer.nvidia.com/cuda-12-1-0-download-archive

Verify installation:
```cmd
nvcc --version
```

### 2. Install Miniconda

Download Miniconda for Windows:
https://docs.conda.io/en/latest/miniconda.html

Install to a location with plenty of space (e.g., `D:\miniconda3`)

### 3. Install NDI SDK

Download and install the NDI Tools:
https://ndi.tv/tools/

This includes the NDI SDK required for video streaming.

## StreamDiffusion Installation

### Step 1: Create Conda Environment

```cmd
conda create -n streamdiffusion python=3.10 -y
conda activate streamdiffusion
```

### Step 2: Install PyTorch with CUDA 12.1

```cmd
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

Verify CUDA is available:
```cmd
python -c "import torch; print(torch.cuda.is_available())"
```

Should print: `True`

### Step 3: Install xformers

```cmd
pip install xformers==0.0.22.post7
```

### Step 4: Clone StreamDiffusion v1

```cmd
cd D:\dev
git clone https://github.com/cumulo-autumn/StreamDiffusion.git
cd StreamDiffusion
```

### Step 5: Install StreamDiffusion

```cmd
python -m pip install -e .
```

Install TinyVAE (required):
```cmd
python -m streamdiffusion.tools.install-tensorrt
```

### Step 6: (Optional) Install TensorRT for Maximum Performance

Install TensorRT for 2-3x faster inference:

```cmd
pip install tensorrt==8.6.1 --extra-index-url https://pypi.nvidia.com
pip install polygraphy onnx-graphsurgeon --extra-index-url https://pypi.nvidia.com
```

**Note**: TensorRT compilation takes 5-10 minutes on first run but is cached for subsequent runs.

## This Repository Setup

### Step 1: Clone This Repository

```cmd
cd D:\dev
git clone <your-repo-url> streamdiffusion-ndi
cd streamdiffusion-ndi
```

### Step 2: Install NDI Python Bindings

```cmd
conda activate streamdiffusion
pip install ndi-python
```

### Step 3: Configure Paths

Update `main.py` line 17 if your StreamDiffusion is installed elsewhere:
```python
sys.path.append("D:/dev/StreamDiffusion/streamdiffusion_repo")
```

Update batch files (`start.bat`, `start-pcvr.bat`) with your Python path:
```batch
set PYTHON_BIN=D:\miniconda3\envs\streamdiffusion\python.exe
```

## Usage

### Quick Start (Windows)

**Option 1: Interactive Mode**
```cmd
start.bat
```
- Lists all available NDI sources
- Prompts you to select one
- Uses xformers acceleration (fast startup)

**Option 2: Auto-select PCVR Source (Recommended for VR)**
```cmd
start-pcvr.bat
```
- Automatically selects "pcvr-obs-ndi-out" source
- Uses TensorRT acceleration (maximum performance)
- Perfect for VR workflows

**Option 3: Manual Command**
```cmd
python main.py --acceleration tensorrt --ndi-source "your-source-name"
```

### Command-line Options

```
--timeout <seconds>          NDI source search timeout (default: 5)
--acceleration <mode>        xformers or tensorrt (default: xformers)
--device <device>            cuda or cpu (default: cuda)
--ndi-source <name>          Auto-select NDI source by name (text search)
```

### Examples

**Auto-select any source containing "obs":**
```cmd
python main.py --ndi-source obs
```

**Use TensorRT for maximum performance:**
```cmd
python main.py --acceleration tensorrt
```

**Longer search timeout for remote sources:**
```cmd
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

### Prompt (Line 29)
```python
DEFAULT_PROMPT = "cyberpunk, neon lights, dark background, glowing, futuristic"
```

### Negative Prompt (Line 30)
```python
DEFAULT_NEGATIVE_PROMPT = "black and white, blurry, low resolution"
```

### Model (Line 31)
```python
MODEL_ID = "stabilityai/sd-turbo"  # or any Stable Diffusion model
```

### Resolution (Lines 35-36)
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
4. **Reduce denoising steps** (line 37: `T_INDEX_LIST = [35, 45]`)
5. **Use SD-Turbo model** (already configured, optimized for speed)

### Expected Performance

| GPU | Resolution | xformers | TensorRT |
|-----|-----------|----------|----------|
| RTX 4090 | 512x512 | ~30 FPS | ~50+ FPS |
| RTX 3080 | 512x512 | ~15 FPS | ~30 FPS |
| RTX 2060 | 512x512 | ~8 FPS | ~15 FPS |

## Troubleshooting

### No NDI sources found
- Ensure NDI Tools are installed
- Check NDI sources are on the same network
- Increase timeout: `python main.py --timeout 10`
- Verify firewall isn't blocking NDI (port 5960)

### ModuleNotFoundError: No module named 'NDIlib'
```cmd
pip install ndi-python
```

### CUDA out of memory
- Lower resolution in `main.py` (try 256x256)
- Close other GPU applications
- Reduce batch size (line 38: `FRAME_BUFFER_SIZE = 1`)

### StreamDiffusion import errors
Ensure StreamDiffusion path is correct in `main.py` line 17:
```python
sys.path.append("D:/dev/StreamDiffusion/streamdiffusion_repo")
```

### TensorRT compilation fails
- Ensure TensorRT is installed: `pip install tensorrt==8.6.1`
- Make sure CUDA 12.1 is installed
- Try with xformers first to verify setup

### Low FPS
1. Use TensorRT: `--acceleration tensorrt`
2. Lower resolution in `main.py`
3. Check GPU usage with Task Manager
4. Ensure no other GPU-intensive apps are running

## Files

- `main.py` - Main NDI processor script
- `start.bat` - Quick launcher with xformers (interactive)
- `start-pcvr.bat` - Auto-select PCVR source with TensorRT
- `start.sh` - Bash script for Git Bash/WSL
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
```cmd
set HF_HOME=D:\huggingface_cache
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
- Windows 11
- NVIDIA RTX 3080 (10GB VRAM)
- CUDA 12.1
- Python 3.10
- StreamDiffusion v1
