# Indeed Job Scraper

A Python-based web scraping tool for extracting IT job postings from Indeed.com with advanced filtering capabilities by year and keywords.

## Features

- 🔍 Search jobs by keywords and location
- 📅 Filter jobs by posting year (focused on 2021 for research)
- 🏷️ Filter by specific keywords in job descriptions
- 💾 Export data to CSV or JSON formats
- 📊 Generate summary statistics
- ⚙️ Easy configuration via JSON file
- 🚦 Built-in rate limiting to respect Indeed's servers

## Requirements

- Python 3.10 or above
- Chrome/Chromium browser
- ChromeDriver (for Selenium)

## Installation

1. **Clone or extract the project files**

2. **Install Python dependencies:**
```bash
pip3 install -r requirements.txt
```

3. **Install ChromeDriver (Ubuntu/Debian):**
```bash
sudo apt install -y chromium-browser chromium-chromedriver
```

For other operating systems, download ChromeDriver from:
https://chromedriver.chromium.org/

## Configuration

Edit `config.json` to customize your search parameters:

```json
{
  "search_query": "software engineer",
  "location": "United States",
  "keywords": ["python", "java", "javascript", "devops"],
  "year_filter": 2021,
  "max_pages": 5,
  "output_format": "csv",
  "rate_limit_seconds": 2
}
```

### Configuration Parameters:

- **search_query**: Main job search term (e.g., "software engineer", "data analyst")
- **location**: Geographic location for job search
- **keywords**: List of keywords to filter job descriptions (case-insensitive)
- **year_filter**: Year to filter jobs by posting date (e.g., 2021)
- **max_pages**: Maximum number of Indeed pages to scrape (10 jobs per page)
- **output_format**: Output file format - "csv", "json", or "both"
- **rate_limit_seconds**: Delay between requests in seconds (recommended: 2-5)

## Usage

### Method 1: Using the CLI Runner (Recommended)

```bash
python3 run_scraper.py
```

This will use the settings from `config.json` and automatically save results.

### Method 2: Using the Scraper Class Directly

```python
from indeed_scraper import IndeedScraper

# Initialize scraper
scraper = IndeedScraper(
    search_query="software engineer",
    location="United States",
    keywords=["python", "machine learning"],
    year_filter=2021
)

# Scrape jobs
jobs = scraper.scrape_jobs(max_pages=5)

# Save results
scraper.save_to_csv(jobs, "jobs_output.csv")
scraper.save_to_json(jobs, "jobs_output.json")

# Print summary
scraper.print_summary(jobs)
```

## Output Format

### CSV Output
The CSV file contains the following columns:
- **title**: Job title
- **company**: Company name
- **location**: Job location
- **salary**: Salary information (if available)
- **date_posted**: When the job was posted
- **job_url**: Direct link to the job posting
- **description_snippet**: Brief job description

### JSON Output
The JSON file contains an array of job objects with the same fields as CSV.

## Example Output

```
=== Indeed Job Scraper ===
Search Query: software engineer
Location: United States
Keywords Filter: ['python', 'java']
Year Filter: 2021
Max Pages: 5

Starting scrape...
Scraping page 1...
Scraping page 2...
Scraping page 3...

=== Scraping Summary ===
Total jobs found: 45
Jobs matching year 2021: 32
Jobs matching keywords: 28
Final filtered results: 25

Results saved to:
- jobs_2024-01-15_143022.csv
```

## Important Notes

### Legal and Ethical Considerations

1. **Terms of Service**: Web scraping may violate Indeed's Terms of Service. This tool is intended for educational and research purposes only.

2. **Rate Limiting**: The tool includes built-in rate limiting. Please be respectful of Indeed's servers and don't set rate_limit_seconds too low.

3. **Personal Use**: This tool should only be used for personal research purposes, not for commercial data collection.

4. **Data Privacy**: Be mindful of privacy when handling scraped data. Don't share or publish personal information.

### Technical Limitations

1. **Dynamic Content**: Indeed uses JavaScript extensively. The scraper uses requests/BeautifulSoup which may not capture all dynamically loaded content. For more robust scraping, consider using the Selenium-based approach (commented in the code).

2. **Anti-Scraping Measures**: Indeed may implement CAPTCHAs or IP blocking. If you encounter issues:
   - Increase `rate_limit_seconds`
   - Reduce `max_pages`
   - Use a VPN or proxy
   - Consider using Selenium with headless Chrome

3. **Date Filtering Accuracy**: Year filtering is based on relative date strings (e.g., "Posted 30+ days ago"). The accuracy depends on Indeed's date format.

4. **Keyword Matching**: Keywords are matched case-insensitively in job descriptions. Partial matches are included.

## Troubleshooting

### "No jobs found"
- Check your internet connection
- Verify the search_query and location are valid
- Indeed may be blocking requests - try increasing rate_limit_seconds
- Try using a different search query

### "ChromeDriver not found" (if using Selenium)
- Ensure ChromeDriver is installed and in your PATH
- On Ubuntu: `sudo apt install chromium-chromedriver`
- Verify with: `which chromedriver`

### "Module not found" errors
- Ensure all dependencies are installed: `pip3 install -r requirements.txt`
- Check Python version: `python3 --version` (should be 3.10+)

## Project Structure

```
indeed-scraper/
├── indeed_scraper.py    # Main scraper class
├── run_scraper.py       # CLI runner script
├── config.json          # Configuration file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Future Enhancements

- [ ] Add support for multiple job boards (LinkedIn, Glassdoor)
- [ ] Implement proxy rotation for better reliability
- [ ] Add GUI interface
- [ ] Database storage option (SQLite/PostgreSQL)
- [ ] Email notifications when new jobs match criteria
- [ ] Advanced filtering (salary range, experience level)

## License

This project is provided as-is for educational purposes. Use responsibly and in accordance with Indeed's Terms of Service.

## Disclaimer

This tool is for educational and research purposes only. The authors are not responsible for any misuse or violations of Indeed's Terms of Service. Always respect website terms of service and robots.txt files.

## Support

For issues or questions, please review the Troubleshooting section above.

---

**Version:** 1.0  
**Last Updated:** 2024  
**Python Version:** 3.10+
