# PowerShell script to build frontend and copy dist to public
# Usage: .\scripts\frontend-build.ps1

Set-StrictMode -Version Latest

$frontendDir = Join-Path $PSScriptRoot '..\frontend'
$distDir = Join-Path $frontendDir 'dist'
$publicDir = Join-Path $PSScriptRoot '..\public'

Write-Host "Building frontend in $frontendDir"
if (-Not (Test-Path $frontendDir)) {
    Write-Error "Frontend directory not found: $frontendDir"
    exit 1
}

Push-Location $frontendDir
if (Test-Path package-lock.json) {
    Write-Host "Running npm ci"
    npm ci
} else {
    Write-Host "Running npm install"
    npm install
}

Write-Host "Running npm run build"
npm run build
Pop-Location

if (-Not (Test-Path $distDir)) {
    Write-Error "Build did not produce dist folder: $distDir"
    exit 2
}

Write-Host "Copying $distDir to $publicDir"
if (-Not (Test-Path $publicDir)) { New-Item -ItemType Directory -Path $publicDir | Out-Null }
Remove-Item -Path (Join-Path $publicDir '*') -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -Path (Join-Path $distDir '*') -Destination $publicDir -Recurse -Force
Write-Host "Frontend build and copy complete."