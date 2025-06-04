$ErrorActionPreference = "Stop"

$MODEL_NAME = "llama4:scout"
$CUSTOM_MODEL_NAME = "rtl-debugger"
# $MODEL_PATH = "$env:USERPROFILE\.ollama\models\manifests\$MODEL_NAME"

# Pull base model if needed
Write-Host "[INFO] Pulling $MODEL_NAME..."
ollama pull $MODEL_NAME

# Create temporary training directory
New-Item -ItemType Directory -Force -Path "training/tmp" | Out-Null

# Combine .sv files
Get-Content training/rtl/*.sv | Set-Content training/tmp/rtl.txt

# Convert PDFs to text
if (-Not (Test-Path "training/tmp/docs.txt")) {
    Write-Host "[INFO] Extracting text from PDFs..."
    python py/pdftotext.py
}

# Combine RTL and docs text
Get-Content training/tmp/rtl.txt, training/tmp/docs.txt | Set-Content training/tmp/train.txt

# Train with Modelfile
Write-Host "[INFO] Creating Ollama model $CUSTOM_MODEL_NAME..."
ollama create $CUSTOM_MODEL_NAME -f "training/Modelfile"

Write-Host "[INFO] Done! You can now run:"
Write-Host "  ollama run $CUSTOM_MODEL_NAME"