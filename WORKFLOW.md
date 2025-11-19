# Workflow Guide

## Visual Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                  SETUP PHASE (One Time)                      │
└─────────────────────────────────────────────────────────────┘

1. Install Dependencies
   ┌─────────────────────────────────┐
   │ pip install -r requirements.txt │
   └─────────────────────────────────┘
                  │
                  ▼
2. Configure Environment
   ┌─────────────────────────────────┐
   │ cp .env.example .env            │
   │ # Edit .env with credentials    │
   └─────────────────────────────────┘
                  │
                  ▼
3. Validate Configuration
   ┌─────────────────────────────────┐
   │ python validate_config.py       │
   └─────────────────────────────────┘
                  │
                  ▼
4. (Optional) Run Tests
   ┌─────────────────────────────────┐
   │ python test_extraction.py       │
   │ python utils.py test            │
   └─────────────────────────────────┘


┌─────────────────────────────────────────────────────────────┐
│                 EXTRACTION PHASE (Per Book)                  │
└─────────────────────────────────────────────────────────────┘

1. Update Book URL in .env
   ┌──────────────────────────────────────────┐
   │ BOOK_URL=https://archive.org/details/... │
   └──────────────────────────────────────────┘
                  │
                  ▼
2. Run Scraper
   ┌─────────────────────────────────┐
   │ python scraper.py               │
   └─────────────────────────────────┘
                  │
                  ├──────────────────────────────┐
                  │                              │
                  ▼                              ▼
         ┌─────────────────┐          ┌──────────────────┐
         │ Chrome Opens    │          │ Logs Display     │
         │ with Profile    │          │ Progress Info    │
         └─────────────────┘          └──────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Navigates to    │
         │ Book Page       │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Authenticates   │
         │ (if needed)     │
         └─────────────────┘
                  │
                  ▼
   ┌──────────────────────────────────┐
   │   FOR EACH PAGE IN BOOK:         │
   │                                  │
   │   1. Inject JS to pierce shadow  │
   │   2. Extract .BRwordElement text │
   │   3. Find next button in shadow  │
   │   4. Click next button           │
   │   5. Wait for page load          │
   │   6. Repeat                      │
   └──────────────────────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Save All Text   │
         │ to Output File  │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Close Browser   │
         └─────────────────┘


┌─────────────────────────────────────────────────────────────┐
│                  ANALYSIS PHASE (Optional)                   │
└─────────────────────────────────────────────────────────────┘

         ┌─────────────────────────┐
         │ extracted_text.txt      │
         └─────────────────────────┘
                  │
                  ├──────────────────┬──────────────────┬─────────────
                  │                  │                  │
                  ▼                  ▼                  ▼
         ┌─────────────┐    ┌─────────────┐   ┌─────────────┐
         │ Search Text │    │ Analyze     │   │ Process     │
         │ grep/find   │    │ Word Count  │   │ With Tools  │
         └─────────────┘    └─────────────┘   └─────────────┘
```

## Quick Reference Commands

### First Time Setup
```bash
# Clone and setup
git clone https://github.com/j-jayes/archive-book-getter-selenium.git
cd archive-book-getter-selenium
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env  # or vim, emacs, etc.

# Validate
python validate_config.py
```

### Daily Usage
```bash
# 1. Edit .env to set BOOK_URL
nano .env

# 2. Run scraper
python scraper.py

# 3. Check output
head -50 extracted_text.txt
```

### Troubleshooting
```bash
# Check configuration
python validate_config.py

# Test connection
python utils.py test

# View Chrome profile help
python utils.py profile

# Run extraction test
python test_extraction.py
```

### Working with Output
```bash
# View first 20 lines
head -20 extracted_text.txt

# Count lines/words
wc -l extracted_text.txt
wc -w extracted_text.txt

# Search for text
grep -i "keyword" extracted_text.txt

# Save specific sections
grep -A 10 "Chapter 1" extracted_text.txt > chapter1.txt
```

## Decision Tree

```
Need to extract text from Archive.org book?
                │
                ▼
        Is it your first time?
           ╱           ╲
         Yes            No
          │              │
          ▼              ▼
    Setup Phase    Just run scraper
     (10 min)       (python scraper.py)
          │              │
          └──────┬───────┘
                 ▼
        Getting errors?
           ╱         ╲
         Yes          No
          │            │
          ▼            ▼
    Run validation   Success!
    & diagnostics    Use output
          │
          ▼
    Still failing?
           │
           ▼
    Check TESTING.md
    & TROUBLESHOOTING
```

## Common Scenarios

### Scenario 1: First Time User
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your info
python validate_config.py
python scraper.py  # Start with max_pages=3 for testing
```

### Scenario 2: Extract Multiple Books
```bash
# For each book:
# 1. Update BOOK_URL in .env
# 2. Update OUTPUT_FILE for unique name
nano .env
python scraper.py
```

### Scenario 3: Testing/Debugging
```bash
# Test setup
python validate_config.py
python utils.py test

# Test extraction logic
python test_extraction.py

# Try with limited pages
# Edit scraper.py: scraper.run(max_pages=3)
python scraper.py
```

### Scenario 4: Authenticated Books
```bash
# Method 1: Use Chrome profile (recommended)
# Set CHROME_PROFILE_PATH in .env
python utils.py profile  # For help finding path

# Method 2: Manual login in code
# Scraper will prompt for login if needed
python scraper.py
```

## Time Estimates

- **Setup (first time)**: 5-10 minutes
- **Configuration per book**: 1 minute
- **Extraction rate**: ~1-3 pages per second
- **100-page book**: ~2-5 minutes
- **500-page book**: ~10-25 minutes

## Best Practices

1. ✅ Always validate config before first run
2. ✅ Test with limited pages first (3-5 pages)
3. ✅ Use unique output filenames for each book
4. ✅ Check output file after extraction
5. ✅ Keep .env file secure and backed up
6. ✅ Close Chrome when using profile mode
7. ✅ Monitor logs for errors during extraction

## What to Do When...

### ✓ Everything Works
- Check output file quality
- Verify text makes sense
- Process output as needed
- Extract more books!

### ⚠ Getting Warnings
- Check logs for details
- May still work - verify output
- Consider adjusting wait times

### ✗ Getting Errors
1. Run `python validate_config.py`
2. Check error messages in console
3. Review TESTING.md
4. Try with simpler book first
5. Check Chrome/ChromeDriver versions

## Support Resources

- **Quick Start**: `QUICKSTART.md`
- **Testing**: `TESTING.md`
- **Architecture**: `ARCHITECTURE.md`
- **Full Docs**: `README.md`
- **Examples**: `example_usage.py`
- **Validation**: `validate_config.py`
