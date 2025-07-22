# SOVR Pay Ultimate Startup Script
# PowerShell script for complete SOVR Pay environment setup

param(
    [switch]$SkipNgrok,
    [switch]$SkipBackend,
    [switch]$SkipDashboard,
    [string]$Port = "8000"
)

# Configuration
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Colors
$Colors = @{
    Green = "`e[32m"
    Red = "`e[31m"
    Yellow = "`e[33m"
    Blue = "`e[34m"
    Reset = "`e[0m"
}

function Write-Status {
    param(
        [string]$Message,
        [string]$Type = "Info"
    )
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    $color = switch ($Type) {
        "Success" { $Colors.Green }
        "Error" { $Colors.Red }
        "Warning" { $Colors.Yellow }
        "Info" { $Colors.Blue }
        default { $Colors.Reset }
    }
    
    Write-Host "${color}[$timestamp] $Message$($Colors.Reset)"
}

function Test-Command {
    param([string]$Command)
    $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

function Start-Backend {
    Write-Status "Starting SOVR Pay Backend..." "Info"
    
    $backendDir = Join-Path $PSScriptRoot "backend"
    if (-not (Test-Path $backendDir)) {
        Write-Status "Backend directory not found: $backendDir" "Error"
        return $false
    }
    
    # Check Python
    if (-not (Test-Command "python")) {
        Write-Status "Python not found. Please install Python 3.8+" "Error"
        return $false
    }
    
    # Install dependencies
    $requirements = Join-Path $backendDir "requirements.txt"
    if (Test-Path $requirements) {
        Write-Status "Installing Python dependencies..." "Info"
        try {
            & python -m pip install -r $requirements
            Write-Status "Dependencies installed successfully" "Success"
        } catch {
            Write-Status "Failed to install dependencies: $_" "Warning"
        }
    }
    
    # Start backend
    try {
        $backendProcess = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", $Port, "--reload" -WorkingDirectory $backendDir -PassThru -NoNewWindow
        Write-Status "Backend started on port $Port" "Success"
        return $backendProcess
    } catch {
        Write-Status "Failed to start backend: $_" "Error"
        return $null
    }
}

function Start-Ngrok {
    Write-Status "Starting ngrok tunnel..." "Info"
    
    if (-not (Test-Command "ngrok")) {
        Write-Status "ngrok not found. Please install from https://ngrok.com/download" "Error"
        return $null
    }
    
    try {
        $ngrokProcess = Start-Process -FilePath "ngrok" -ArgumentList "http", $Port -PassThru -NoNewWindow
        Write-Status "ngrok tunnel started" "Success"
        return $ngrokProcess
    } catch {
        Write-Status "Failed to start ngrok: $_" "Error"
        return $null
    }
}

function Get-NgrokUrl {
    Write-Status "Fetching ngrok URL..." "Info"
    
    $maxAttempts = 30
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -TimeoutSec 5
            $httpsTunnel = $response.tunnels | Where-Object { $_.proto -eq "https" }
            if ($httpsTunnel) {
                $url = $httpsTunnel.public_url
                Write-Status "ngrok URL: $url" "Success"
                return $url
            }
        } catch {
            Write-Status "Waiting for ngrok..." "Info"
        }
        
        $attempt++
        Start-Sleep 1
    }
    
    Write-Status "Failed to get ngrok URL" "Warning"
    return $null
}

function Update-EnvironmentFiles {
    param([string]$NgrokUrl)
    
    Write-Status "Updating environment files..." "Info"
    
    $envFiles = @(".env.production", ".env.development")
    
    foreach ($envFile in $envFiles) {
        $envPath = Join-Path $PSScriptRoot $envFile
        $content = @"
VITE_API_BASE_URL=$NgrokUrl
ENVIRONMENT=production
PORT=$Port
"@
        Set-Content -Path $envPath -Value $content -Force
        Write-Status "Updated $envFile" "Success"
    }
}

function Start-Dashboard {
    Write-Status "Opening dashboard..." "Info"
    
    $dashboardPath = Join-Path $PSScriptRoot "dashboard" "dashboard.html"
    if (Test-Path $dashboardPath) {
        Start-Process $dashboardPath
        Write-Status "Dashboard opened" "Success"
    } else {
        Write-Status "Dashboard not found at $dashboardPath" "Warning"
    }
}

function Show-Status {
    param(
        [string]$BackendUrl,
        [string]$NgrokUrl
    )
    
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "🎯 SOVR Pay System Status" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "📖 API Documentation: $($NgrokUrl ?? $BackendUrl)/docs" -ForegroundColor Green
    Write-Host "❤️  Health Check: $($NgrokUrl ?? $BackendUrl)/health" -ForegroundColor Green
    Write-Host "🌐 Local Backend: $BackendUrl" -ForegroundColor Blue
    if ($NgrokUrl) {
        Write-Host "🔗 Public URL: $NgrokUrl" -ForegroundColor Blue
    }
    Write-Host "=" * 60 -ForegroundColor Cyan
}

# Main execution
try {
    Write-Host @"
    
    ███████╗ ██████╗  ██████╗ ██████╗ ███████╗
    ██╔════╝██╔═══██╗██╔═══██╗██╔══██╗██╔════╝
    ███████╗██║   ██║██║   ██║██████╔╝█████╗  
    ╚════██║██║   ██║██║   ██║██╔══██╗██╔══╝  
    ███████║╚██████╔╝╚██████╔╝██║  ██║███████╗
    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝
    
    SOVR Pay Ultimate Startup Script v2.0
    Enterprise Financial Infrastructure
    
"@ -ForegroundColor Cyan
    
    $backendUrl = "http://localhost:$Port"
    
    # Start backend if not skipped
    if (-not $SkipBackend) {
        $backendProcess = Start-Backend
        if (-not $backendProcess) {
            Write-Status "Failed to start backend" "Error"
            exit 1
        }
        
        # Wait for backend to be ready
        Write-Status "Waiting for backend to be ready..." "Info"
        Start-Sleep 3
    }
    
    # Start ngrok if not skipped
    $ngrokUrl = $null
    if (-not $SkipNgrok) {
        $ngrokProcess = Start-Ngrok
        if ($ngrokProcess) {
            $ngrokUrl = Get-NgrokUrl
            if ($ngrokUrl) {
                Update-EnvironmentFiles -NgrokUrl $ngrokUrl
            }
        }
    }
    
    # Open dashboard if not skipped
    if (-not $SkipDashboard) {
        Start-Sleep 2
        Start-Dashboard
    }
    
    # Show final status
    Show-Status -BackendUrl $backendUrl -NgrokUrl $ngrokUrl
    
    Write-Status "All services started successfully! Press Ctrl+C to stop" "Success"
    
    # Keep running
    while ($true) {
        Start-Sleep 1
    }
    
} catch {
    Write-Status "Error: $_" "Error"
    exit 1
}
