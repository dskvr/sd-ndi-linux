# Troubleshooting Guide

## Dependency Conflicts

### Pip dependency resolution errors during installation

This is expected! The Makefile uses `--no-deps` strategically to install a known working combination of package versions:

- `huggingface_hub==0.19.4`
- `tokenizers==0.14.1`
- `transformers==4.35.0`
- `diffusers==0.24.0`
- `accelerate==0.24.0`

These versions have metadata conflicts but work perfectly together in practice. The `make install` or `make install-venv` commands handle this automatically.

**If you're installing manually**, use `--no-deps` for the core packages:
```bash
pip install --no-deps huggingface_hub==0.19.4
pip install --no-deps tokenizers==0.14.1
pip install --no-deps transformers==4.35.0
pip install --no-deps diffusers==0.24.0
pip install --no-deps accelerate==0.24.0
```

Then install their dependencies separately with normal pip install.

## NDI Issues

### No NDI sources found

**Causes:**
- NDI SDK not installed
- NDI sources not on the same network
- Firewall blocking NDI traffic
- Source not broadcasting

**Solutions:**
```bash
# Increase search timeout
python main.py --timeout 10

# Check NDI SDK is installed
ls ~/Downloads/NDI\ SDK\ for\ Linux/lib/x86_64-linux-gnu/libndi*

# Verify environment variable is set
echo $LD_LIBRARY_PATH

# Check firewall (NDI uses port 5960)
sudo ufw status
sudo ufw allow 5960/tcp
sudo ufw allow 5960/udp
```

### ModuleNotFoundError: No module named 'NDIlib'

**Solution:**
```bash
# Activate your environment first
conda activate streamdiffusion
# or
source ~/.virtualenvs/streamdiffusion/bin/activate

# Install NDI Python bindings
pip install ndi-python
```

### NDI library not found at runtime

**Solution:**
```bash
# Run ldconfig
sudo ldconfig

# Add to environment
export LD_LIBRARY_PATH="$HOME/Downloads/NDI SDK for Linux/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"

# Make permanent by adding to ~/.bashrc or ~/.zshrc
echo 'export LD_LIBRARY_PATH="$HOME/Downloads/NDI SDK for Linux/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"' >> ~/.zshrc
```

## CUDA Issues

### CUDA out of memory

**Solutions:**
1. Lower resolution in `main.py`:
   ```python
   WIDTH = 256   # Try 256x256 instead of 512x512
   HEIGHT = 256
   ```

2. Close other GPU applications:
   ```bash
   # Check GPU usage
   nvidia-smi
   ```

3. Reduce batch size in `main.py` (line 44):
   ```python
   FRAME_BUFFER_SIZE = 1
   ```

### CUDA not available

**Check CUDA installation:**
```bash
# Check nvcc
nvcc --version

# Check CUDA in PyTorch
python -c "import torch; print(torch.cuda.is_available())"
```

**If False:**
1. Ensure CUDA is in PATH:
   ```bash
   export PATH=/opt/cuda/bin:$PATH
   export LD_LIBRARY_PATH=/opt/cuda/lib64:$LD_LIBRARY_PATH
   ```

2. Reinstall PyTorch with CUDA support:
   ```bash
   pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu121
   ```

## StreamDiffusion Issues

### StreamDiffusion import errors

**Check StreamDiffusion path:**

In `start.sh`:
```bash
STREAMDIFFUSION_PATH="$HOME/Projects/StreamDiffusion"
```

Or pass via command line:
```bash
python main.py --streamdiffusion-path "$HOME/Projects/StreamDiffusion"
```

### ModuleNotFoundError: No module named 'utils'

**Cause:** Incorrect StreamDiffusion path

**Solution:**
The path should point to the root StreamDiffusion directory (not `src`):
```bash
export STREAMDIFFUSION_PATH="$HOME/Projects/StreamDiffusion"
python main.py --streamdiffusion-path "$STREAMDIFFUSION_PATH"
```

## TensorRT Issues

### TensorRT compilation fails

**Solutions:**

1. Ensure TensorRT is installed:
   ```bash
   pip install tensorrt==8.6.1 --extra-index-url https://pypi.nvidia.com
   pip install polygraphy onnx-graphsurgeon --extra-index-url https://pypi.nvidia.com
   ```

2. Make sure CUDA 12.1+ is installed:
   ```bash
   nvcc --version
   ```

3. Try with xformers first to verify basic setup:
   ```bash
   python main.py --acceleration xformers
   ```

4. If compilation takes too long, it's normal for the first run (5-10 minutes)

### TensorRT TracerWarnings

These warnings are normal during first-time compilation and can be ignored.

## Performance Issues

### Low FPS

**Solutions:**

1. Use TensorRT acceleration:
   ```bash
   make start  # or python main.py --acceleration tensorrt
   ```

2. Lower resolution in `main.py`:
   ```python
   WIDTH = 256
   HEIGHT = 256
   ```

3. Check GPU usage:
   ```bash
   # Monitor GPU while running
   watch -n 1 nvidia-smi
   ```

4. Close other GPU applications:
   ```bash
   # Check what's using GPU
   nvidia-smi
   ```

5. Reduce denoising steps in `main.py`:
   ```python
   T_INDEX_LIST = [30, 40]  # Lower values
   ```

### First frame is very slow

This is normal - the model needs to warm up. Subsequent frames will be faster.

## Numpy Version Conflicts

### opencv-python requires numpy>=2 but you have numpy 1.26.4

This warning can be ignored. The code works fine with numpy 1.26.4. OpenCV's metadata is overly strict.

**If it causes issues:**
```bash
pip install "numpy<2"
```

## General Debugging

### Enable verbose logging

Add to the top of `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check installed versions

```bash
# Activate environment
conda activate streamdiffusion
# or
source ~/.virtualenvs/streamdiffusion/bin/activate

# Check versions
pip list | grep -E "torch|diffusers|transformers|huggingface|accelerate|xformers"
```

### Clean reinstall

```bash
# Remove environment
conda env remove -n streamdiffusion
# or
rm -rf ~/.virtualenvs/streamdiffusion

# Remove StreamDiffusion
rm -rf ~/Projects/StreamDiffusion

# Clean cache
make clean

# Reinstall
make install
# or
make install-venv
```

## Getting Help

If you're still having issues:

1. Check the logs:
   ```bash
   tail -f /tmp/sd-ndi.log
   ```

2. Run in test mode:
   ```bash
   make test
   ```

3. Verify all prerequisites:
   ```bash
   make check-compat
   make check-deps
   ```

4. For StreamDiffusion issues: https://github.com/cumulo-autumn/StreamDiffusion/issues
5. For NDI issues: https://ndi.tv/support/
6. For this repo issues: Create an issue on GitHub
