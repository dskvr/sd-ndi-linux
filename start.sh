#!/bin/bash
# StreamDiffusion NDI Starter Script

echo "========================================"
echo "  StreamDiffusion NDI Real-time Processor"
echo "========================================"
echo ""

# ===== CONFIGURE THESE PATHS FOR YOUR SYSTEM =====
# Set HuggingFace cache location (optional, can be commented out)
export HF_HOME=/c/huggingface_cache

# Set Python path - UPDATE THIS to match your conda environment location
PYTHON_BIN="C:/miniconda3/envs/streamdiffusion/python.exe"
# ================================================

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to script directory
cd "$SCRIPT_DIR"

echo "Working directory: $SCRIPT_DIR"
echo "Python: $PYTHON_BIN"
echo "HuggingFace cache: $HF_HOME"
echo ""

# Run with xformers by default (faster startup than tensorrt)
# Add --acceleration tensorrt for maximum performance (slower first-time startup)
echo "Starting NDI processor..."
echo ""

"$PYTHON_BIN" main.py --acceleration xformers "$@"

echo ""
echo "NDI processor stopped."
