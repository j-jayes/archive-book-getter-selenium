#!/usr/bin/env python3
"""
Configuration validator for Archive Book Scraper
Helps users verify their .env setup before running the scraper
"""

import os
from pathlib import Path
from dotenv import load_dotenv


def validate_config():
    """Validate the .env configuration"""
    print("=" * 70)
    print("Archive Book Scraper - Configuration Validator")
    print("=" * 70)
    print()
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ CRITICAL: .env file not found!")
        print()
        print("Please create a .env file:")
        print("  1. Copy .env.example to .env")
        print("     cp .env.example .env")
        print("  2. Edit .env with your credentials")
        print()
        return False
    
    print("✓ .env file found")
    
    # Load environment variables
    load_dotenv()
    
    # Check required variables
    print("\nChecking required variables:")
    print("-" * 70)
    
    all_valid = True
    
    # ARCHIVE_USERNAME
    username = os.getenv('ARCHIVE_USERNAME')
    if not username or username.startswith('your_'):
        print("❌ ARCHIVE_USERNAME: Not set or using placeholder")
        all_valid = False
    else:
        print(f"✓ ARCHIVE_USERNAME: {username}")
    
    # ARCHIVE_PASSWORD
    password = os.getenv('ARCHIVE_PASSWORD')
    if not password or password.startswith('your_'):
        print("❌ ARCHIVE_PASSWORD: Not set or using placeholder")
        all_valid = False
    else:
        print(f"✓ ARCHIVE_PASSWORD: {'*' * len(password)} (hidden)")
    
    # BOOK_URL
    book_url = os.getenv('BOOK_URL')
    if not book_url or book_url.startswith('https://archive.org/details/your-'):
        print("❌ BOOK_URL: Not set or using placeholder")
        all_valid = False
    elif not book_url.startswith('https://archive.org/'):
        print(f"⚠️  BOOK_URL: {book_url}")
        print("    Warning: URL should start with https://archive.org/")
    else:
        print(f"✓ BOOK_URL: {book_url}")
    
    # Optional variables
    print("\nChecking optional variables:")
    print("-" * 70)
    
    # CHROME_PROFILE_PATH
    chrome_profile = os.getenv('CHROME_PROFILE_PATH')
    if chrome_profile and not chrome_profile.startswith('/Users/YOUR_USERNAME'):
        profile_path = Path(chrome_profile)
        if profile_path.exists():
            print(f"✓ CHROME_PROFILE_PATH: {chrome_profile}")
            print("  Profile directory exists")
        else:
            print(f"⚠️  CHROME_PROFILE_PATH: {chrome_profile}")
            print("  Warning: Directory does not exist")
            print("  The scraper will work without it, but won't use saved authentication")
    else:
        print("○ CHROME_PROFILE_PATH: Not set (will work without saved authentication)")
    
    # OUTPUT_FILE
    output_file = os.getenv('OUTPUT_FILE', 'extracted_text.txt')
    print(f"✓ OUTPUT_FILE: {output_file}")
    
    # Final verdict
    print("\n" + "=" * 70)
    if all_valid:
        print("✅ Configuration is valid! You can run the scraper.")
        print()
        print("To start scraping, run:")
        print("  python scraper.py")
        print()
        print("Or try examples:")
        print("  python example_usage.py")
        return True
    else:
        print("❌ Configuration has errors. Please fix the issues above.")
        print()
        print("Edit your .env file:")
        print("  nano .env")
        print()
        return False


def show_example_env():
    """Show example .env content"""
    print("\nExample .env file content:")
    print("-" * 70)
    print("""
ARCHIVE_USERNAME=my_archive_username
ARCHIVE_PASSWORD=my_secure_password
CHROME_PROFILE_PATH=/Users/myname/Library/Application Support/Google/Chrome
BOOK_URL=https://archive.org/details/examplebook
OUTPUT_FILE=extracted_text.txt
    """.strip())
    print("-" * 70)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        show_example_env()
    else:
        success = validate_config()
        
        if not success:
            print("\nTip: Run 'python validate_config.py example' to see an example .env file")
        
        exit(0 if success else 1)
