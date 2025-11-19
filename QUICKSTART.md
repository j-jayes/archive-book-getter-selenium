# Quick Start Guide

This guide will help you get started with the Archive Book Scraper in just a few minutes.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your information:
```bash
# Use your favorite text editor
nano .env
# or
vim .env
# or
open -e .env  # Mac TextEdit
```

3. Fill in these required values:
   - `ARCHIVE_USERNAME`: Your Internet Archive username
   - `ARCHIVE_PASSWORD`: Your Internet Archive password
   - `BOOK_URL`: The full URL of the book you want to scrape
   - `CHROME_PROFILE_PATH`: (Optional) Path to your Chrome profile

### Finding Your Chrome Profile Path

Open Chrome and go to: `chrome://version/`

Look for "Profile Path" and copy the directory up to (but not including) "Default" or your profile name.

**Mac Example:**
```
/Users/YourName/Library/Application Support/Google/Chrome
```

## Step 3: Verify Setup

Run the utility script to check your configuration:

```bash
python utils.py check
```

If everything is configured correctly, you'll see checkmarks (✓) for each item.

## Step 4: Run the Scraper

### Basic Usage (All Pages)

```bash
python scraper.py
```

This will:
1. Open Chrome with your profile
2. Log in to Internet Archive (if needed)
3. Navigate to your book
4. Extract text from all pages
5. Save to `extracted_text.txt`

### Limited Pages (Testing)

Edit `scraper.py` and change the last line:

```python
# Change this:
scraper.run(max_pages=None)

# To this (for 5 pages):
scraper.run(max_pages=5)
```

### Using Examples

Try the example scripts:

```bash
# Interactive examples
python example_usage.py

# Specific example
python example_usage.py 1  # Basic usage
python example_usage.py 2  # First 5 pages
python example_usage.py 3  # Custom workflow
```

## Step 5: Check Output

After scraping completes, check your output file:

```bash
# View first 20 lines
head -20 extracted_text.txt

# Count total lines
wc -l extracted_text.txt

# Search for specific text
grep "keyword" extracted_text.txt
```

## Troubleshooting

### "Missing required environment variables"
- Check that your `.env` file exists and has all required values
- Make sure you replaced the placeholder values (e.g., `your_username_here`)

### Chrome profile issues
- Close Chrome completely before running the scraper
- Try without `CHROME_PROFILE_PATH` first (leave it blank or commented)
- Verify the path using `chrome://version/`

### No text extracted
- Check that the book URL is correct
- Try a different book to test
- Make sure you have access to the book (some require login)

### Script hangs or takes too long
- Some books have many pages - be patient
- Use `max_pages` to limit the number of pages for testing
- Check your internet connection

## Tips

1. **Test First**: Always test with `max_pages=5` before scraping entire books
2. **Monitor Progress**: The scraper logs its progress - watch the console output
3. **Check Output Early**: After a few pages, check `extracted_text.txt` to verify text is being extracted correctly
4. **Internet Connection**: Ensure stable internet connection for best results
5. **Book Access**: Make sure you're logged in and have access to the book

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore `example_usage.py` for advanced usage patterns
- Modify `scraper.py` to customize behavior for your needs

## Support

If you encounter issues:
1. Run `python utils.py check` to verify your setup
2. Check the console output for error messages
3. Review the troubleshooting section above
4. Consult the main README.md for more details
