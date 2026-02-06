@echo off
REM Legal Contract Assistant - Windows Launcher
REM Quick launcher for Windows users

echo ⚖️  Legal Contract Assistant for Indian SMEs
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\Lib\site-packages\streamlit" (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    if exist ".env.example" (
        echo 🔧 Creating .env file...
        copy .env.example .env
        echo ⚠️  Please edit .env file and add your API keys
    )
)

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "temp_documents" mkdir temp_documents

echo.
echo ✅ Setup complete!
echo 🚀 Starting Legal Contract Assistant...
echo 🌐 Open your browser to: http://localhost:8501
echo 🛑 Press Ctrl+C to stop the application
echo.

REM Launch the application
python run.py

pause