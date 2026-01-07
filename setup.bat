@echo off
echo ======================================
echo AI Assistant - Setup Script (Windows)
echo ======================================
echo.

echo Checking Python version...
python --version
if errorlevel 1 (
    echo Error: Python is not installed!
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install pipwin
pipwin install pyaudio
pip install -r requirements.txt

echo.
echo Setting up configuration...
if not exist .env (
    copy .env.example .env
    echo Created .env file. Please edit it with your API keys.
) else (
    echo .env file already exists.
)

echo.
echo ======================================
echo Setup complete!
echo ======================================
echo.
echo To activate the virtual environment:
echo   venv\Scripts\activate.bat
echo.
echo To run the assistant:
echo   python main.py --mode interactive
echo.
echo Don't forget to configure your API keys in .env file!
echo.
pause
