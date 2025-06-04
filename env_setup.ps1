$ErrorActionPreference = "Stop"

# Create a virtual environment in 'venv'
Write-Host "[INFO] Creating virtual environment..."
python -m venv venv

# Activate the virtual environment
Write-Host "[INFO] Activating virtual environment..."
. .\venv\Scripts\Activate.ps1

# Upgrade pip (optional but recommended)
python -m pip install --upgrade pip

# Install required Python packages
Write-Host "[INFO] Installing requirements..."
pip install -r requirements.txt