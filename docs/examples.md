# Usage Examples

Practical examples for different use cases and scenarios with StreamDiffusion NDI.

## Basic Usage Examples

### Example 1: Quick Interactive Start

Start with auto-detection and source selection:

```bash
make start
```

This will:
1. Search for NDI sources (5 second timeout)
2. List all available sources
3. Prompt you to select one
4. Start processing with xformers acceleration

**Expected output:**
```
Searching for NDI sources (timeout: 5s)...

Found 2 NDI source(s):
  [0] MY-PC (OBS Studio)
  [1] DESKTOP-ABC (vMix - Camera 1)

Select NDI source [0-1]: 0
```

### Example 2: Auto-Select Source by Name

Automatically select a source containing "obs":

```bash
python main.py --ndi-source obs
```

Or via Makefile:
```bash
make start NDI_SOURCE=obs
```

This will automatically connect to the first NDI source with "obs" in its name.

### Example 3: Maximum Performance (TensorRT)

Use TensorRT for 2-3x better performance:

```bash
python main.py --acceleration tensorrt --ndi-source obs
```

**Note**: First run takes 5-10 minutes to compile the TensorRT engine, but subsequent runs are instant.

### Example 4: Remote NDI Sources

Increase search timeout for remote sources:

```bash
python main.py --timeout 10 --ndi-source "remote-camera"
```

### Example 5: Custom StreamDiffusion Path

If StreamDiffusion is installed in a non-standard location:

```bash
python main.py --streamdiffusion-path "$HOME/custom/path/StreamDiffusion"
```

## Prompt Examples

Edit `main.py` line 33 to change the transformation style.

### Cyberpunk Style (Default)

```python
DEFAULT_PROMPT = "cyberpunk, neon lights, dark background, glowing, futuristic"
DEFAULT_NEGATIVE_PROMPT = "black and white, blurry, low resolution, pixelated, pixel art, low quality, low fidelity"
```

**Use case**: Futuristic streaming overlay, gaming content, tech presentations

### Anime Style

```python
DEFAULT_PROMPT = "anime style, detailed, vibrant colors, studio quality, cel shading"
DEFAULT_NEGATIVE_PROMPT = "realistic, photo, 3d render, blurry, low quality"
```

**Use case**: VTuber streams, anime-themed content, art streams

### Oil Painting

```python
DEFAULT_PROMPT = "oil painting, classical art style, detailed brushstrokes, renaissance, masterpiece"
DEFAULT_NEGATIVE_PROMPT = "digital, modern, photo, cartoon, low quality"
```

**Use case**: Art exhibitions, classical music streams, educational content

### Pencil Sketch

```python
DEFAULT_PROMPT = "pencil sketch, hand-drawn, artistic, detailed lines, monochrome drawing"
DEFAULT_NEGATIVE_PROMPT = "color, photo, digital, blurry"
```

**Use case**: Art tutorials, minimalist aesthetic, drawing streams

### Watercolor

```python
DEFAULT_PROMPT = "watercolor painting, soft colors, artistic, flowing, delicate, pastel"
DEFAULT_NEGATIVE_PROMPT = "harsh lines, digital, photo, dark"
```

**Use case**: Relaxing content, meditation streams, art therapy

### Comic Book Style

```python
DEFAULT_PROMPT = "comic book style, bold lines, halftone dots, pop art, dynamic"
DEFAULT_NEGATIVE_PROMPT = "realistic, photo, blurry, low contrast"
```

**Use case**: Gaming streams, superhero content, action content

### Retro 80s Aesthetic

```python
DEFAULT_PROMPT = "1980s aesthetic, retro, vaporwave, neon pink and blue, synthwave"
DEFAULT_NEGATIVE_PROMPT = "modern, realistic, dull colors"
```

**Use case**: Synthwave music, retro gaming, 80s themed content

### Film Noir

```python
DEFAULT_PROMPT = "film noir, black and white, high contrast, dramatic lighting, 1940s"
DEFAULT_NEGATIVE_PROMPT = "color, bright, cheerful, modern"
```

**Use case**: Mystery content, detective streams, dramatic presentations

### Fantasy Art

```python
DEFAULT_PROMPT = "fantasy art, magical, ethereal, detailed, epic, concept art, mystical"
DEFAULT_NEGATIVE_PROMPT = "realistic, modern, mundane, low quality"
```

**Use case**: RPG streams, fantasy gaming, storytelling

### Low Poly 3D

```python
DEFAULT_PROMPT = "low poly 3d, geometric, simple shapes, clean, stylized"
DEFAULT_NEGATIVE_PROMPT = "realistic, detailed, photo, high poly"
```

**Use case**: Indie game development, minimalist content, tech demos

## Resolution Examples

### Maximum Quality (Slow)

Edit `main.py` lines 39-42:

```python
WIDTH = 512
HEIGHT = 512
OUTPUT_WIDTH = 1920
OUTPUT_HEIGHT = 1080
```

**Performance**: ~15-20 FPS on RTX 3080 (xformers)
**Use case**: High-quality streams, demonstrations, recordings

