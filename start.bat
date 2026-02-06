@echo off
echo ⚖️  Legal Contract Assistant for Indian SMEs
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found
echo 🚀 Starting Legal Contract Assistant...
echo.
echo 🌐 The application will open in your browser at:
echo    http://localhost:8501
echo.
echo 🛑 Press Ctrl+C to stop the application
echo.

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "temp_documents" mkdir temp_documents

REM Create .env file if it doesn't exist
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ℹ️  Created .env file. Add API keys for full functionality.
    )
)

REM Launch the application
python -m streamlit run app.py --server.headless true --server.port 8501

pause