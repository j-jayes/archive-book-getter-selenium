#!/usr/bin/env python3
"""
Test script to verify Shadow DOM extraction logic
Uses the test HTML file with Selenium
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path


def test_shadow_dom_extraction():
    """Test the Shadow DOM extraction on test HTML file"""
    print("Testing Shadow DOM extraction logic...\n")
    
    # Setup Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Load test HTML file
        test_file = Path(__file__).parent / "test_shadow_dom.html"
        driver.get(f"file://{test_file.absolute()}")
        
        # Wait for page to load
        time.sleep(2)
        
        # Get test results from the page
        results_element = driver.find_element_by_id("test-results")
        results_text = results_element.text
        
        print(results_text)
        print("\n" + "="*60)
        
        # Check if tests passed
        if "✓ All tests passed!" in results_text:
            print("\n✅ Shadow DOM extraction logic verified successfully!")
            return True
        else:
            print("\n⚠️  Tests did not pass as expected")
            return False
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False
        
    finally:
        driver.quit()


if __name__ == "__main__":
    success = test_shadow_dom_extraction()
    exit(0 if success else 1)
