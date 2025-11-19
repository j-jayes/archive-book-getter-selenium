# Architecture Documentation

## Overview

The Archive Book Scraper is designed to extract text from Internet Archive books that use Shadow DOM encapsulation. This document explains the technical architecture and implementation details.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Archive Book Scraper                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐     ┌──────────────────┐              │
│  │  Configuration  │────▶│  Selenium Driver │              │
│  │   (.env file)   │     │   (Chrome)       │              │
│  └─────────────────┘     └──────────────────┘              │
│                                   │                          │
│                                   ▼                          │
│                          ┌─────────────────┐                │
│                          │  Chrome Profile │                │
│                          │  (Auth Session) │                │
│                          └─────────────────┘                │
│                                   │                          │
│                                   ▼                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Internet Archive Book Reader                │  │
│  │                                                        │  │
│  │    ┌─────────────────────────────────────┐           │  │
│  │    │      <ia-book-theater>              │           │  │
│  │    │      (Custom Element)               │           │  │
│  │    │                                     │           │  │
│  │    │   ┌──────────────────────┐         │           │  │
│  │    │   │   #shadow-root        │         │           │  │
│  │    │   │                       │         │           │  │
│  │    │   │  ┌─────────────────┐ │         │           │  │
│  │    │   │  │ .BRwordElement  │ │         │           │  │
│  │    │   │  │ .BRwordElement  │ │◀────────┼───────┐   │  │
│  │    │   │  │ .BRwordElement  │ │         │       │   │  │
│  │    │   │  └─────────────────┘ │         │       │   │  │
│  │    │   │                       │         │       │   │  │
│  │    │   │  ┌─────────────────┐ │         │   Recursive  │
│  │    │   │  │ Nested Elements │ │         │    Shadow    │
│  │    │   │  │  #shadow-root   │ │         │     DOM      │
│  │    │   │  │  └──────────────┤ │         │   Piercing   │
│  │    │   │     .BRwordElement │ │         │       │   │  │
│  │    │   │  └─────────────────┘ │         │       │   │  │
│  │    │   └──────────────────────┘         │       │   │  │
│  │    └─────────────────────────────────────┘       │   │  │
│  └──────────────────────────────────────────────────┼───┘  │
│                                                      │       │
│                                                      ▼       │
│                          ┌──────────────────────────────┐   │
│                          │   Text Extraction Engine    │   │
│                          │   (JavaScript Injection)    │   │
│                          └──────────────────────────┬───┘   │
│                                                      │       │
│                                                      ▼       │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              Pagination Handler                       │ │
│  │  (Find & Click Next Button in Shadow DOM)            │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                      │       │
│                                                      ▼       │
│                          ┌──────────────────────────────┐   │
│                          │    File Output System       │   │
│                          │  (extracted_text.txt)       │   │
│                          └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. ArchiveBookScraper Class

The main class that orchestrates the entire scraping process.

**Key Methods:**
- `setup_driver()`: Configures Chrome with local profile support
- `login()`: Handles authentication with Internet Archive
- `pierce_shadow_dom()`: Basic shadow DOM access
- `extract_text_from_shadow_dom()`: Recursive text extraction
- `find_next_button_in_shadow()`: Pagination handler
- `scrape_book()`: Main orchestration loop
- `save_to_file()`: Output generation

### 2. Shadow DOM Piercing Algorithm

The core innovation is the recursive Shadow DOM traversal:

```javascript
function extractTextFromShadowDOM(root) {
    // Recursive traversal through all shadow roots
    function traverse(element) {
        // 1. Check for shadow root
        if (element.shadowRoot) {
            traverse(element.shadowRoot);
        }
        
        // 2. If DocumentFragment/ShadowRoot, query for .BRwordElement
        if (element instanceof DocumentFragment || element instanceof ShadowRoot) {
            const wordElements = element.querySelectorAll('.BRwordElement');
            // Extract text from each
        }
        
        // 3. Recursively traverse children
        // 4. Handle both shadow and regular DOM nodes
    }
}
```

**Why This Works:**
- Shadow DOM creates encapsulation boundaries
- Standard `querySelector` cannot cross shadow boundaries
- Our algorithm recursively accesses each shadow root
- Collects text from `.BRwordElement` nodes at any depth

### 3. Pagination System

The pagination handler searches for "next" buttons within shadow-nested structures:

```javascript
function findAndClickNext(root) {
    // Multiple selector strategies
    const selectors = [
        'button.BRicon.next',
        'button[title*="next" i]',
        'button[aria-label*="next" i]',
        // ... more patterns
    ];
    
    // Recursive search through shadow boundaries
    // Click when found and enabled
}
```

