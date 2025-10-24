# StreamDiffusion NDI Real-time Video Processor

Real-time AI video transformation using StreamDiffusion and NDI (Network Device Interface).

## Overview

This tool captures video from an NDI source, applies real-time AI transformation using StreamDiffusion, and outputs the result as a new NDI stream.

**Pipeline:**
```
NDI Input → StreamDiffusion (img2img) → NDI Output
```

## Features

- List and select from available NDI sources
- Real-time AI-powered video transformation
- GPU-accelerated processing (CUDA)
- Configurable acceleration modes (xformers / TensorRT)
- Output as NDI stream for integration with other tools

## Requirements

- Windows 10/11 with NVIDIA GPU (CUDA 12.1+)
- Python 3.10+
- NDI SDK (installed separately)
- 8GB+ VRAM recommended

## Installation

### 1. Install NDI SDK

Download and install the NDI SDK from NewTek:
https://ndi.tv/sdk/

### 2. Clone and Setup

```bash
cd ~/dev
git clone <this-repo> streamdiffusion-ndi
cd streamdiffusion-ndi
```

### 3. Install Dependencies

Using the existing `streamdiffusion` conda environment:

```bash
D:/miniconda3/envs/streamdiffusion/python.exe -m pip install -r requirements.txt
```

Or install ndi-python separately:
```bash
pip install ndi-python
```

## Usage

### Basic Usage

```bash
python main.py
```

The script will:
1. Search for available NDI sources (5 second timeout)
2. Display a list of found sources
3. Prompt you to select one
4. Initialize StreamDiffusion
5. Start processing frames in real-time

### Command-line Options

```bash
python main.py --timeout 10           # Longer NDI source search
python main.py --acceleration tensorrt # Use TensorRT (faster)
python main.py --device cpu           # Use CPU (slow, not recommended)
```

### Output

The processed video is available as an NDI source named:
```
streamdiffusion-ndi-render
```

You can receive this in any NDI-compatible application (OBS Studio, vMix, Wirecast, etc.)

## Configuration

Edit `main.py` to customize:

- **Prompt** (line 23): Change the AI transformation style
- **Model** (line 22): Use a different Stable Diffusion model
- **Resolution** (lines 27-28): Adjust processing resolution
- **Denoising steps** (line 29): Trade quality for speed

### Example Prompts

```python
# Cyberpunk style (default)
DEFAULT_PROMPT = "cyberpunk, neon lights, dark background, glowing, futuristic"

# Anime style
DEFAULT_PROMPT = "anime style, detailed, vibrant colors, studio quality"

# Oil painting
DEFAULT_PROMPT = "oil painting, classical art style, detailed brushstrokes"

# Sketch style
DEFAULT_PROMPT = "pencil sketch, hand-drawn, artistic, detailed lines"
```

## Performance

Expected performance (RTX 3080+):
- **xformers**: ~15-20 FPS
- **TensorRT**: ~25-35 FPS (after first-time compilation)

## Troubleshooting

### No NDI sources found
- Ensure NDI SDK is installed
- Check that NDI sources are on the same network
- Try increasing `--timeout` value

### Low FPS
- Use TensorRT acceleration: `--acceleration tensorrt`
- Reduce resolution in `main.py`
- Close other GPU-intensive applications

### Import errors
- Ensure StreamDiffusion is installed: `pip list | grep streamdiffusion`
- Install missing dependencies from requirements.txt

## Architecture

```
main.py
├── NDI Input
│   ├── List sources
│   ├── Connect to selected source
│   └── Receive video frames
│
├── StreamDiffusion Pipeline
│   ├── Initialize model (SD-Turbo)
│   ├── Prepare with prompt
│   └── Process frames (img2img)
│
└── NDI Output
    ├── Convert processed frames
    └── Send to NDI stream
```

## License

Based on StreamDiffusion (Apache 2.0)

## Credits

- [StreamDiffusion](https://github.com/cumulo-autumn/StreamDiffusion) - Real-time diffusion
- [NDI SDK](https://ndi.tv/) - Video over IP protocol
- [Stability AI](https://stability.ai/) - SD-Turbo model
