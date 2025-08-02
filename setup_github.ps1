# FolderPulse GitHub Setup Script
# This script will install Git (if needed) and set up the repository for GitHub

Write-Host "🚀 FolderPulse GitHub Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Function to check if Git is installed
function Test-GitInstalled {
    try {
        $gitVersion = git --version 2>$null
        if ($gitVersion) {
            Write-Host "✅ Git is already installed: $gitVersion" -ForegroundColor Green
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

# Function to install Git for Windows
function Install-Git {
    Write-Host "📥 Installing Git for Windows..." -ForegroundColor Yellow
    
    # Download Git for Windows installer
    $gitUrl = "https://github.com/git-for-windows/git/releases/latest/download/Git-2.42.0.2-64-bit.exe"
    $installerPath = "$env:TEMP\GitInstaller.exe"
    
    try {
        Write-Host "Downloading Git installer..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $gitUrl -OutFile $installerPath -ErrorAction Stop
        
        Write-Host "Running Git installer (this may take a few minutes)..." -ForegroundColor Yellow
        Start-Process -FilePath $installerPath -ArgumentList "/SILENT" -Wait
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        Write-Host "✅ Git installation completed!" -ForegroundColor Green
        
        # Clean up installer
        Remove-Item $installerPath -ErrorAction SilentlyContinue
        
        return $true
    }
    catch {
        Write-Host "❌ Failed to install Git: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to set up Git repository
function Setup-Repository {
    Write-Host "🔧 Setting up Git repository..." -ForegroundColor Yellow
    
    try {
        # Initialize repository
        git init
        Write-Host "✅ Repository initialized" -ForegroundColor Green
        
        # Add all files
        git add .
        Write-Host "✅ Files staged for commit" -ForegroundColor Green
        
        # Create initial commit
        git commit -m "Initial commit: FolderPulse - Modern folder management tool"
        Write-Host "✅ Initial commit created" -ForegroundColor Green
        
        return $true
    }
    catch {
        Write-Host "❌ Failed to set up repository: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to display next steps
function Show-NextSteps {
    Write-Host ""
    Write-Host "🎉 Repository setup complete!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps to complete GitHub backup:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Go to GitHub.com and create a new repository:" -ForegroundColor White
    Write-Host "   - Name: FolderPulse" -ForegroundColor Gray
    Write-Host "   - Description: Modern Python application for folder management" -ForegroundColor Gray
    Write-Host "   - Keep it Public or Private (your choice)" -ForegroundColor Gray
    Write-Host "   - Don't initialize with README (we already have one)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. After creating the repository, run these commands:" -ForegroundColor White
    Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/FolderPulse.git" -ForegroundColor Gray
    Write-Host "   git branch -M main" -ForegroundColor Gray
    Write-Host "   git push -u origin main" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Your code will be backed up to GitHub!" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: Replace 'YOUR_USERNAME' with your actual GitHub username" -ForegroundColor Yellow
}

# Main execution
try {
    # Check if we're in the right directory
    if (-not (Test-Path "src\main.py")) {
        Write-Host "❌ Please run this script from the FolderPulse root directory" -ForegroundColor Red
        exit 1
    }
    
    # Check if Git is installed
    if (-not (Test-GitInstalled)) {
        Write-Host "Git not found. Installing Git for Windows..." -ForegroundColor Yellow
        
        if (-not (Install-Git)) {
            Write-Host "❌ Git installation failed. Please install Git manually from https://git-scm.com/download/windows" -ForegroundColor Red
            exit 1
        }
        
        # Wait a moment for installation to complete
        Start-Sleep -Seconds 3
    }
    
    # Set up the repository
    if (Setup-Repository) {
        Show-NextSteps
    } else {
        Write-Host "❌ Repository setup failed" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ An error occurred: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎯 Setup script completed!" -ForegroundColor Cyan
