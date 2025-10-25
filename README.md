# StreamDiffusion NDI Real-time Video Processor

Real-time AI video transformation using StreamDiffusion and NDI (Network Device Interface) for Linux.

Captures video from an NDI source, applies AI transformation using Stable Diffusion, and outputs the result as a new NDI stream.

Same functionality as [streamdiffision-ndi](https://github.com/ktamas77/streamdiffusion-ndi) but without the spyware dependency or support ;)

**Pipeline:** `NDI Input → StreamDiffusion (img2img) → NDI Output`

## Features

- List and auto-select NDI sources by name
- Real-time AI-powered video transformation with SD-Turbo
- GPU-accelerated processing (xformers or TensorRT)
- Output as NDI stream for OBS, vMix, Wirecast, etc.
- Easy installation and service management via Makefile

## System Requirements

- **OS**: Linux (tested on Ubuntu 22.04+, Arch Linux)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (RTX 2060+)
- **CUDA**: 12.1+
- **Python**: 3.10
- **Disk**: ~10GB for models and dependencies

## Quick Installation

### Check Compatibility

```bash
make check-compat  # Verify Linux OS and NVIDIA GPU
make check-deps    # Check for CUDA, Conda/Python, NDI SDK
```

### Install Everything

**Using Conda (recommended):**
```bash
make install
```

**Using Python venv:**
```bash
make install-venv
```

The Makefile will:
1. Check system compatibility
2. Guide you through prerequisite installation (CUDA, NDI SDK)
3. Create the Python environment (conda or venv)
4. Install all dependencies and StreamDiffusion

**Note**: Some prerequisites (CUDA, NDI SDK) require manual download/installation. The Makefile will pause with instructions when needed.

## Usage

### Start Processing

**Conda:**
```bash
make start
```

**Venv:**
```bash
make start ENV_TYPE=venv
```

This will:
- List available NDI sources
- Let you select one
- Start processing and output to NDI stream named `streamdiffusion-ndi-render`

### Other Commands

```bash
make stop           # Stop the processor
make restart        # Restart the processor
make status         # Check if running
make test           # Quick test run (3 second timeout)
make clean          # Remove cached models and temp files
make help           # Show all commands
```

### Command-line Options

Run manually with options:
```bash
python main.py --ndi-source "obs" --acceleration tensorrt
```

Options:
- `--timeout <seconds>` - NDI source search timeout (default: 5)
- `--acceleration <mode>` - xformers or tensorrt (default: xformers)
- `--device <device>` - cuda or cpu (default: cuda)
- `--ndi-source <name>` - Auto-select NDI source by name
- `--streamdiffusion-path <path>` - Path to StreamDiffusion repo

## Output

The processed video stream is available as:
```
streamdiffusion-ndi-render
```

Add this NDI source in OBS Studio, vMix, Wirecast, or any NDI-compatible application.

## Documentation

- **[Installation Guide](docs/installation.md)** - Detailed prerequisite installation and manual setup
- **[Configuration Guide](docs/configuration.md)** - Prompts, models, resolution, performance tuning
- **[Troubleshooting Guide](docs/troubleshooting.md)** - Common issues and solutions

## Performance

**xformers (default):**
- Fast startup (30-60s)
- Good performance (~15-20 FPS on RTX 3080)

**TensorRT (recommended for production):**
- Slow first run (5-10min compilation, then cached)
- Excellent performance (~25-35 FPS on RTX 3080)
- Use with: `make start ACCELERATION=tensorrt`

## Configuration

Edit `main.py` to customize:
- **Line 33**: Prompt (cyberpunk, anime, oil painting, etc.)
- **Line 34**: Negative prompt
- **Line 35**: Model (default: stabilityai/sd-turbo)
- **Lines 39-40**: Processing resolution (512x512)
- **Lines 41-42**: Output resolution (1920x1080)

See [Configuration Guide](docs/configuration.md) for examples and performance tips.

## Troubleshooting

**Dependency conflicts during installation?**
- Expected! The Makefile uses `--no-deps` to install known working versions
- See [Troubleshooting Guide](docs/troubleshooting.md)

**No NDI sources found?**
- Install NDI SDK
- Check sources are on same network
- Increase timeout: `python main.py --timeout 10`

**CUDA out of memory?**
- Lower resolution in `main.py` (try 256x256)
- Close other GPU applications

**More issues?** See [Troubleshooting Guide](docs/troubleshooting.md)

## Files

- `main.py` - Main NDI processor
- `start.sh` - Quick launcher script
- `Makefile` - Installation and service management
- `docs/` - Detailed documentation

## Credits

- [StreamDiffusion](https://github.com/cumulo-autumn/StreamDiffusion) - Real-time diffusion pipeline
- [NDI SDK](https://ndi.tv/) - Network Device Interface
- [Stability AI](https://stability.ai/) - SD-Turbo model

Based on [streamdiffusion-ndi](https://github.com/ktamas77/streamdiffusion-ndi) with Windows support removed.

## License

Apache 2.0 (based on StreamDiffusion)

---

**Tested on:** Ubuntu 22.04 LTS, Arch Linux (Wayland) | NVIDIA RTX 3080 | CUDA 12.1 | Python 3.10
