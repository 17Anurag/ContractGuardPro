"""
Test script to check Gemini API functionality
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Google Gemini API connection"""
    print("🔍 Testing Google Gemini API connection...")
    
    # Set API key directly for testing
    api_key = "AIzaSyAonMi7V7RrPxcEeUMY4nDoYVmrFvtVFe8"
    
    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ No Gemini API key found")
        print("💡 Get a free API key from: https://makersuite.google.com/app/apikey")
        return False
    
    print(f"✅ API key found: {api_key[:20]}...")
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI library imported successfully")
        
        # Configure API
        genai.configure(api_key=api_key)
        print("✅ Gemini API configured")
        
        # Initialize model with correct model name
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Gemini Flash model initialized")
        
        # Test API call
        print("🧪 Testing API call...")
        response = model.generate_content("Hello, this is a test. Please respond with 'Gemini API working'.")
        
        result = response.text
        print(f"✅ API Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        if "quota" in str(e).lower():
            print("💡 Quota exceeded. Try again in a few minutes or use a different model.")
        elif "API_KEY_INVALID" in str(e):
            print("💡 Your API key appears to be invalid. Please check it at: https://makersuite.google.com/app/apikey")
        return False

def install_gemini():
    """Install Google Generative AI library"""
    print("📦 Installing Google Generative AI library...")
    try:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
        print("✅ Google Generative AI library installed successfully")
        return True
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Gemini API Testing Tool")
    print("=" * 40)
    
    # Check if library is installed
    try:
        import google.generativeai as genai
    except ImportError:
        print("📦 Google Generative AI library not found. Installing...")
        if not install_gemini():
            print("❌ Failed to install required library")
            return
        print("✅ Library installed. Please restart and try again.")
        return
    
    # Test Gemini API
    gemini_works = test_gemini_api()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"Gemini API: {'✅ Working' if gemini_works else '❌ Failed'}")
    
    if gemini_works:
        print("\n🎉 Gemini API is working! Your ContractGuard now has AI explanations.")
        print("💡 Restart your app to use the AI features.")
    else:
        print("\n⚠️  Gemini API is not working. Follow these steps:")
        print("1. Go to: https://makersuite.google.com/app/apikey")
        print("2. Sign in with your Google account")
        print("3. Click 'Create API Key'")
        print("4. Copy the key and add it to your .env file:")
        print("   GEMINI_API_KEY=your_actual_key_here")
        print("5. Restart the application")
        print("\n🆓 Gemini API is FREE with generous limits!")

if __name__ == "__main__":
    main()