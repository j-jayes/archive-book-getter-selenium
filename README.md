# Archive Book Getter - Selenium Scraper

A smart Selenium-based scraper for extracting text from Internet Archive books. This tool uses local Chrome profiles for authentication and employs advanced JavaScript techniques to pierce Shadow DOMs and extract hidden text content.

## Features

- 🔐 **Local Chrome Profile Authentication**: Uses your existing Chrome profile to maintain logged-in sessions
- 🎯 **Shadow DOM Piercing**: Recursively traverses and extracts content from shadow-nested elements
- 📖 **Text Extraction**: Extracts text from `.BRwordElement` nodes within `<ia-book-theater>` 
- 📄 **Pagination Handling**: Automatically navigates through book pages using shadow-nested buttons
- 💾 **Text Accumulation**: Saves all extracted text to a cumulative output file
- 🛡️ **Error Handling**: Robust error handling and logging throughout the scraping process

## Prerequisites

- Python 3.8+
- Google Chrome browser
- ChromeDriver (automatically managed by webdriver-manager)
- Internet Archive account

## Installation

1. Clone this repository:
```bash
git clone https://github.com/j-jayes/archive-book-getter-selenium.git
cd archive-book-getter-selenium
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Edit `.env` with your credentials and settings:
```env
ARCHIVE_USERNAME=your_archive_org_username
ARCHIVE_PASSWORD=your_archive_org_password
CHROME_PROFILE_PATH=/Users/YOUR_USERNAME/Library/Application Support/Google/Chrome
BOOK_URL=https://archive.org/details/your-book-identifier
OUTPUT_FILE=extracted_text.txt
```

### Finding Your Chrome Profile Path on Mac

To find your Chrome profile path:

1. Open Chrome and navigate to `chrome://version/`
2. Look for the "Profile Path" field
3. Copy the path up to (but not including) the profile name
4. The default path on Mac is usually: `/Users/YOUR_USERNAME/Library/Application Support/Google/Chrome`

## Usage

### Basic Usage

Run the scraper to extract all pages:

```bash
python scraper.py
```

### Advanced Usage

Edit `scraper.py` to customize the behavior:

```python
# Limit to first 10 pages
scraper.run(max_pages=10)

# Scrape all pages (default)
scraper.run(max_pages=None)
```

## How It Works

### 1. Chrome Profile Loading
The scraper uses your local Chrome profile to maintain authentication sessions with Internet Archive, avoiding the need to log in repeatedly.

### 2. Shadow DOM Piercing
Internet Archive's book reader uses Shadow DOM to encapsulate its components. The scraper:
- Locates the `<ia-book-theater>` element
- Recursively traverses all shadow roots
- Identifies `.BRwordElement` nodes containing text
- Extracts and accumulates the text content

### 3. Pagination
The scraper automatically:
- Searches for "next page" buttons within shadow-nested elements
- Clicks the button to advance
- Continues until no more pages are available

### 4. Text Extraction & Storage
All extracted text is:
- Accumulated in memory during the scraping process
- Written to the specified output file
- Saved with one text element per line for easy processing

## Output

The scraper generates a text file (default: `extracted_text.txt`) containing all extracted text from the book. Each text element is written on a separate line.

Example output structure:
```
word1
word2
word3
...
```

## Configuration Options

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ARCHIVE_USERNAME` | Internet Archive username | Yes | - |
| `ARCHIVE_PASSWORD` | Internet Archive password | Yes | - |
| `CHROME_PROFILE_PATH` | Path to Chrome profile directory | No | - |
| `BOOK_URL` | Full URL to the book on archive.org | Yes | - |
| `OUTPUT_FILE` | Path to save extracted text | No | `extracted_text.txt` |

## Troubleshooting

### Chrome Profile Issues
- Ensure Chrome is closed before running the scraper with profile loading
- Verify the profile path is correct using `chrome://version/`
- Try without profile path first to test basic functionality

### No Text Extracted
- Verify the book URL is correct and accessible
- Check that you're logged in (some books require authentication)
- Try increasing wait times in the script

### Pagination Not Working
- Some books use different pagination structures
- Check browser console for JavaScript errors
- Manually inspect the Shadow DOM structure

## Logging

The scraper provides detailed logging output:
- `INFO`: Normal operation messages
- `WARNING`: Non-critical issues (e.g., no text found on a page)
- `ERROR`: Critical errors that stop execution

## Security Notes

- The `.env` file containing credentials is automatically excluded from version control
- Never commit your `.env` file to a repository
- Use secure storage for your credentials

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for any purpose.

## Disclaimer

This tool is for personal use and educational purposes. Ensure you comply with Internet Archive's Terms of Service and respect copyright laws when using this scraper.