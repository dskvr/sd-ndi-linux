# Configuration Guide

## Command-line Options

```
--timeout <seconds>          NDI source search timeout (default: 5)
--acceleration <mode>        xformers or tensorrt (default: xformers)
--device <device>            cuda or cpu (default: cuda)
--ndi-source <name>          Auto-select NDI source by name (text search)
--streamdiffusion-path <path> Path to StreamDiffusion repository
```

## Usage Examples

### Auto-select NDI source

Auto-select any source containing "obs":
```bash
python main.py --ndi-source obs
```

### Use TensorRT acceleration

For maximum performance (2-3x faster than xformers):
```bash
python main.py --acceleration tensorrt
```

**Note**: First run takes 5-10 minutes to compile TensorRT engine, but it's cached for subsequent runs.

### Longer search timeout

For remote NDI sources:
```bash
python main.py --timeout 10
```

### Custom StreamDiffusion path

```bash
python main.py --streamdiffusion-path "$HOME/custom/path/StreamDiffusion"
```

## Model Configuration

Edit `main.py` to customize the AI model behavior:

### Prompt (Line 33)

The prompt controls the style of the output:

```python
DEFAULT_PROMPT = "cyberpunk, neon lights, dark background, glowing, futuristic"
```

### Negative Prompt (Line 34)

What to avoid in the output:

```python
DEFAULT_NEGATIVE_PROMPT = "black and white, blurry, low resolution, pixelated, pixel art, low quality, low fidelity"
```

### Model (Line 35)

Which Stable Diffusion model to use:

```python
MODEL_ID = "stabilityai/sd-turbo"  # or any Stable Diffusion model
```

### Resolution (Lines 39-40)

Internal processing resolution (higher = better quality but slower):

```python
WIDTH = 512   # Higher = better quality but slower
HEIGHT = 512
```

### Output Resolution (Lines 41-42)

Final output resolution:

```python
OUTPUT_WIDTH = 1920
OUTPUT_HEIGHT = 1080
```

### Denoising Steps (Line 43)

```python
T_INDEX_LIST = [35, 45]  # Lower values = faster but lower quality
```

## Example Prompts

### Anime Style
```python
DEFAULT_PROMPT = "anime style, detailed, vibrant colors, studio quality"
```

### Oil Painting
```python
DEFAULT_PROMPT = "oil painting, classical art style, detailed brushstrokes"
```

### Pencil Sketch
```python
DEFAULT_PROMPT = "pencil sketch, hand-drawn, artistic, detailed lines"
```

### Watercolor
```python
DEFAULT_PROMPT = "watercolor painting, soft colors, artistic, flowing"
```

### Retro Gaming
```python
DEFAULT_PROMPT = "retro gaming, pixel art, 8-bit, vibrant colors"
```

## Performance Tuning

### Acceleration Modes

#### xformers (Default)
- **Startup**: Fast (30-60 seconds)
- **Performance**: Good (~15-20 FPS on RTX 3080)
- **Use case**: Quick testing, development

#### TensorRT (Recommended for Production)
- **Startup**: Slow first time (5-10 minutes compilation), then fast
- **Performance**: Excellent (~25-35 FPS on RTX 3080)
- **Use case**: Production, maximum performance
- **Note**: Engine is cached after first compilation

### Performance Tips

1. **Use TensorRT** for best performance (2-3x faster than xformers)
2. **Close other GPU applications** (browsers, games, etc.)
3. **Lower resolution** if needed (try 256x256 for maximum speed)
4. **Reduce denoising steps** (e.g., `T_INDEX_LIST = [30, 40]`)
5. **Use SD-Turbo model** (already configured, optimized for speed)

### Expected Performance

| GPU | Resolution | xformers | TensorRT |
|-----|-----------|----------|----------|
| RTX 4090 | 512x512 | ~30 FPS | ~50+ FPS |
| RTX 3080 | 512x512 | ~15 FPS | ~30 FPS |
| RTX 2060 | 512x512 | ~8 FPS | ~15 FPS |

## NDI Output Configuration

### Output Stream Name

The processed video is available as an NDI source named:
```
streamdiffusion-ndi-render
```

This name is defined in `main.py` (line 36):
```python
OUTPUT_NDI_NAME = "streamdiffusion-ndi-render"
```

### Receiving the Output

Add the NDI output as a source in:
- **OBS Studio** (requires NDI plugin)
- **vMix**
- **Wirecast**
- Any NDI-compatible application

## Environment Variables

### HuggingFace Cache Location

Set custom cache directory for downloaded models (optional):
```bash
export HF_HOME=$HOME/.cache/huggingface
```

Add to `~/.bashrc` or `~/.zshrc` to make permanent.

### Debug Mode

Add verbose logging in `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
