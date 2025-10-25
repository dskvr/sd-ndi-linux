.PHONY: help check-deps check-compat install install-prereqs install-env install-deps start stop restart status clean
.PHONY: install-venv install-env-venv install-deps-venv

# Configuration
ENV_TYPE ?= conda  # Options: conda, venv
CONDA_ENV := streamdiffusion
CONDA_BIN := $(shell which conda 2>/dev/null || echo "$(HOME)/Downloads/.miniconda3/bin/conda")
VENV_PATH := $(HOME)/.virtualenvs/streamdiffusion
STREAMDIFFUSION_PATH := $(HOME)/Projects/StreamDiffusion
NDI_SDK_PATH := $(HOME)/Downloads/NDI SDK for Linux
NDI_LIB_PATH := $(NDI_SDK_PATH)/lib/x86_64-linux-gnu

# Environment-specific settings
ifeq ($(ENV_TYPE),venv)
    PYTHON_BIN := $(VENV_PATH)/bin/python
    PIP_BIN := $(VENV_PATH)/bin/pip
    ACTIVATE_CMD := . $(VENV_PATH)/bin/activate
else
    PYTHON_BIN := $(HOME)/Downloads/.miniconda3/envs/$(CONDA_ENV)/bin/python
    PIP_BIN := $(HOME)/Downloads/.miniconda3/envs/$(CONDA_ENV)/bin/pip
    ACTIVATE_CMD := . $(HOME)/Downloads/.miniconda3/etc/profile.d/conda.sh && conda activate $(CONDA_ENV)
endif

## help: Display this help message
help:
	@echo "StreamDiffusion NDI - Makefile Commands"
	@echo "========================================"
	@echo ""
	@echo "Setup Commands (Conda - default):"
	@echo "  make check-compat     - Check system compatibility"
	@echo "  make check-deps       - Check if all dependencies are installed"
	@echo "  make install          - Full installation (all steps)"
	@echo "  make install-prereqs  - Install system prerequisites only"
	@echo "  make install-env      - Create conda environment only"
	@echo "  make install-deps     - Install Python dependencies only"
	@echo ""
	@echo "Setup Commands (venv alternative):"
	@echo "  make install-venv     - Full installation using Python venv"
	@echo "  make install-env-venv - Create venv environment only"
	@echo "  make install-deps-venv- Install dependencies in venv"
	@echo ""
	@echo "Service Commands:"
	@echo "  make start            - Start the NDI processor"
	@echo "  make stop             - Stop the NDI processor"
	@echo "  make restart          - Restart the NDI processor"
	@echo "  make status           - Check if the processor is running"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean            - Clean up temporary files and caches"
	@echo "  make test             - Run a quick test of the application"
	@echo ""
	@echo "Environment Variables:"
	@echo "  ENV_TYPE=venv         - Use venv instead of conda (e.g., make start ENV_TYPE=venv)"
	@echo ""

## check-compat: Check system compatibility
check-compat:
	@echo "Checking system compatibility..."
	@echo ""
	@echo "=== OS Check ==="
	@uname -a | grep -q Linux && echo "✓ Linux detected" || (echo "✗ Not running Linux" && exit 1)
	@echo ""
	@echo "=== GPU Check ==="
	@if command -v nvidia-smi >/dev/null 2>&1; then \
		echo "✓ NVIDIA GPU detected:"; \
		nvidia-smi --query-gpu=name,memory.total --format=csv,noheader; \
	else \
		echo "✗ NVIDIA GPU not found or nvidia-smi not installed"; \
		exit 1; \
	fi
	@echo ""
	@echo "System is compatible!"

