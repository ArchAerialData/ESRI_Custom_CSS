@echo off
REM ESRI Scene Viewer HTML Generator Launcher
REM Double-click this file to launch the GUI application

cd /d "%~dp0"
python scene-viewer-generator.py

REM If Python not in PATH, try py launcher
if errorlevel 1 (
    py scene-viewer-generator.py
)

REM If still fails, show error
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
)
