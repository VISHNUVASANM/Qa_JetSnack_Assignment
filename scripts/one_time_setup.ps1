# Run once from PowerShell (project folder):
#   powershell -ExecutionPolicy Bypass -File .\scripts\one_time_setup.ps1
#
# Does: Python deps, Appium 2 + UiAutomator2 driver, optional PATH / ANDROID_HOME.

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

Write-Host "== Python packages =="
python -m pip install -r requirements.txt

Write-Host "== Appium CLI (2.x works on Node 20.18; Appium 3 needs newer Node) =="
npm install -g appium@2.11.5
appium driver install uiautomator2 2>$null
if ($LASTEXITCODE -ne 0) {
  Write-Host "(Driver already installed is OK.)"
}

Write-Host "== Versions =="
appium --version
appium driver list --installed

$sdk = Join-Path $env:LOCALAPPDATA "Android\Sdk"
$pt = Join-Path $sdk "platform-tools"
$npm = Join-Path $env:APPDATA "npm"

Write-Host "== Optional: User PATH + ANDROID_HOME (close terminals after) =="
if (-not (Test-Path $pt)) {
  Write-Host "Skip PATH: not found $pt"
  exit 0
}

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $userPath) { $userPath = "" }
$parts = $userPath -split ';' | Where-Object { $_ -and $_.Trim() }
$changed = $false
foreach ($dir in @($pt, $npm)) {
  if ($parts -contains $dir) { continue }
  if (-not (Test-Path $dir)) { continue }
  $userPath = if ($userPath) { "$userPath;$dir" } else { $dir }
  $changed = $true
  Write-Host "Will append to User PATH: $dir"
}
if ($changed) {
  [Environment]::SetEnvironmentVariable("Path", $userPath, "User")
}
[Environment]::SetEnvironmentVariable("ANDROID_HOME", $sdk, "User")
Write-Host "ANDROID_HOME user variable set to: $sdk"
Write-Host "Done. Open a NEW terminal and run: adb devices"