## check-deps: Check if all dependencies are installed
check-deps:
	@echo "Checking dependencies..."
	@echo ""
	@echo "=== CUDA ==="
	@if command -v nvcc >/dev/null 2>&1; then \
		echo "✓ CUDA installed:"; \
		nvcc --version | grep "release"; \
	else \
		echo "✗ CUDA not found in PATH"; \
		echo "  Run: make install-prereqs"; \
	fi
	@echo ""
	@echo "=== Conda ==="
	@if [ -f "$(CONDA_BIN)" ]; then \
		echo "✓ Conda installed:"; \
		$(CONDA_BIN) --version; \
	else \
		echo "✗ Conda not found"; \
		echo "  Run: make install-prereqs"; \
	fi
	@echo ""
	@echo "=== NDI SDK ==="
	@if [ -d "$(NDI_SDK_PATH)" ] && [ -f "$(NDI_LIB_PATH)/libndi.so.6.2.1" ]; then \
		echo "✓ NDI SDK found at $(NDI_SDK_PATH)"; \
	else \
		echo "✗ NDI SDK not found"; \
		echo "  Download from https://ndi.tv/sdk/"; \
	fi
	@echo ""
	@echo "=== Conda Environment ==="
	@if [ -d "$(HOME)/Downloads/.miniconda3/envs/$(CONDA_ENV)" ]; then \
		echo "✓ Environment '$(CONDA_ENV)' exists"; \
	else \
		echo "✗ Environment '$(CONDA_ENV)' not found"; \
		echo "  Run: make install-env"; \
	fi
	@echo ""
	@echo "=== StreamDiffusion ==="
	@if [ -d "$(STREAMDIFFUSION_PATH)" ]; then \
		echo "✓ StreamDiffusion found at $(STREAMDIFFUSION_PATH)"; \
	else \
		echo "✗ StreamDiffusion not found"; \
		echo "  Run: make install-deps"; \
	fi
	@echo ""

## install: Full installation
install: check-compat install-prereqs install-env install-deps
	@echo ""
	@echo "========================================"
	@echo "Installation complete!"
	@echo "========================================"
	@echo ""
	@echo "To start the processor:"
	@echo "  make start"
	@echo ""
	@echo "Or run manually:"
	@echo "  ./start.sh"
	@echo ""

## install-prereqs: Install system prerequisites
install-prereqs:
	@echo "Installing system prerequisites..."
	@echo ""
	@echo "NOTE: Some steps require manual action."
	@echo ""
	@echo "=== CUDA ==="
	@if ! command -v nvcc >/dev/null 2>&1; then \
		echo "CUDA not found. Please install manually:"; \
		echo ""; \
		echo "Arch Linux:"; \
		echo "  sudo pacman -S cuda cuda-tools"; \
		echo ""; \
		echo "Ubuntu/Debian:"; \
		echo "  See README.md for installation instructions"; \
		echo ""; \
		echo "After installation, add to ~/.zshrc or ~/.bashrc:"; \
		echo "  export PATH=/opt/cuda/bin:\$$PATH"; \
		echo "  export LD_LIBRARY_PATH=/opt/cuda/lib64:\$$LD_LIBRARY_PATH"; \
		echo ""; \
		read -p "Press Enter when CUDA is installed..."; \
	else \
		echo "✓ CUDA already installed"; \
	fi
	@echo ""
	@echo "=== Conda ==="
	@if [ ! -f "$(CONDA_BIN)" ]; then \
		echo "Installing Miniconda..."; \
		cd $(HOME)/Downloads && \
		wget -nc https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
		bash Miniconda3-latest-Linux-x86_64.sh -b -p $(HOME)/Downloads/.miniconda3 && \
		$(HOME)/Downloads/.miniconda3/bin/conda init $$(basename $$SHELL); \
		echo ""; \
		echo "Conda installed. Please restart your shell and run 'make install' again."; \
		exit 1; \
	else \
		echo "✓ Conda already installed"; \
	fi
	@echo ""
	@echo "=== NDI SDK ==="
	@if [ ! -d "$(NDI_SDK_PATH)" ]; then \
		echo "NDI SDK not found. Please download and install manually:"; \
		echo ""; \
		echo "1. Download from: https://ndi.tv/sdk/"; \
		echo "2. Extract to ~/Downloads/"; \
		echo "3. Run the installer: ./Install_NDI_SDK_v*.sh"; \
		echo ""; \
		echo "After installation, add to ~/.zshrc or ~/.bashrc:"; \
		echo "  export LD_LIBRARY_PATH=\"\$$HOME/Downloads/NDI SDK for Linux/lib/x86_64-linux-gnu:\$$LD_LIBRARY_PATH\""; \
		echo ""; \
		read -p "Press Enter when NDI SDK is installed..."; \
	else \
		echo "✓ NDI SDK already installed"; \
	fi

