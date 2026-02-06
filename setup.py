"""
Setup script for Legal Contract Assistant
"""
import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def download_spacy_model():
    """Download spaCy English model"""
    print("Downloading spaCy English model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model downloaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading spaCy model: {e}")
        return False
    return True

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = ["logs", "temp_documents"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def setup_environment():
    """Setup environment file"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("Setting up environment file...")
        env_file.write_text(env_example.read_text())
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your API keys")
    elif env_file.exists():
        print("✅ Environment file already exists")
    else:
        print("⚠️  No .env.example file found")
    
    return True

def verify_installation():
    """Verify installation"""
    print("\nVerifying installation...")
    
    try:
        # Test imports
        import streamlit
        import spacy
        import pandas
        import openai
        import anthropic
        
        # Test spaCy model
        nlp = spacy.load("en_core_web_sm")
        
        print("✅ All core dependencies are working")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except OSError as e:
        print(f"❌ spaCy model error: {e}")
        print("Please run: python -m spacy download en_core_web_sm")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Legal Contract Assistant for Indian SMEs")
    print("=" * 60)
    
    steps = [
        ("Installing requirements", install_requirements),
        ("Downloading spaCy model", download_spacy_model),
        ("Creating directories", create_directories),
        ("Setting up environment", setup_environment),
        ("Verifying installation", verify_installation)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI or Anthropic API key")
    print("2. Run the application: streamlit run app.py")
    print("3. Open your browser to http://localhost:8501")
    print("\n⚠️  Remember: This system provides educational information only, not legal advice.")

if __name__ == "__main__":
    main()