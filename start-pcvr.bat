@echo off
REM StreamDiffusion NDI Starter Script (PCVR NDI Source)

echo ========================================
echo   StreamDiffusion NDI Real-time Processor
echo   Auto-selecting: pcvr-obs-ndi-out
echo ========================================
echo.

REM Set environment
set HF_HOME=/d/huggingface_cache

REM Python path
set PYTHON_BIN=D:\miniconda3\envs\streamdiffusion\python.exe

REM Change to script directory
cd /d "%~dp0"

echo Working directory: %CD%
echo Python: %PYTHON_BIN%
echo HuggingFace cache: %HF_HOME%
echo.

REM Run with tensorrt and auto-select pcvr-obs-ndi-out source
echo Starting NDI processor with TensorRT acceleration...
echo.

"%PYTHON_BIN%" main.py --acceleration tensorrt --ndi-source pcvr-obs-ndi-out %*

echo.
echo NDI processor stopped.
