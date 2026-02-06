"""
Test script to check API key functionality
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_api():
    """Test OpenAI API connection"""
    print("🔍 Testing OpenAI API connection...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No OpenAI API key found in .env file")
        return False
    
    print(f"✅ API key found: {api_key[:20]}...")
    
    try:
        import openai
        print("✅ OpenAI library imported successfully")
        
        # Initialize client
        try:
            client = openai.OpenAI(api_key=api_key)
        except TypeError:
            # Fallback for version compatibility
            openai.api_key = api_key
            client = openai
        print("✅ OpenAI client initialized")
        
        # Test API call
        print("🧪 Testing API call...")
        if hasattr(client, 'chat'):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, this is a test. Please respond with 'API working'."}],
                max_tokens=10
            )
            result = response.choices[0].message.content
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, this is a test. Please respond with 'API working'."}],
                max_tokens=10
            )
            result = response.choices[0].message.content
        print(f"✅ API Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        return False

def test_anthropic_api():
    """Test Anthropic API connection"""
    print("\n🔍 Testing Anthropic API connection...")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_anthropic_api_key_here":
        print("❌ No valid Anthropic API key found")
        return False
    
    print(f"✅ API key found: {api_key[:20]}...")
    
    try:
        import anthropic
        print("✅ Anthropic library imported successfully")
        
        # Initialize client
        client = anthropic.Anthropic(api_key=api_key)
        print("✅ Anthropic client initialized")
        
        # Test API call
        print("🧪 Testing API call...")
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hello, this is a test. Please respond with 'API working'."}]
        )
        
        result = response.content[0].text
        print(f"✅ API Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 API Key Testing Tool")
    print("=" * 40)
    
    # Test OpenAI
    openai_works = test_openai_api()
    
    # Test Anthropic
    anthropic_works = test_anthropic_api()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"OpenAI API: {'✅ Working' if openai_works else '❌ Failed'}")
    print(f"Anthropic API: {'✅ Working' if anthropic_works else '❌ Failed'}")
    
    if openai_works or anthropic_works:
        print("\n🎉 At least one API is working! Restart your app to use AI features.")
    else:
        print("\n⚠️  No APIs are working. Check your API keys and try again.")
        print("\nTroubleshooting tips:")
        print("1. Verify your API key is correct")
        print("2. Check if you have credits/quota remaining")
        print("3. Ensure your API key has the right permissions")
        print("4. Try using gpt-3.5-turbo instead of gpt-4 (cheaper)")

if __name__ == "__main__":
    main()