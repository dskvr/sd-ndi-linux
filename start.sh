#!/bin/bash
# StreamDiffusion NDI Starter Script (Linux)

echo "========================================"
echo "  StreamDiffusion NDI Real-time Processor"
echo "========================================"
echo

# ===== CONFIGURE THESE PATHS FOR YOUR SYSTEM =====
# Set HuggingFace cache location (optional, can be commented out)
export HF_HOME="$HOME/.cache/huggingface"

# Set Python path - UPDATE THIS to match your conda environment location
PYTHON_BIN="$HOME/miniconda3/envs/streamdiffusion/bin/python"

# Set StreamDiffusion path - UPDATE THIS to match your StreamDiffusion installation
STREAMDIFFUSION_PATH="$HOME/Projects/StreamDiffusion/streamdiffusion_repo"
# ================================================

# Change to script directory
cd "$(dirname "$0")"

echo "Working directory: $(pwd)"
echo "Python: $PYTHON_BIN"
echo "HuggingFace cache: $HF_HOME"
echo "StreamDiffusion path: $STREAMDIFFUSION_PATH"
echo

# Run with xformers for compatibility (TensorRT may have issues on Linux)
# Change to --acceleration tensorrt for maximum performance if TensorRT is properly configured
echo "Starting NDI processor..."
echo

"$PYTHON_BIN" main.py --acceleration xformers --streamdiffusion-path "$STREAMDIFFUSION_PATH" "$@"

echo
echo "NDI processor stopped."
