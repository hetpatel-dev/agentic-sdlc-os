# ==============================================================================
# Agentic SDLC OS — Universal Installer for Windows PowerShell
# Installs Agentic SDLC OS globally for all Antigravity projects or locally into a project
# ==============================================================================
param(
    [switch]$Global,
    [switch]$Submodule,
    [string]$TargetDir = "."
)

$RepoUrl = "https://github.com/hetpatel-dev/agentic-sdlc-os.git"

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "         AGENTIC SDLC OS — UNIVERSAL PROJECT INSTALLER                          " -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

if ($Global) {
    # 1. Global Installation (Available across all projects on this machine)
    $pluginDir = Join-Path $HOME ".gemini\config\plugins\agentic-sdlc-os"
    Write-Host "[INSTALL] Installing Agentic SDLC OS globally to $pluginDir..." -ForegroundColor Yellow
    
    $sourceRoot = $null
    if (Test-Path (Join-Path $PSScriptRoot "..\plugin.json")) {
        $sourceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
    } elseif (Test-Path "plugin.json") {
        $sourceRoot = (Get-Location).Path
    }

    if ($sourceRoot) {
        Write-Host "[LOCAL] Copying directly from local repository at '$sourceRoot'..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $pluginDir -Force | Out-Null
        Copy-Item -Path "$sourceRoot\*" -Destination $pluginDir -Recurse -Force -Exclude ".git"
    } elseif (Test-Path $pluginDir) {
        Write-Host "[UPDATE] Existing global installation found. Updating from GitHub..." -ForegroundColor Yellow
        git -C $pluginDir pull origin main
    } else {
        New-Item -ItemType Directory -Path (Split-Path $pluginDir) -Force | Out-Null
        git clone $RepoUrl $pluginDir
    }
    
    # Enable in global plugins config if needed
    Write-Host "[OK] Global installation complete! Agentic SDLC OS is now active across all projects." -ForegroundColor Green
    Write-Host "     Verify with: agy plugin list" -ForegroundColor Yellow
    exit 0
}

# 2. Local Project Installation
Write-Host "[INSTALL] Installing Agentic SDLC OS into project at '$TargetDir'..." -ForegroundColor Yellow

if ($Submodule) {
    Write-Host "[GIT] Adding as git submodule at '.agents/sdlc-os'..." -ForegroundColor Yellow
    git submodule add $RepoUrl .agents/sdlc-os
} else {
    $tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("sdlc-os-" + [System.Guid]::NewGuid().ToString().Substring(0,8))
    Write-Host "[DOWNLOAD] Cloning latest release from GitHub..." -ForegroundColor Yellow
    git clone --depth 1 $RepoUrl $tempDir

    # Copy .agents, rules, skills, governance, docs, scripts into target
    Write-Host "[DEPLOY] Copying .agents, governance, docs, scripts to '$TargetDir'..." -ForegroundColor Yellow
    Copy-Item -Path "$tempDir\.agents" -Destination $TargetDir -Recurse -Force
    Copy-Item -Path "$tempDir\governance" -Destination $TargetDir -Recurse -Force
    Copy-Item -Path "$tempDir\scripts" -Destination $TargetDir -Recurse -Force
    
    if (-not (Test-Path (Join-Path $TargetDir "docs"))) {
        Copy-Item -Path "$tempDir\docs" -Destination $TargetDir -Recurse -Force
    } else {
        $destTemplates = Join-Path $TargetDir "docs\templates"
        New-Item -ItemType Directory -Path $destTemplates -Force | Out-Null
        Copy-Item -Path "$tempDir\docs\templates\*" -Destination $destTemplates -Recurse -Force
        foreach ($d in @("adr", "api", "architecture", "database", "governance", "operations", "product", "releases", "requirements", "security", "testing")) {
            New-Item -ItemType Directory -Path (Join-Path $TargetDir "docs\$d") -Force | Out-Null
        }
    }

    if (-not (Test-Path (Join-Path $TargetDir "AGENTS.md"))) {
        Copy-Item -Path "$tempDir\AGENTS.md" -Destination $TargetDir -Force
    }
    if (-not (Test-Path (Join-Path $TargetDir "GEMINI.md"))) {
        Copy-Item -Path "$tempDir\GEMINI.md" -Destination $TargetDir -Force
    }
    if (-not (Test-Path (Join-Path $TargetDir ".gitignore"))) {
        Copy-Item -Path "$tempDir\.gitignore" -Destination $TargetDir -Force
    }
    
    # Clean up temp
    Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "       [SUCCESS] AGENTIC SDLC OS INSTALLED INTO YOUR PROJECT!                  " -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Run bootstrap to verify environment:"
Write-Host "   powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1"
Write-Host "2. Start delegating to 'sdlc-orchestrator' or invoke any of the 18 SDLC skills."
