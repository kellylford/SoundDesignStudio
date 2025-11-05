@echo off
REM Export all presets as WAV files for demonstration

echo ========================================
echo Sound Design Studio - Preset Exporter
echo ========================================
echo.
echo This will export all presets to WAV files...
echo.

python export_preset_demos.py

REM Copy README to the output folder
if exist preset_demos (
    echo.
    echo Copying documentation...
    copy /Y PRESET_DEMOS_README.md preset_demos\README.md > nul
    echo Documentation copied to preset_demos\README.md
)

echo.
echo Press any key to exit...
pause > nul