## Data Flow

1. **Initialization**
   - Load `.env` configuration
   - Validate required credentials
   - Initialize Selenium WebDriver

2. **Authentication**
   - Load Chrome with user profile (if configured)
   - Navigate to target book URL
   - Login if not already authenticated

3. **Page Processing Loop**
   ```
   For each page:
     ├─ Inject JavaScript for Shadow DOM traversal
     ├─ Extract all .BRwordElement text nodes
     ├─ Accumulate text in memory
     ├─ Search for next button in Shadow DOM
     ├─ Click next button
     └─ Wait for page load
   ```

4. **Output Generation**
   - Write accumulated text to file
   - One text element per line
   - UTF-8 encoding

## Shadow DOM Challenges & Solutions

### Challenge 1: Encapsulation
**Problem:** Shadow DOM creates isolated DOM trees that normal selectors can't access.

**Solution:** Recursively access each element's `shadowRoot` property to traverse all shadow boundaries.

### Challenge 2: Dynamic Content
**Problem:** Book reader loads content dynamically as pages change.

**Solution:** Wait for page transitions and re-execute extraction on each page.

### Challenge 3: Button Location
**Problem:** Pagination buttons are buried in shadow-nested structures.

**Solution:** Implement recursive button finder with multiple selector patterns.

### Challenge 4: Authentication
**Problem:** Books may require login, cookies, sessions.

**Solution:** Use local Chrome profile to maintain authenticated sessions.

## Security Considerations

1. **Credential Storage**
   - Credentials stored in `.env` file
   - `.env` excluded from version control via `.gitignore`
   - Never logged or displayed in plain text

2. **Profile Access**
   - Chrome profile used for convenience
   - Contains browser session data
   - User must ensure Chrome is closed during profile use

3. **Data Privacy**
   - Extracted text stored locally only
   - No external services called
   - No data transmission beyond archive.org

## Performance Optimization

1. **Wait Times**
   - Configurable delays between pages
   - Balance between speed and reliability
   - Default: 1-2 seconds per page

2. **Memory Management**
   - Text accumulated in Python list
   - Written to file at end
   - Suitable for books up to thousands of pages

3. **Error Recovery**
   - Graceful handling of missing elements
   - Continues on partial failures
   - Comprehensive logging

## Extension Points

The scraper is designed for easy extension:

1. **Custom Extractors**
   - Modify `extract_text_from_shadow_dom()` for different elements
   - Add custom selectors for specific sites

2. **Output Formats**
   - Modify `save_to_file()` for JSON, CSV, etc.
   - Add metadata extraction

3. **Pagination Strategies**
   - Extend `find_next_button_in_shadow()` for different UI patterns
   - Add keyboard navigation support

4. **Authentication Methods**
   - Extend `login()` for different auth flows
   - Add OAuth or API key support

## Testing Strategy

1. **Unit Testing** (test_shadow_dom.html)
   - Validates JavaScript extraction logic
   - Tests with known Shadow DOM structure
   - Verifies button finding algorithms

2. **Configuration Validation** (validate_config.py)
   - Ensures environment is properly configured
   - Validates credentials and paths
   - Checks dependencies

3. **Integration Testing** (utils.py)
   - Tests connection to Internet Archive
   - Validates ChromeDriver setup
   - Checks end-to-end flow

## Troubleshooting Guide

### Common Issues

1. **No text extracted**
   - Verify book uses `.BRwordElement` class
   - Check JavaScript console for errors
   - Inspect actual Shadow DOM structure

2. **Pagination fails**
   - Book may use different button classes
   - Inspect actual pagination elements
   - Modify button selectors

3. **Authentication issues**
   - Close Chrome before using profile
   - Verify profile path is correct
   - Try manual login first

4. **ChromeDriver errors**
   - Ensure Chrome and ChromeDriver versions match
   - Update ChromeDriver via webdriver-manager
   - Check system permissions

## Dependencies

- **selenium**: Browser automation
- **python-dotenv**: Environment configuration
- **webdriver-manager**: Automatic ChromeDriver management

## Future Enhancements

Potential improvements for future versions:

1. **Parallel Processing**
   - Process multiple pages concurrently
   - Faster extraction for large books

2. **OCR Integration**
   - Extract text from page images
   - Handle books without text layer

3. **Progress Tracking**
   - Save checkpoints during extraction
   - Resume from interruption

4. **Format Preservation**
   - Maintain paragraph structure
   - Preserve formatting information

5. **Metadata Extraction**
   - Book title, author, publication info
   - Page numbers and structure

6. **GUI Interface**
   - User-friendly configuration
   - Real-time progress visualization
   - Batch processing support