## install-env: Create conda environment
install-env:
	@echo "Creating conda environment..."
	@if [ ! -d "$(HOME)/Downloads/.miniconda3/envs/$(CONDA_ENV)" ]; then \
		. $(HOME)/Downloads/.miniconda3/etc/profile.d/conda.sh && \
		conda create -n $(CONDA_ENV) python=3.10 -y; \
		echo "✓ Environment created"; \
	else \
		echo "✓ Environment already exists"; \
	fi

## install-venv: Full installation using Python venv
install-venv: check-compat install-env-venv install-deps-venv
	@echo ""
	@echo "========================================"
	@echo "Installation complete (venv)!"
	@echo "========================================"
	@echo ""
	@echo "To start the processor:"
	@echo "  make start ENV_TYPE=venv"
	@echo ""
	@echo "Or activate manually:"
	@echo "  source $(VENV_PATH)/bin/activate"
	@echo "  python main.py"
	@echo ""

## install-env-venv: Create Python venv environment
install-env-venv:
	@echo "Creating Python venv environment..."
	@if [ ! -d "$(VENV_PATH)" ]; then \
		python3.10 -m venv $(VENV_PATH); \
		echo "✓ Venv created at $(VENV_PATH)"; \
	else \
		echo "✓ Venv already exists"; \
	fi

## install-deps-venv: Install dependencies in venv
install-deps-venv:
	@echo "Installing Python dependencies in venv..."
	@. $(VENV_PATH)/bin/activate && \
	echo "Installing core dependencies with locked versions..." && \
	pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu121 && \
	pip install xformers==0.0.22.post7 && \
	pip install "numpy<2" && \
	echo "Installing base packages without dependency resolution..." && \
	pip install --no-deps "huggingface_hub==0.19.4" && \
	pip install --no-deps "tokenizers==0.14.1" && \
	pip install --no-deps "transformers==4.35.0" && \
	pip install --no-deps "diffusers==0.24.0" && \
	pip install --no-deps "accelerate==0.24.0" && \
	echo "Installing supporting dependencies..." && \
	pip install "filelock" "fsspec>=2023.5.0" "packaging>=20.0" "pyyaml>=5.1" && \
	pip install "regex!=2019.12.17" "requests" "safetensors>=0.3.1" "tqdm>=4.27" && \
	pip install "psutil" "typing-extensions>=3.7.4.3" && \
	echo "Installing opencv-python and NDI..." && \
	pip install ndi-python && \
	pip install "opencv-python<4.8" && \
	pip install "numpy<2" && \
	echo "Cloning StreamDiffusion..." && \
	if [ ! -d "$(STREAMDIFFUSION_PATH)" ]; then \
		mkdir -p $(HOME)/Projects && \
		cd $(HOME)/Projects && \
		git clone https://github.com/cumulo-autumn/StreamDiffusion.git; \
	fi && \
	echo "Installing StreamDiffusion (with --no-deps)..." && \
	cd $(STREAMDIFFUSION_PATH) && \
	pip install --no-deps -e . && \
	echo "Final version verification..." && \
	pip install "numpy<2" && \
	echo "Installing TinyVAE and TensorRT..." && \
	python -m streamdiffusion.tools.install-tensorrt && \
	echo "✓ All dependencies installed"

