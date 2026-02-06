"""
Simple launcher for Legal Contract Assistant
Avoids complex checks and just starts the app
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    print("⚖️  Legal Contract Assistant for Indian SMEs")
    print("=" * 50)
    
    # Create directories
    Path("logs").mkdir(exist_ok=True)
    Path("temp_documents").mkdir(exist_ok=True)
    
    # Create .env if needed
    if not Path(".env").exists() and Path(".env.example").exists():
        Path(".env").write_text(Path(".env.example").read_text())
        print("📝 Created .env file")
    
    print("🚀 Starting application...")
    print("🌐 Open browser to: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop")
    print()
    
    # Launch Streamlit directly
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")

if __name__ == "__main__":
    main()