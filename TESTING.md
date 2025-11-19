# Testing Guide

This document explains how to test the Archive Book Scraper before using it on real books.

## Pre-Flight Checklist

Before running the scraper, verify your setup:

```bash
# 1. Check if all dependencies are installed
pip list | grep -E "selenium|python-dotenv|webdriver-manager"

# 2. Validate your configuration
python validate_config.py

# 3. Test connection to Internet Archive
python utils.py test

# 4. View Chrome profile help (if needed)
python utils.py profile
```

## Running the Test Suite

### 1. Shadow DOM Extraction Test

This test validates that the JavaScript Shadow DOM piercing logic works correctly:

```bash
# Run the extraction test
python test_extraction.py
```

**What it tests:**
- Recursive Shadow DOM traversal
- Text extraction from .BRwordElement nodes
- Next button finding in shadow-nested structures

**Expected output:**
```
Testing Shadow DOM extraction logic...

Test Results
Total text elements extracted: 11
...
✅ Shadow DOM extraction logic verified successfully!
```

### 2. Configuration Validation Test

```bash
# Without .env file (should fail)
python validate_config.py

# After creating .env
cp .env.example .env
# Edit .env with your credentials
python validate_config.py

# Show example configuration
python validate_config.py example
```

**Expected output (when valid):**
```
✓ .env file found
✓ ARCHIVE_USERNAME: your_username
✓ ARCHIVE_PASSWORD: ******
✓ BOOK_URL: https://archive.org/details/...
✅ Configuration is valid! You can run the scraper.
```

### 3. Import Test

Verify all Python modules import correctly:

```bash
python -c "from scraper import ArchiveBookScraper; print('✓ Scraper imports')"
python -c "import utils; print('✓ Utils imports')"
python -c "import example_usage; print('✓ Examples import')"
python -c "import validate_config; print('✓ Validator imports')"
```

### 4. Selenium WebDriver Test

Test that ChromeDriver is working:

```bash
python utils.py test
```

**Expected output:**
```
Testing connection to Internet Archive...
✅ Successfully connected to Internet Archive
   Page title: Internet Archive: Digital Library...
```

## Manual Testing

### Test with Limited Pages

For your first run, test with a small number of pages:

1. Edit `scraper.py` and change the last line:
```python
# Change from:
scraper.run(max_pages=None)

# To:
scraper.run(max_pages=3)  # Test with just 3 pages
```

2. Run the scraper:
```bash
python scraper.py
```

3. Check the output:
```bash
# View extracted text
head -50 extracted_text.txt

# Count lines
wc -l extracted_text.txt

# Search for specific words
grep -i "chapter" extracted_text.txt
```

### Test with Example Scripts

Try the example scripts:

```bash
# Interactive menu
python example_usage.py

# Specific examples
python example_usage.py 1  # Basic usage
python example_usage.py 2  # Limited to 5 pages
python example_usage.py 3  # Custom workflow
```

## Troubleshooting Tests

### ChromeDriver Issues

If you get ChromeDriver errors:

```bash
# Check Chrome version
google-chrome --version  # Linux
# or
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version  # Mac

# Update ChromeDriver
pip install --upgrade webdriver-manager

# Test manually
python -c "from selenium import webdriver; driver = webdriver.Chrome(); driver.quit(); print('OK')"
```

### Import Errors

If you get import errors:

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version (needs 3.8+)
python --version
```

### Configuration Errors

If validation fails:

```bash
# Check .env file exists
ls -la .env

# View example format
python validate_config.py example

# Check file permissions
chmod 600 .env  # Secure permissions
```

## Test with Different Books

Test the scraper with various Internet Archive books:

### 1. Public Domain Book (No Login Required)

```env
BOOK_URL=https://archive.org/details/adventuresofhuck00twaiiala
```

### 2. Borrowed Book (Login Required)

```env
BOOK_URL=https://archive.org/details/[your-borrowed-book]
```

Make sure you're logged in and have the book borrowed.

### 3. Different Text Structures

Some books may use different class names. If extraction fails:

1. Open the book in Chrome
2. Open DevTools (F12)
3. Inspect the page structure
4. Look for Shadow DOM elements
5. Find the actual class names used for text
6. Modify the scraper accordingly

## Performance Testing

### Measure Extraction Speed

```bash
# Time the scraper
time python scraper.py

# Check memory usage
/usr/bin/time -v python scraper.py  # Linux
```

### Test Large Books

For books with many pages:

1. Start with `max_pages=10`
2. Check output and performance
3. Gradually increase if working well
4. Monitor memory usage

## Validation Checklist

Before considering the scraper production-ready:

- [ ] Configuration validation passes
- [ ] Shadow DOM test passes
- [ ] Connection test succeeds
- [ ] Successfully extracts text from test pages (3-5 pages)
- [ ] Pagination works (advances through pages)
- [ ] Output file is created and contains text
- [ ] No errors in console output
- [ ] Chrome profile authentication works (if used)
- [ ] Can extract from at least one complete book

## Continuous Testing

After making any modifications:

```bash
# Quick validation
python -m py_compile scraper.py  # Syntax check
python validate_config.py        # Config check
python test_extraction.py        # Logic check

# Full test
python scraper.py  # Run with max_pages=3
```

## Test Output Verification

Verify the extracted text is correct:

```bash
# 1. Check file was created
ls -lh extracted_text.txt

# 2. View first lines
head -20 extracted_text.txt

# 3. View last lines
tail -20 extracted_text.txt

# 4. Count unique words
cat extracted_text.txt | tr ' ' '\n' | sort -u | wc -l

# 5. Check for common words
grep -c "the" extracted_text.txt
grep -c "and" extracted_text.txt

# 6. Look for chapter markers
grep -i "chapter" extracted_text.txt

# 7. Search for specific content
grep -i "keyword" extracted_text.txt
```

## Automated Testing

For future enhancement, consider adding:

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test full workflow with mock data
3. **Regression Tests**: Ensure changes don't break existing functionality
4. **Performance Tests**: Benchmark extraction speed

## Reporting Issues

If tests fail, collect this information:

```bash
# System information
python --version
pip list | grep -E "selenium|dotenv|webdriver"

# Chrome version
google-chrome --version  # or equivalent for Mac

# Test results
python validate_config.py > test_results.txt
python test_extraction.py >> test_results.txt
python utils.py test >> test_results.txt

# Error logs (if scraper fails)
python scraper.py 2>&1 | tee scraper_error.log
```

## Success Criteria

The scraper is working correctly if:

1. All validation checks pass ✓
2. Text is extracted from test pages ✓
3. Pagination advances through pages ✓
4. Output file contains readable text ✓
5. No critical errors in logs ✓
6. Chrome profile authentication works (if used) ✓

Once all criteria are met, you can confidently use the scraper for full book extraction!
