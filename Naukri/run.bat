@echo off
setlocal
cd /d "%~dp0"
echo Starting Headless Naukri Profile Updater...
"%~dp0naukri_venv\Scripts\python.exe" main.py %*
set EXIT_CODE=%ERRORLEVEL%
echo Exited with code %EXIT_CODE%
exit /b %EXIT_CODE%

