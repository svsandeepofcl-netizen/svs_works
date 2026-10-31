$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir
$pythonExe = Join-Path $scriptDir "naukri_venv\Scripts\python.exe"

Write-Host "Starting Headless Naukri Profile Updater..." -ForegroundColor Cyan
& $pythonExe "main.py" @args
$exitCode = $LASTEXITCODE
Write-Host "Finished with exit code: $exitCode" -ForegroundColor ($exitCode -eq 0 ? 'Green' : 'Red')
exit $exitCode

