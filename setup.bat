@echo off
REM Installation script for Sound Design Studio development environment
REM Run this after creating your virtual environment

echo ========================================
echo Sound Design Studio - Setup Script
echo ========================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo ERROR: Virtual environment not detected!
    echo.
    echo Please create and activate a virtual environment first:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo.
    pause
    exit /b 1
)

echo Virtual environment detected: %VIRTUAL_ENV%
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ========================================
    echo INSTALLATION FAILED!
    echo ========================================
    echo.
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo You can now run the application:
echo   python sound_design_studio_v2.py
echo.
echo Or use the launcher:
echo   run_studio_v2.bat
echo.
echo To build an executable:
echo   build.bat
echo.
pause
