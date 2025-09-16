"""
RBI Chatbot Deployment Script
Simple script to launch the Streamlit application with proper configuration
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required files exist"""
    required_files = [
        "rbi_chatbot_streamlit.py",
        "chroma_db",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        print("📋 Setup checklist:")
        print("1. Run the chatbot.ipynb notebook to create vector database")
        print("2. Ensure requirements.txt is in the same directory")
        print("3. Run this script from the Chatbot directory")
        return False
    
    print("✅ All required files found")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def launch_streamlit():
    """Launch the Streamlit application"""
    print("🚀 Launching RBI Chatbot...")
    print("📱 The application will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("⭐ Press Ctrl+C to stop the application")
    
    try:
        subprocess.run([
            "streamlit", "run", "rbi_chatbot_streamlit.py",
            "--server.port", "8501",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")

def main():
    print("🏦 RBI Guidelines Chatbot - Deployment Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("rbi_chatbot_streamlit.py").exists():
        print("❌ Please run this script from the Chatbot directory")
        print("📁 Current directory:", os.getcwd())
        return
    
    # Check requirements
    if not check_requirements():
        return
    
    # Ask user if they want to install requirements
    install_deps = input("\n📦 Install/update requirements? (y/N): ").strip().lower()
    if install_deps in ['y', 'yes']:
        if not install_requirements():
            return
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n💡 Optional: Set OPENAI_API_KEY environment variable for better responses")
        print("   Without it, the system will use Ollama (if available) or demo mode")
    
    # Launch application
    print("\n" + "=" * 50)
    launch_streamlit()

if __name__ == "__main__":
    main()
