@echo off
REM StreamDiffusion NDI Starter Script (Windows)

echo ========================================
echo   StreamDiffusion NDI Real-time Processor
echo ========================================
echo.

REM ===== CONFIGURE THESE PATHS FOR YOUR SYSTEM =====
REM Set HuggingFace cache location (optional, can be commented out)
set HF_HOME=C:\huggingface_cache

REM Set Python path - UPDATE THIS to match your conda environment location
set PYTHON_BIN=C:\miniconda3\envs\streamdiffusion\python.exe
REM ================================================

REM Change to script directory
cd /d "%~dp0"

echo Working directory: %CD%
echo Python: %PYTHON_BIN%
echo HuggingFace cache: %HF_HOME%
echo.

REM Run with TensorRT for maximum performance (slower first-time startup)
REM Change to --acceleration xformers for faster startup if needed
echo Starting NDI processor...
echo.

"%PYTHON_BIN%" main.py --acceleration tensorrt %*

echo.
echo NDI processor stopped.
