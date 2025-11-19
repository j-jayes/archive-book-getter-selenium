#!/usr/bin/env python3
"""
Utility script for Archive Book Scraper
Provides helpful commands for setup and testing
"""

import os
import sys
from pathlib import Path


def check_environment():
    """Check if environment is properly configured"""
    print("Checking environment configuration...\n")
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("   Please create .env file from .env.example:")
        print("   cp .env.example .env")
        return False
    else:
        print("✓ .env file found")
    
    # Check if required packages are installed
    try:
        import selenium
        print(f"✓ Selenium installed (version {selenium.__version__})")
    except ImportError:
        print("❌ Selenium not installed")
        print("   Please run: pip install -r requirements.txt")
        return False
    
    try:
        import dotenv
        print("✓ python-dotenv installed")
    except ImportError:
        print("❌ python-dotenv not installed")
        print("   Please run: pip install -r requirements.txt")
        return False
    
    # Check Chrome/ChromeDriver
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
        driver.quit()
        print("✓ ChromeDriver working")
    except Exception as e:
        print(f"❌ ChromeDriver issue: {e}")
        return False
    
    # Check .env variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['ARCHIVE_USERNAME', 'ARCHIVE_PASSWORD', 'BOOK_URL']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing or incomplete environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n   Please update your .env file with real values")
        return False
    else:
        print("✓ All required environment variables set")
    
    print("\n✅ Environment is ready!")
    return True


def show_chrome_profile_help():
    """Show help for finding Chrome profile path"""
    print("\nHow to find your Chrome profile path:\n")
    print("1. Open Google Chrome")
    print("2. Navigate to: chrome://version/")
    print("3. Look for 'Profile Path'")
    print("4. Copy the path up to (but not including) the profile name")
    print("\nExample on Mac:")
    print("  /Users/YourUsername/Library/Application Support/Google/Chrome")
    print("\nExample on Linux:")
    print("  /home/username/.config/google-chrome")
    print("\nExample on Windows:")
    print("  C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data")


def test_connection():
    """Test connection to Internet Archive"""
    print("Testing connection to Internet Archive...\n")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import time
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        
        driver = webdriver.Chrome(options=options)
        driver.get("https://archive.org")
        
        time.sleep(2)
        
        if "Internet Archive" in driver.title:
            print("✅ Successfully connected to Internet Archive")
            print(f"   Page title: {driver.title}")
        else:
            print("⚠️  Connected but unexpected page content")
        
        driver.quit()
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")


def show_usage():
    """Show usage information"""
    print("\nArchive Book Scraper - Utility Script\n")
    print("Usage: python utils.py [command]\n")
    print("Commands:")
    print("  check       - Check if environment is properly configured")
    print("  profile     - Show help for finding Chrome profile path")
    print("  test        - Test connection to Internet Archive")
    print("  help        - Show this help message")
    print("\nExamples:")
    print("  python utils.py check")
    print("  python utils.py profile")
    print("  python utils.py test")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        show_usage()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'check': check_environment,
        'profile': show_chrome_profile_help,
        'test': test_connection,
        'help': show_usage
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        show_usage()


if __name__ == "__main__":
    main()
