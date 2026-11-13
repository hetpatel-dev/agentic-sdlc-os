# ==============================================================================
# Agentic SDLC OS — Universal Installer for Windows PowerShell
# Installs Agentic SDLC OS globally for all Antigravity projects or locally into a project
# ==============================================================================
param(
    [switch]$Global,
    [switch]$Submodule,
    [switch]$Update,
    [string]$TargetDir = "."
)

$RepoUrl = "https://github.com/hetpatel-dev/agentic-sdlc-os.git"

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "         AGENTIC SDLC OS — UNIVERSAL PROJECT INSTALLER                          " -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

if ($Update) {
    # Upgrade existing project installation while preserving project files and tasks
    Write-Host "[UPDATE] Upgrading Agentic SDLC OS in project at '$TargetDir'..." -ForegroundColor Yellow
    $updateScript = Join-Path $PSScriptRoot "update.py"
    if (-not (Test-Path $updateScript)) {
        $updateScript = "scripts/update.py"
    }
    python $updateScript --target $TargetDir
    exit $LASTEXITCODE
}

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
    $sourceRoot = $null
    if (Test-Path (Join-Path $PSScriptRoot "..\plugin.json")) {
        $sourceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
    } elseif (Test-Path "plugin.json") {
        $sourceRoot = (Get-Location).Path
    }

    $isTemp = $false
    if ($sourceRoot) {
        Write-Host "[LOCAL] Deploying directly from local repository at '$sourceRoot'..." -ForegroundColor Yellow
        $tempSource = $sourceRoot
    } else {
        $tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("sdlc-os-" + [System.Guid]::NewGuid().ToString().Substring(0,8))
        Write-Host "[DOWNLOAD] Cloning latest release from GitHub..." -ForegroundColor Yellow
        git clone --depth 1 $RepoUrl $tempDir
        $tempSource = $tempDir
        $isTemp = $true
    }

    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null

    # Copy .agents, rules, skills, agents, scripts into target
    Write-Host "[DEPLOY] Copying .agents, scripts, skills, agents, rules to '$TargetDir'..." -ForegroundColor Yellow
    Copy-Item -Path "$tempSource\.agents" -Destination (Join-Path $TargetDir ".agents") -Recurse -Force
    Copy-Item -Path "$tempSource\scripts" -Destination (Join-Path $TargetDir "scripts") -Recurse -Force
    if (Test-Path (Join-Path $tempSource "skills")) {
        Copy-Item -Path "$tempSource\skills" -Destination (Join-Path $TargetDir "skills") -Recurse -Force
    }
    if (Test-Path (Join-Path $tempSource "agents")) {
        Copy-Item -Path "$tempSource\agents" -Destination (Join-Path $TargetDir "agents") -Recurse -Force
    }
    if (Test-Path (Join-Path $tempSource "rules")) {
        Copy-Item -Path "$tempSource\rules" -Destination (Join-Path $TargetDir "rules") -Recurse -Force
    }
    
    # Governance: Deploy schemas & quality gates; ensure clean empty traceability ledger for new projects
    $destGov = Join-Path $TargetDir "governance"
    New-Item -ItemType Directory -Path (Join-Path $destGov "schemas") -Force | Out-Null
    Copy-Item -Path "$tempSource\governance\schemas\*" -Destination (Join-Path $destGov "schemas") -Recurse -Force
    Copy-Item -Path "$tempSource\governance\quality_gates.json" -Destination $destGov -Force
    
    $destLedger = Join-Path $destGov "traceability_ledger.json"
    if (-not (Test-Path $destLedger)) {
        $cleanLedger = @'
{
  "version": "1.0.0",
  "system": "Agentic SDLC OS",
  "last_updated": "2026-11-13T00:00:00Z",
  "objectives": {},
  "requirements": {},
  "adrs": {},
  "tasks": {}
}
'@
        $utf8NoBom = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllText($destLedger, $cleanLedger, $utf8NoBom)
    }

    # Docs: Create empty directory structure and deploy templates ONLY (never scaffold testing/sample artifacts)
    $destDocs = Join-Path $TargetDir "docs"
    $docDirs = @(
        "adr", "api", "architecture", "database", "governance", 
        "operations", "product", "releases", "requirements", 
        "security", "testing", "testing\performance", "templates"
    )
    foreach ($d in $docDirs) {
        New-Item -ItemType Directory -Path (Join-Path $destDocs $d) -Force | Out-Null
    }
    Copy-Item -Path "$tempSource\docs\templates\*" -Destination (Join-Path $destDocs "templates") -Recurse -Force

    if (-not (Test-Path (Join-Path $TargetDir "AGENTS.md"))) {
        Copy-Item -Path "$tempSource\AGENTS.md" -Destination $TargetDir -Force
    }
    if (-not (Test-Path (Join-Path $TargetDir "GEMINI.md"))) {
        Copy-Item -Path "$tempSource\GEMINI.md" -Destination $TargetDir -Force
    }
    if (-not (Test-Path (Join-Path $TargetDir ".gitignore"))) {
        Copy-Item -Path "$tempSource\.gitignore" -Destination $TargetDir -Force
    }
    
    # Clean up temp if cloned
    if ($isTemp) {
        Remove-Item -Path $tempSource -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "       [SUCCESS] AGENTIC SDLC OS INSTALLED INTO YOUR PROJECT!                  " -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Run bootstrap to verify environment:"
Write-Host "   powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1"
Write-Host "2. Start delegating to 'sdlc-orchestrator' or invoke any of the 18 SDLC skills."
