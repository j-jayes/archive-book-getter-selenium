#!/usr/bin/env python3
"""
Internet Archive Book Scraper
Extracts text from Internet Archive books by piercing Shadow DOMs
"""

import os
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ArchiveBookScraper:
    """Scraper for extracting text from Internet Archive books"""
    
    def __init__(self):
        """Initialize the scraper with environment variables"""
        load_dotenv()
        
        self.username = os.getenv('ARCHIVE_USERNAME')
        self.password = os.getenv('ARCHIVE_PASSWORD')
        self.chrome_profile_path = os.getenv('CHROME_PROFILE_PATH')
        self.book_url = os.getenv('BOOK_URL')
        self.output_file = os.getenv('OUTPUT_FILE', 'extracted_text.txt')
        
        self.driver = None
        self.extracted_text = []
        
        # Validate required environment variables
        if not all([self.username, self.password, self.book_url]):
            raise ValueError("Missing required environment variables. Check your .env file.")
    
    def setup_driver(self):
        """Set up Chrome driver with local profile for authentication"""
        logger.info("Setting up Chrome driver with local profile...")
        
        chrome_options = Options()
        
        # Use local Chrome profile if provided
        if self.chrome_profile_path:
            logger.info(f"Using Chrome profile: {self.chrome_profile_path}")
            chrome_options.add_argument(f"user-data-dir={self.chrome_profile_path}")
            chrome_options.add_argument("--profile-directory=Default")
        
        # Additional options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Disable headless mode to use profile properly
        # chrome_options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        
        logger.info("Chrome driver setup complete")
    
    def login(self):
        """Login to Internet Archive if not already authenticated"""
        logger.info("Checking authentication status...")
        
        # Navigate to the book page
        self.driver.get(self.book_url)
        time.sleep(3)
        
        # Check if already logged in by looking for user menu
        try:
            # If we can find the login link, we're not logged in
            login_element = self.driver.find_element(By.LINK_TEXT, "Log in")
            logger.info("Not logged in, proceeding with login...")
            
            # Click login
            login_element.click()
            time.sleep(2)
            
            # Fill in credentials
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            
            # Submit form
            login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            login_button.click()
            
            time.sleep(3)
            logger.info("Login successful")
            
        except NoSuchElementException:
            logger.info("Already logged in or no login required")
    
    def pierce_shadow_dom(self, shadow_host_selector):
        """
        Recursive JavaScript function to pierce Shadow DOM
        
        Args:
            shadow_host_selector: CSS selector for the shadow host element
            
        Returns:
            Shadow root element or None
        """
        js_script = """
        function getShadowRoot(selector) {
            const element = document.querySelector(selector);
            if (element && element.shadowRoot) {
                return element.shadowRoot;
            }
            return null;
        }
        return getShadowRoot(arguments[0]);
        """
        
        return self.driver.execute_script(js_script, shadow_host_selector)
    
    def extract_text_from_shadow_dom(self):
        """
        Extract text from .BRwordElement nodes within Shadow DOM
        Recursively pierces through ia-book-theater shadow structure
        """
        logger.info("Extracting text from Shadow DOM...")
        
        # JavaScript to recursively extract text from shadow DOM
        js_extract_text = """
        function extractTextFromShadowDOM(root) {
            let allText = [];
            
            // Recursive function to traverse shadow DOMs
            function traverse(element) {
                // Check if element has shadow root
                if (element.shadowRoot) {
                    traverse(element.shadowRoot);
                }
                
                // If it's a document fragment or shadow root
                if (element instanceof DocumentFragment || element instanceof ShadowRoot) {
                    // Look for .BRwordElement nodes
                    const wordElements = element.querySelectorAll('.BRwordElement');
                    wordElements.forEach(wordEl => {
                        const text = wordEl.textContent || wordEl.innerText;
                        if (text && text.trim()) {
                            allText.push(text.trim());
                        }
                    });
                    
                    // Traverse children
                    const children = element.querySelectorAll('*');
                    children.forEach(child => traverse(child));
                }
                
                // If it's a regular element
                if (element instanceof Element) {
                    // Check for .BRwordElement class
                    if (element.classList && element.classList.contains('BRwordElement')) {
                        const text = element.textContent || element.innerText;
                        if (text && text.trim()) {
                            allText.push(text.trim());
                        }
                    }
                    
                    // Check if element has shadow root
                    if (element.shadowRoot) {
                        traverse(element.shadowRoot);
                    }
                    
                    // Traverse children
                    Array.from(element.children).forEach(child => traverse(child));
                }
            }
            
            // Start traversal from root
            traverse(root);
            
            return allText;
        }
        
        // Find ia-book-theater element
        const bookTheater = document.querySelector('ia-book-theater');
        if (bookTheater) {
            return extractTextFromShadowDOM(bookTheater);
        }
        
        // Fallback: try to extract from entire document
        return extractTextFromShadowDOM(document.body);
        """
        
        try:
            text_array = self.driver.execute_script(js_extract_text)
            if text_array and len(text_array) > 0:
                logger.info(f"Extracted {len(text_array)} text elements from current page")
                return text_array
            else:
                logger.warning("No text elements found on current page")
                return []
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return []
    
    def find_next_button_in_shadow(self):
        """
        Find and click the next page button within shadow DOM
        
        Returns:
            True if next button found and clicked, False otherwise
        """
        logger.info("Looking for next page button in Shadow DOM...")
        
        # JavaScript to find and click next button in shadow DOM
        js_find_next = """
        function findAndClickNext(root) {
            // Recursive function to find next button
            function findButton(element) {
                // Check if element has shadow root
                if (element.shadowRoot) {
                    const button = findButton(element.shadowRoot);
                    if (button) return button;
                }
                
                // If it's a document fragment or shadow root
                if (element instanceof DocumentFragment || element instanceof ShadowRoot) {
                    // Look for next button with various selectors
                    const selectors = [
                        'button.BRicon.next',
                        'button[title*="next" i]',
                        'button[aria-label*="next" i]',
                        '.BRnext',
                        '[class*="next"]',
                        'button:has(.icon-next)',
                        'button.flip-right'
                    ];
                    
                    for (let selector of selectors) {
                        try {
                            const button = element.querySelector(selector);
                            if (button && !button.disabled) {
                                return button;
                            }
                        } catch (e) {
                            // Selector might not be valid in this context
                        }
                    }
                    
                    // Traverse children
                    const children = element.querySelectorAll('*');
                    for (let child of children) {
                        const button = findButton(child);
                        if (button) return button;
                    }
                }
                
                return null;
            }
            
            // Start search
            const button = findButton(root);
            if (button) {
                button.click();
                return true;
            }
            return false;
        }
        
        // Find ia-book-theater and search for next button
        const bookTheater = document.querySelector('ia-book-theater');
        if (bookTheater) {
            return findAndClickNext(bookTheater);
        }
        
        // Fallback: search entire document
        return findAndClickNext(document.body);
        """
        
        try:
            result = self.driver.execute_script(js_find_next)
            if result:
                logger.info("Next button clicked successfully")
                time.sleep(2)  # Wait for page to load
                return True
            else:
                logger.info("Next button not found - might be on last page")
                return False
        except Exception as e:
            logger.error(f"Error finding next button: {e}")
            return False
    
    def scrape_book(self, max_pages=None):
        """
        Main scraping function - iterates through pages and extracts text
        
        Args:
            max_pages: Maximum number of pages to scrape (None for all pages)
        """
        logger.info(f"Starting book scraping from {self.book_url}")
        
        # Setup driver and login
        self.setup_driver()
        self.login()
        
        # Navigate to book reader
        self.driver.get(self.book_url)
        time.sleep(5)  # Wait for book reader to load
        
        page_count = 0
        
        while True:
            # Check if we've reached max pages
            if max_pages and page_count >= max_pages:
                logger.info(f"Reached maximum page limit: {max_pages}")
                break
            
            page_count += 1
            logger.info(f"Processing page {page_count}...")
            
            # Extract text from current page
            page_text = self.extract_text_from_shadow_dom()
            if page_text:
                self.extracted_text.extend(page_text)
            
            # Try to go to next page
            if not self.find_next_button_in_shadow():
                logger.info("No more pages to process")
                break
            
            # Small delay between pages
            time.sleep(1)
        
        logger.info(f"Scraping complete. Processed {page_count} pages")
        logger.info(f"Total text elements extracted: {len(self.extracted_text)}")
    
    def save_to_file(self):
        """Save extracted text to output file"""
        logger.info(f"Saving extracted text to {self.output_file}...")
        
        # Create output directory if it doesn't exist
        output_path = Path(self.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            # Write each text element on a new line
            for text in self.extracted_text:
                f.write(text + '\n')
        
        logger.info(f"Text saved successfully to {self.output_file}")
        logger.info(f"Total words written: {sum(len(text.split()) for text in self.extracted_text)}")
    
    def cleanup(self):
        """Close browser and cleanup resources"""
        if self.driver:
            logger.info("Closing browser...")
            self.driver.quit()
            logger.info("Cleanup complete")
    
    def run(self, max_pages=None):
        """
        Main entry point to run the scraper
        
        Args:
            max_pages: Maximum number of pages to scrape (None for all pages)
        """
        try:
            self.scrape_book(max_pages=max_pages)
            self.save_to_file()
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            raise
        finally:
            self.cleanup()


def main():
    """Main function"""
    # Create scraper instance
    scraper = ArchiveBookScraper()
    
    # Run scraper (set max_pages to limit, or None for all pages)
    # Example: scraper.run(max_pages=10)  # Scrape only first 10 pages
    scraper.run(max_pages=None)  # Scrape all pages


if __name__ == "__main__":
    main()