### Balanced (Default)

```python
WIDTH = 512
HEIGHT = 512
OUTPUT_WIDTH = 1920
OUTPUT_HEIGHT = 1080
```

**Performance**: ~15-20 FPS on RTX 3080 (xformers)
**Use case**: General streaming, most use cases

### Maximum Speed

```python
WIDTH = 256
HEIGHT = 256
OUTPUT_WIDTH = 1920
OUTPUT_HEIGHT = 1080
```

**Performance**: ~30-40 FPS on RTX 3080 (xformers)
**Use case**: Live events, fast-paced content, lower-end GPUs

### Portrait Mode (9:16)

```python
WIDTH = 288
HEIGHT = 512
OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
```

**Use case**: Vertical video, TikTok, Instagram Reels, YouTube Shorts

### Square Output (1:1)

```python
WIDTH = 512
HEIGHT = 512
OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1080
```

**Use case**: Instagram posts, social media, square displays

## Integration Examples

### OBS Studio Integration

1. **Start StreamDiffusion NDI processor:**
   ```bash
   make start
   ```

2. **In OBS Studio:**
   - Add Source → NDI Source
   - Select "streamdiffusion-ndi-render"
   - Adjust size and position as needed

3. **Recommended OBS settings:**
   - Canvas Resolution: 1920x1080
   - Output Resolution: 1920x1080
   - FPS: 30

### vMix Integration

1. **Start processor with vMix source:**
   ```bash
   python main.py --ndi-source "vmix"
   ```

2. **In vMix:**
   - Add Input → NDI
   - Select "streamdiffusion-ndi-render"
   - Use as overlay or main source

### Wirecast Integration

1. **Start processor:**
   ```bash
   make start
   ```

2. **In Wirecast:**
   - Add Source → NDI
   - Choose "streamdiffusion-ndi-render"
   - Apply to desired layer

### Dual PC Streaming Setup

**PC 1 (Gaming/Content):**
- Running OBS or game capture
- Broadcasting NDI source to network

**PC 2 (Streaming PC):**
```bash
# Increase timeout for network sources
python main.py --timeout 10 --ndi-source "gaming-pc"
```

Add the processed NDI output to your streaming software.

## Real-World Use Cases

### Use Case 1: Live Concert Visualization

**Setup:**
- Input: Camera feed of musicians
- Style: Watercolor or oil painting
- Resolution: 1920x1080 @ 30 FPS

**Configuration:**
```python
DEFAULT_PROMPT = "watercolor painting, soft colors, artistic, flowing, concert lighting"
WIDTH = 512
HEIGHT = 512
```

**Command:**
```bash
python main.py --acceleration tensorrt --ndi-source "concert-camera"
```

### Use Case 2: Gaming Stream Overlay

**Setup:**
- Input: Webcam feed
- Style: Cyberpunk or anime
- Resolution: 512x512 internal, 1920x1080 output

**Configuration:**
```python
DEFAULT_PROMPT = "anime style, detailed, vibrant colors, gaming streamer"
WIDTH = 512
HEIGHT = 512
```

**Command:**
```bash
python main.py --acceleration xformers --ndi-source "webcam"
```

### Use Case 3: Art Museum Virtual Tour

**Setup:**
- Input: Museum camera feed
- Style: Oil painting or classical art
- Resolution: High quality

**Configuration:**
```python
DEFAULT_PROMPT = "oil painting, museum, classical art, detailed, masterpiece"
WIDTH = 512
HEIGHT = 512
```

**Command:**
```bash
python main.py --acceleration tensorrt --timeout 10
```

### Use Case 4: Podcast Video Enhancement

**Setup:**
- Input: Static podcast camera
- Style: Film noir or pencil sketch
- Resolution: 1920x1080

**Configuration:**
```python
DEFAULT_PROMPT = "pencil sketch, portrait, artistic, professional"
WIDTH = 512
HEIGHT = 512
```

### Use Case 5: Educational Content

**Setup:**
- Input: Presentation camera
- Style: Clean, minimalist
- Resolution: 1920x1080

**Configuration:**
```python
DEFAULT_PROMPT = "clean illustration, educational, clear, professional"
WIDTH = 512
HEIGHT = 512
```

## Performance Optimization Examples

### Example 1: Low-End GPU (RTX 2060 6GB)

```python
# main.py configuration
WIDTH = 256
HEIGHT = 256
OUTPUT_WIDTH = 1280
OUTPUT_HEIGHT = 720
T_INDEX_LIST = [30, 40]  # Lower denoising steps
FRAME_BUFFER_SIZE = 1
```

```bash
python main.py --acceleration xformers
```

**Expected**: ~10-15 FPS

### Example 2: Mid-Range GPU (RTX 3070 8GB)

```python
WIDTH = 512
HEIGHT = 512
OUTPUT_WIDTH = 1920
OUTPUT_HEIGHT = 1080
T_INDEX_LIST = [35, 45]
```

```bash
python main.py --acceleration xformers
```

