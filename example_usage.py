#!/usr/bin/env python3
"""
Example usage script for the Archive Book Scraper

This script demonstrates different ways to use the scraper.
"""

from scraper import ArchiveBookScraper
import logging

# Configure logging level
logging.basicConfig(level=logging.INFO)

def example_basic_usage():
    """Example: Basic usage - scrape all pages"""
    print("=" * 60)
    print("Example 1: Basic Usage - Scrape All Pages")
    print("=" * 60)
    
    scraper = ArchiveBookScraper()
    scraper.run(max_pages=None)  # Scrape all pages


def example_limited_pages():
    """Example: Scrape only first 5 pages"""
    print("=" * 60)
    print("Example 2: Limited Scraping - First 5 Pages")
    print("=" * 60)
    
    scraper = ArchiveBookScraper()
    scraper.run(max_pages=5)  # Scrape only first 5 pages


def example_custom_workflow():
    """Example: Custom workflow with manual control"""
    print("=" * 60)
    print("Example 3: Custom Workflow")
    print("=" * 60)
    
    scraper = ArchiveBookScraper()
    
    try:
        # Manual control over each step
        scraper.setup_driver()
        scraper.login()
        
        # Navigate to book
        scraper.driver.get(scraper.book_url)
        import time
        time.sleep(5)
        
        # Process just 3 pages manually
        for page_num in range(3):
            print(f"Processing page {page_num + 1}...")
            
            # Extract text
            page_text = scraper.extract_text_from_shadow_dom()
            if page_text:
                scraper.extracted_text.extend(page_text)
                print(f"  - Extracted {len(page_text)} text elements")
            
            # Go to next page
            if page_num < 2:  # Don't click next on last iteration
                if not scraper.find_next_button_in_shadow():
                    print("No more pages available")
                    break
            
            time.sleep(1)
        
        # Save results
        scraper.save_to_file()
        
    finally:
        scraper.cleanup()


if __name__ == "__main__":
    import sys
    
    print("\nArchive Book Scraper - Examples\n")
    print("Available examples:")
    print("1. Basic usage - scrape all pages")
    print("2. Limited scraping - first 5 pages")
    print("3. Custom workflow - manual control")
    print()
    
    # Choose which example to run
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("Enter example number (1-3) or press Enter for default (1): ").strip()
        if not choice:
            choice = "1"
    
    examples = {
        "1": example_basic_usage,
        "2": example_limited_pages,
        "3": example_custom_workflow
    }
    
    if choice in examples:
        examples[choice]()
    else:
        print(f"Invalid choice: {choice}")
        print("Using default example (1)")
        example_basic_usage()
