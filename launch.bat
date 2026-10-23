@echo off
title Adobe Enhance Speech Clone - Quick Launcher
echo ========================================================
echo   Starting Adobe Podcast Enhance Speech (Local Clone)
echo ========================================================
echo.
echo Checking and installing dependencies...
python -m pip install -r requirements.txt --quiet
echo.
echo Launching Web Interface...
start "" http://127.0.0.1:7860
python app.py
pause
