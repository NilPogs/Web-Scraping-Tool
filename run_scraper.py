#!/usr/bin/env python3
"""
Simple CLI runner for Indeed Scraper with config file support
"""

import json
import sys
import os
from indeed_scraper import IndeedScraper

def load_config(config_file='config.json'):
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file '{config_file}' not found. Using defaults.")
        return {}
    except json.JSONDecodeError:
        print(f"Error parsing config file. Using defaults.")
        return {}

def main():
    print("\n" + "="*60)
    print("INDEED JOB SCRAPER - IT INDUSTRY (Config Mode)")
    print("="*60 + "\n")
    
    # Load configuration
    config = load_config()
    
    query = config.get('search_query', 'IT jobs')
    location = config.get('location', '')
    keywords = config.get('keywords', ['IT', 'Software', 'Developer'])
    year_filter = config.get('year_filter', None)
    max_pages = config.get('max_pages', 5)
    
    print(f"Configuration loaded:")
    print(f"  Query: {query}")
    print(f"  Location: {location if location else 'All locations'}")
    print(f"  Keywords: {', '.join(keywords)}")
    print(f"  Year filter: {year_filter if year_filter else 'None'}")
    print(f"  Max pages: {max_pages}")
    print()
    
    proceed = input("Proceed with scraping? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Scraping cancelled.")
        return
    
    # Create scraper instance
    scraper = IndeedScraper(keywords=keywords, year_filter=year_filter, max_pages=max_pages)
    
    # Scrape jobs
    scraper.scrape_jobs(query=query, location=location)
    
    # Save results
    if scraper.jobs_data:
        timestamp = scraper.jobs_data[0]['scraped_at'].replace(':', '-').replace(' ', '_')
        csv_file = f"indeed_jobs_{timestamp}.csv"
        json_file = f"indeed_jobs_{timestamp}.json"
        
        scraper.save_to_csv(csv_file)
        scraper.save_to_json(json_file)
        scraper.get_summary()
        
        print(f"\nFiles saved:")
        print(f"  - {csv_file}")
        print(f"  - {json_file}")
    else:
        print("\nNo jobs were scraped. Please try different search parameters.")

if __name__ == "__main__":
    main()
