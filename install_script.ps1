# Exit on any error
$ErrorActionPreference = "Stop"

Write-Host "=== Quiz Bot One-Touch Installer ===`n"

# Ask for API Key
$API_KEY = Read-Host "Enter your Groq API Key"

# Save API Key to .env
$envFile = ".env"
Write-Host "Saving API Key to $envFile..."
@"
API_KEY=$API_KEY
"@ | Out-File -Encoding UTF8 $envFile

# Create virtual environment
Write-Host "`nCreating Python virtual environment..."
python -m venv venv

# Activate venv
Write-Host "Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
Write-Host "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright and Chromium
Write-Host "Installing Playwright Chromium..."
playwright install chromium

# Build .exe with PyInstaller (custom name)
Write-Host "`nBuilding standalone executable..."
pyinstaller --onefile --name PracticalPhysicsPractice --add-data "web_helper.js;." main.py

Write-Host "`nBuild complete! Your executable is located at: dist\PracticalPhysicsPractice.exe"
Write-Host "You can now run the bot by double-clicking the executable or running:"
Write-Host "  dist\PracticalPhysicsPractice.exe"
Write-Host "`nThe program will prompt for the INIT_URL at runtime."
Write-Host "Your API_KEY is already saved in the .env file."
Write-Host "`n=== Installation Finished ==="
