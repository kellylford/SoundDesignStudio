@echo off
REM Launcher for Sound Design Studio v2

echo Starting Sound Design Studio...

REM Check if virtual environment exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    python sound_design_studio_v2.py
) else (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to install dependencies.
    pause
)
