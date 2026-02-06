#!/usr/bin/env python3
"""
Simple launcher for Legal Contract Assistant
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Legal Contract Assistant"""
    
    print("⚖️  Legal Contract Assistant for Indian SMEs")
    print("=" * 50)
    print("🚀 Starting the application...")
    print()
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Error: app.py not found in current directory")
        print("Please run this script from the project root directory")
        return 1
    
    # Check if Streamlit is available
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} found")
    except ImportError:
        print("❌ Streamlit not found. Please install requirements:")
        print("   pip install -r requirements.txt")
        return 1
    
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    Path("temp_documents").mkdir(exist_ok=True)
    
    # Set up environment
    if not Path(".env").exists() and Path(".env.example").exists():
        print("📝 Creating .env file from template...")
        Path(".env").write_text(Path(".env.example").read_text())
        print("⚠️  Please edit .env file and add your API keys for full functionality")
    
    print("🌐 Launching web application...")
    print("📱 Open your browser to: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop")
    print()
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
        return 0
    except Exception as e:
        print(f"\n❌ Error launching application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())