## install-deps: Install Python dependencies and StreamDiffusion
install-deps:
	@echo "Installing Python dependencies..."
	@. $(HOME)/Downloads/.miniconda3/etc/profile.d/conda.sh && \
	conda activate $(CONDA_ENV) && \
	echo "Installing core dependencies with locked versions..." && \
	pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu121 && \
	pip install xformers==0.0.22.post7 && \
	pip install "numpy<2" && \
	echo "Installing base packages without dependency resolution..." && \
	pip install --no-deps "huggingface_hub==0.19.4" && \
	pip install --no-deps "tokenizers==0.14.1" && \
	pip install --no-deps "transformers==4.35.0" && \
	pip install --no-deps "diffusers==0.24.0" && \
	pip install --no-deps "accelerate==0.24.0" && \
	echo "Installing supporting dependencies..." && \
	pip install "filelock" "fsspec>=2023.5.0" "packaging>=20.0" "pyyaml>=5.1" && \
	pip install "regex!=2019.12.17" "requests" "safetensors>=0.3.1" "tqdm>=4.27" && \
	pip install "psutil" "typing-extensions>=3.7.4.3" && \
	echo "Installing opencv-python and NDI..." && \
	pip install ndi-python && \
	pip install "opencv-python<4.8" && \
	pip install "numpy<2" && \
	echo "Cloning StreamDiffusion..." && \
	if [ ! -d "$(STREAMDIFFUSION_PATH)" ]; then \
		mkdir -p $(HOME)/Projects && \
		cd $(HOME)/Projects && \
		git clone https://github.com/cumulo-autumn/StreamDiffusion.git; \
	fi && \
	echo "Installing StreamDiffusion (with --no-deps)..." && \
	cd $(STREAMDIFFUSION_PATH) && \
	pip install --no-deps -e . && \
	echo "Final version verification..." && \
	pip install "numpy<2" && \
	echo "Installing TinyVAE and TensorRT..." && \
	python -m streamdiffusion.tools.install-tensorrt && \
	echo "✓ All dependencies installed"

## start: Start the NDI processor
start:
	@echo "Starting StreamDiffusion NDI processor ($(ENV_TYPE))..."
	@if [ -f /tmp/sd-ndi.pid ] && kill -0 $$(cat /tmp/sd-ndi.pid) 2>/dev/null; then \
		echo "Processor is already running (PID: $$(cat /tmp/sd-ndi.pid))"; \
		exit 1; \
	fi
	@$(ACTIVATE_CMD) && \
	nohup $(PYTHON_BIN) main.py --acceleration xformers --streamdiffusion-path "$(STREAMDIFFUSION_PATH)" > /tmp/sd-ndi.log 2>&1 & echo $$! > /tmp/sd-ndi.pid
	@echo "Processor started (PID: $$(cat /tmp/sd-ndi.pid))"
	@echo "Logs: /tmp/sd-ndi.log"

## stop: Stop the NDI processor
stop:
	@if [ -f /tmp/sd-ndi.pid ]; then \
		if kill -0 $$(cat /tmp/sd-ndi.pid) 2>/dev/null; then \
			echo "Stopping processor (PID: $$(cat /tmp/sd-ndi.pid))..."; \
			kill $$(cat /tmp/sd-ndi.pid); \
			rm /tmp/sd-ndi.pid; \
			echo "Processor stopped"; \
		else \
			echo "Processor not running (stale PID file)"; \
			rm /tmp/sd-ndi.pid; \
		fi \
	else \
		echo "Processor not running (no PID file)"; \
	fi

## restart: Restart the NDI processor
restart: stop
	@sleep 2
	@$(MAKE) start

## status: Check if the processor is running
status:
	@if [ -f /tmp/sd-ndi.pid ] && kill -0 $$(cat /tmp/sd-ndi.pid) 2>/dev/null; then \
		echo "Processor is running (PID: $$(cat /tmp/sd-ndi.pid))"; \
		echo ""; \
		echo "Recent logs:"; \
		tail -n 10 /tmp/sd-ndi.log 2>/dev/null || echo "No logs available"; \
	else \
		echo "Processor is not running"; \
		if [ -f /tmp/sd-ndi.pid ]; then \
			rm /tmp/sd-ndi.pid; \
		fi \
	fi

## clean: Clean up temporary files and caches
clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__
	@rm -f /tmp/sd-ndi.pid
	@rm -f /tmp/sd-ndi.log
	@echo "✓ Cleanup complete"

## test: Run a quick test
test:
	@echo "Running quick test ($(ENV_TYPE))..."
	@$(ACTIVATE_CMD) && \
	$(PYTHON_BIN) main.py --timeout 3