**Expected**: ~15-20 FPS with xformers, ~30 FPS with TensorRT

### Example 3: High-End GPU (RTX 4090 24GB)

```python
WIDTH = 512
HEIGHT = 512
OUTPUT_WIDTH = 1920
OUTPUT_HEIGHT = 1080
T_INDEX_LIST = [35, 45]
```

```bash
python main.py --acceleration tensorrt
```

**Expected**: ~50+ FPS

## Debugging Examples

### Enable Verbose Logging

Add to the top of `main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Without NDI Sources

```bash
# Quick test (will exit if no sources)
make test
```

### Monitor GPU Usage While Running

In another terminal:

```bash
watch -n 1 nvidia-smi
```

### Check NDI Network Traffic

```bash
# Monitor network traffic on NDI port
sudo tcpdump -i any port 5960
```

## Automation Examples

### Auto-Start on Boot (systemd)

Create `/etc/systemd/system/streamdiffusion-ndi.service`:

```ini
[Unit]
Description=StreamDiffusion NDI Processor
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/Projects/sd-ndi-linux
ExecStart=/home/your-username/miniconda3/envs/streamdiffusion/bin/python main.py --ndi-source "obs" --acceleration tensorrt
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable streamdiffusion-ndi
sudo systemctl start streamdiffusion-ndi
```

### Scheduled Start/Stop (cron)

Start every day at 6 PM:
```bash
0 18 * * * cd /home/your-username/Projects/sd-ndi-linux && make start
```

Stop every day at midnight:
```bash
0 0 * * * cd /home/your-username/Projects/sd-ndi-linux && make stop
```

### Stream Quality Monitoring Script

Create `monitor.sh`:

```bash
#!/bin/bash
while true; do
    if ! make status > /dev/null 2>&1; then
        echo "$(date): StreamDiffusion NDI stopped, restarting..."
        make start
    fi
    sleep 60
done
```

## Advanced Customization

### Multiple Concurrent Streams

Run multiple instances with different prompts and outputs:

**Terminal 1 (Cyberpunk):**
```bash
# Edit main.py OUTPUT_NDI_NAME = "render-cyberpunk"
python main.py --ndi-source "camera1" --acceleration tensorrt
```

**Terminal 2 (Anime):**
```bash
# Edit main.py OUTPUT_NDI_NAME = "render-anime"
python main.py --ndi-source "camera2" --acceleration xformers
```

### Dynamic Prompt Switching

Modify `main.py` to read prompts from a file:

```python
# At the top of main.py
PROMPT_FILE = "current_prompt.txt"

# In the main loop
if os.path.exists(PROMPT_FILE):
    with open(PROMPT_FILE, 'r') as f:
        current_prompt = f.read().strip()
else:
    current_prompt = DEFAULT_PROMPT

pil_output = stream(image=pil_input, prompt=current_prompt)
```

Change style on-the-fly:
```bash
echo "anime style, vibrant" > current_prompt.txt
```

### Custom Model Loading

Use a different Stable Diffusion model:

```python
# main.py line 35
MODEL_ID = "runwayml/stable-diffusion-v1-5"
# or
MODEL_ID = "prompthero/openjourney"  # Midjourney-style model
# or
MODEL_ID = "/path/to/local/model"
```

## Troubleshooting Examples

### Example: NDI Source Not Appearing

```bash
# Increase timeout
python main.py --timeout 15

# Check firewall
sudo ufw status
sudo ufw allow 5960/tcp
sudo ufw allow 5960/udp

# Verify NDI SDK installation
ls ~/Downloads/NDI\ SDK\ for\ Linux/lib/x86_64-linux-gnu/libndi*
```

### Example: Low FPS Performance

```bash
# Check GPU usage
nvidia-smi

# Try lower resolution
# Edit main.py: WIDTH = 256, HEIGHT = 256

# Use TensorRT
python main.py --acceleration tensorrt
```

### Example: Memory Issues

```python
# Reduce buffer size in main.py
FRAME_BUFFER_SIZE = 1

# Lower resolution
WIDTH = 256
HEIGHT = 256
```

## Tips and Tricks

### Tip 1: Prompt Engineering

Combine multiple style keywords:
```python
DEFAULT_PROMPT = "anime style, cel shading, vibrant colors, studio quality, detailed, 4k"
```

### Tip 2: Negative Prompts Matter

Strong negative prompts improve quality:
```python
DEFAULT_NEGATIVE_PROMPT = "blurry, low resolution, pixelated, low quality, distorted, deformed, ugly, bad anatomy"
```

### Tip 3: Aspect Ratio Matching

Match processing aspect ratio to input for best results:
- 16:9 input → 512x288 or 512x512 processing
- 9:16 input → 288x512 processing
- 1:1 input → 512x512 processing

### Tip 4: Warmup Period

The first 10-20 frames are slower due to model warmup. Wait for stable FPS before judging performance.

### Tip 5: Network Optimization

For remote NDI sources:
- Use wired Ethernet (not WiFi)
- Ensure gigabit network switches
- Minimize network hops between source and processor
