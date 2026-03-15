#!/usr/bin/env python3
"""
Quick test script for the Indeed scraper - runs without confirmation
"""

from indeed_scraper import IndeedScraper

print("=== Testing Indeed Scraper ===\n")

# Initialize scraper with filters
scraper = IndeedScraper(
    keywords=["python"],
    year_filter=2021,
    max_pages=1
)

print("Attempting to scrape 1 page as a test...")
jobs = scraper.scrape_jobs(query="software engineer", location="United States")

print(f"\nTest Results:")
print(f"- Total jobs scraped: {len(jobs)}")

if jobs:
    print(f"- Sample job title: {jobs[0].get('title', 'N/A')}")
    print(f"- Sample company: {jobs[0].get('company', 'N/A')}")
    print("\n✓ Scraper is working!")
else:
    print("\n⚠ No jobs found. This could be due to:")
    print("  - Indeed blocking requests")
    print("  - Network issues")
    print("  - Changes in Indeed's HTML structure")
    print("  - Strict filtering (year 2021 + keywords)")

print("\nNote: The main scraper (run_scraper.py) is ready to use with config.json")
