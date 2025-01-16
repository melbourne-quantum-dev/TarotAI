# TarotAI Setup Script for Windows

# Check if uv is installed
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv could not be found. Installing..." -ForegroundColor Yellow
    pip install uv
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
uv venv .venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
.\.venv\Scripts\activate

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
uv pip install -r requirements.txt

# Verify installation
Write-Host "Verifying installation..." -ForegroundColor Cyan
python -c "import tarotai; print('TarotAI setup successful!')"

Write-Host ""
Write-Host "Setup complete! To activate the virtual environment, run:" -ForegroundColor Green
Write-Host "  .\.venv\Scripts\activate" -ForegroundColor White
