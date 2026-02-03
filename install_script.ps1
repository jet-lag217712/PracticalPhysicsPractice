# Exit on any error
$ErrorActionPreference = "Stop"

Write-Host "=== Quiz Bot One-Touch Installer ===`n"

# -------------------------------
# 1️⃣ Check Python
# -------------------------------
Write-Host "[Step 1] Checking if Python 3.10+ is installed..."

$pythonInstalled = $false
try {
    $versionOutput = python --version 2>&1
    if ($versionOutput -match "Python (\d+)\.(\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -ge 3 -and $minor -ge 10) {
            $pythonInstalled = $true
            Write-Host "Python detected: $versionOutput"
        }
    }
} catch {}

if (-not $pythonInstalled) {
    Write-Host "Python 3.10+ not detected. Downloading and installing Python..."

    $installerUrl = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
    $installerPath = "$env:TEMP\python_installer.exe"

    Write-Host "Downloading Python installer..."
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

    Write-Host "Running Python installer..."
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

    Write-Host "Python installation complete. Please restart PowerShell and re-run this script."
    exit
}

# -------------------------------
# 2️⃣ Ask for API Key
# -------------------------------
$API_KEY = Read-Host "Enter your Groq API Key"

# Save API Key to .env
$envFile = ".env"
Write-Host "Saving API Key to $envFile..."
@"
API_KEY=$API_KEY
"@ | Out-File -Encoding UTF8 $envFile

# -------------------------------
# 3️⃣ Create and activate virtual environment
# -------------------------------
Write-Host "`n[Step 2] Creating Python virtual environment..."
python -m venv venv

Write-Host "Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

# -------------------------------
# 4️⃣ Upgrade pip
# -------------------------------
Write-Host "[Step 3] Upgrading pip..."
pip install --upgrade pip

# -------------------------------
# 5️⃣ Install dependencies
# -------------------------------
Write-Host "[Step 4] Installing Python dependencies..."
pip install -r requirements.txt

# -------------------------------
# 6️⃣ Install Playwright Chromium
# -------------------------------
Write-Host "[Step 5] Installing Playwright Chromium..."
playwright install chromium

# -------------------------------
# 7️⃣ Build .exe
# -------------------------------
Write-Host "[Step 6] Building standalone executable..."
pyinstaller --onefile --name PracticalPhysicsPractice --add-data "web_helper.js;." main.py

Write-Host "`nBuild complete! Your executable is located at: dist\PracticalPhysicsPractice.exe"
Write-Host "You can now run the bot by double-clicking the executable or running:"
Write-Host "  dist\PracticalPhysicsPractice.exe"
Write-Host "`nThe program will prompt for the INIT_URL at runtime."
Write-Host "Your API_KEY is already saved in the .env file."
Write-Host "`n=== Installation Finished ==="
