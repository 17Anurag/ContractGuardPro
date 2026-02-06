"""
Run script for Legal Contract Assistant
Handles startup checks and launches the Streamlit app
"""
import os
import sys
import subprocess
from pathlib import Path
import logging

def check_environment():
    """Check if environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("⚠️  .env file not found. Creating from template...")
        if Path(".env.example").exists():
            Path(".env").write_text(Path(".env.example").read_text())
            print("✅ Created .env file. Please add your API keys.")
        else:
            print("❌ No .env.example file found")
            return False
    
    # Check required directories
    required_dirs = ["logs", "temp_documents"]
    for directory in required_dirs:
        Path(directory).mkdir(exist_ok=True)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print("✅ Environment check passed")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        "streamlit",
        "spacy", 
        "pandas",
        "openai",
        "anthropic",
        "PyPDF2",
        "python-docx",
        "pdfplumber"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    # Check spaCy model
    try:
        import spacy
        spacy.load("en_core_web_sm")
    except OSError:
        print("❌ spaCy English model not found")
        print("Run: python -m spacy download en_core_web_sm")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_api_keys():
    """Check if API keys are configured"""
    print("🔑 Checking API configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_key and not anthropic_key:
        print("⚠️  No API keys found in .env file")
        print("The system will work with limited functionality")
        print("Add OPENAI_API_KEY or ANTHROPIC_API_KEY to .env for full features")
        return True  # Not blocking, just limited functionality
    
    if openai_key:
        print("✅ OpenAI API key found")
    if anthropic_key:
        print("✅ Anthropic API key found")
    
    return True

def launch_app():
    """Launch the Streamlit application"""
    print("🚀 Launching Legal Contract Assistant...")
    
    try:
        # Set Streamlit configuration
        os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
        os.environ["STREAMLIT_SERVER_PORT"] = "8501"
        
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        return False
    
    return True

def show_startup_info():
    """Show startup information"""
    print("⚖️  Legal Contract Assistant for Indian SMEs")
    print("=" * 50)
    print("📋 Features:")
    print("  • Contract analysis and risk assessment")
    print("  • Plain-language explanations")
    print("  • SME-friendly contract templates")
    print("  • Business impact analysis")
    print("")
    print("⚠️  IMPORTANT DISCLAIMER:")
    print("  This system provides educational information only.")
    print("  It is NOT a lawyer and does NOT provide legal advice.")
    print("  Always consult qualified legal professionals.")
    print("=" * 50)
    print("")

def main():
    """Main run function"""
    show_startup_info()
    
    # Run startup checks
    checks = [
        ("Environment", check_environment),
        ("Dependencies", check_dependencies), 
        ("API Keys", check_api_keys)
    ]
    
    for check_name, check_func in checks:
        if not check_func():
            print(f"\n❌ Startup failed: {check_name} check failed")
            print("\nTroubleshooting:")
            print("1. Run setup.py to install dependencies")
            print("2. Check .env file for API keys")
            print("3. Ensure Python 3.8+ is installed")
            sys.exit(1)
    
    print("\n✅ All checks passed!")
    print("🌐 Starting web application...")
    print("📱 Open your browser to: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    print("")
    
    # Launch the application
    launch_app()

if __name__ == "__main__":
    main()