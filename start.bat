@echo off
REM StreamDiffusion NDI Starter Script (Windows)

echo ========================================
echo   StreamDiffusion NDI Real-time Processor
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

REM Run with xformers by default (faster startup than tensorrt)
REM Add --acceleration tensorrt for maximum performance (slower first-time startup)
echo Starting NDI processor...
echo.

"%PYTHON_BIN%" main.py --acceleration xformers %*

echo.
echo NDI processor stopped.
