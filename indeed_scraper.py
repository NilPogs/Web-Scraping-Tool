#!/usr/bin/env python3
"""
Indeed Job Scraper - IT Industry Focus
Scrapes job postings from Indeed.com with keyword and year filtering
Compatible with Python 3.10+
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import re
from datetime import datetime, timedelta
from urllib.parse import quote_plus
import os
import sys

class IndeedScraper:
    def __init__(self, keywords=None, year_filter=None, max_pages=5):
        """
        Initialize the Indeed scraper
        
        Args:
            keywords (list): List of keywords to filter jobs
            year_filter (int): Year to filter jobs (e.g., 2021)
            max_pages (int): Maximum number of pages to scrape
        """
        self.base_url = "https://www.indeed.com"
        self.keywords = keywords if keywords else ["IT", "Software", "Developer"]
        self.year_filter = year_filter
        self.max_pages = max_pages
        self.jobs_data = []
        
        # Headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def parse_date(self, date_str):
        """
        Parse Indeed date strings and convert to datetime
        
        Args:
            date_str (str): Date string from Indeed (e.g., "30+ days ago", "Just posted")
        
        Returns:
            datetime: Parsed date or None
        """
        if not date_str:
            return None
        
        date_str = date_str.lower().strip()
        today = datetime.now()
        
        try:
            if 'just posted' in date_str or 'today' in date_str:
                return today
            elif 'yesterday' in date_str:
                return today - timedelta(days=1)
            elif 'days ago' in date_str:
                days = int(re.search(r'(\d+)', date_str).group(1))
                return today - timedelta(days=days)
            elif 'month' in date_str:
                months = int(re.search(r'(\d+)', date_str).group(1)) if re.search(r'(\d+)', date_str) else 1
                return today - timedelta(days=months * 30)
            elif '30+' in date_str:
                return today - timedelta(days=30)
        except:
            pass
        
        return None
    
    def matches_year(self, date_obj):
        """
        Check if a date matches the year filter
        
        Args:
            date_obj (datetime): Date to check
        
        Returns:
            bool: True if matches year filter or no filter set
        """
        if not self.year_filter or not date_obj:
            return True
        
        return date_obj.year == self.year_filter
    
    def matches_keywords(self, text):
        """
        Check if text contains any of the keywords
        
        Args:
            text (str): Text to search
        
        Returns:
            bool: True if any keyword is found
        """
        if not self.keywords or not text:
            return True
        
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.keywords)
    
    def scrape_job_details(self, job_url):
        """
        Scrape detailed information from a job posting
        
        Args:
            job_url (str): URL of the job posting
        
        Returns:
            dict: Job details
        """
        try:
            time.sleep(1)  # Rate limiting
            response = requests.get(job_url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job description
            description_div = soup.find('div', {'id': 'jobDescriptionText'})
            description = description_div.get_text(strip=True) if description_div else ""
            
            return {'description': description}
        
        except Exception as e:
            print(f"Error scraping job details: {e}")
            return None
    
    def scrape_jobs(self, query="IT jobs", location=""):
        """
        Scrape jobs from Indeed
        
        Args:
            query (str): Job search query
            location (str): Location to search
        """
        print(f"\n{'='*60}")
        print(f"Starting Indeed Job Scraper")
        print(f"{'='*60}")
        print(f"Query: {query}")
        print(f"Location: {location if location else 'All locations'}")
        print(f"Keywords filter: {', '.join(self.keywords)}")
        print(f"Year filter: {self.year_filter if self.year_filter else 'None'}")
        print(f"Max pages: {self.max_pages}")
        print(f"{'='*60}\n")
        
        for page in range(self.max_pages):
            start = page * 10
            url = f"{self.base_url}/jobs?q={quote_plus(query)}&l={quote_plus(location)}&start={start}"
            
            print(f"Scraping page {page + 1}/{self.max_pages}...")
            
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code != 200:
                    print(f"Failed to fetch page {page + 1}. Status code: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards (Indeed's structure may vary)
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                if not job_cards:
                    # Try alternative structure
                    job_cards = soup.find_all('td', class_='resultContent')
                
                if not job_cards:
                    print(f"No jobs found on page {page + 1}")
                    break
                
                print(f"Found {len(job_cards)} job listings on page {page + 1}")
                
                for card in job_cards:
                    try:
                        # Extract job title
                        title_elem = card.find('h2', class_='jobTitle')
                        if not title_elem:
                            title_elem = card.find('a', class_='jcs-JobTitle')
                        
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        job_link = title_elem.find('a')
                        job_url = self.base_url + job_link['href'] if job_link and 'href' in job_link.attrs else ""
                        
                        # Extract company name
                        company_elem = card.find('span', class_='companyName')
                        company = company_elem.get_text(strip=True) if company_elem else "N/A"
                        
                        # Extract location
                        location_elem = card.find('div', class_='companyLocation')
                        job_location = location_elem.get_text(strip=True) if location_elem else "N/A"
                        
                        # Extract salary (if available)
                        salary_elem = card.find('div', class_='salary-snippet')
                        salary = salary_elem.get_text(strip=True) if salary_elem else "N/A"
                        
                        # Extract date posted
                        date_elem = card.find('span', class_='date')
                        date_str = date_elem.get_text(strip=True) if date_elem else ""
                        date_posted = self.parse_date(date_str)
                        
                        # Extract job snippet
                        snippet_elem = card.find('div', class_='job-snippet')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                        
                        # Apply filters
                        if not self.matches_keywords(title + " " + snippet):
                            continue
                        
                        if not self.matches_year(date_posted):
                            continue
                        
                        # Create job data
                        job_data = {
                            'title': title,
                            'company': company,
                            'location': job_location,
                            'salary': salary,
                            'date_posted': date_posted.strftime('%Y-%m-%d') if date_posted else "N/A",
                            'snippet': snippet,
                            'url': job_url,
                            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        self.jobs_data.append(job_data)
                        print(f"  ✓ Added: {title} at {company}")
                    
                    except Exception as e:
                        print(f"  ✗ Error parsing job card: {e}")
                        continue
                
                # Rate limiting between pages
                time.sleep(2)
            
            except Exception as e:
                print(f"Error scraping page {page + 1}: {e}")
                continue
        
        print(f"\n{'='*60}")
        print(f"Scraping completed! Total jobs collected: {len(self.jobs_data)}")
        print(f"{'='*60}\n")
    
    def save_to_csv(self, filename="indeed_jobs.csv"):
        """Save scraped jobs to CSV file"""
        if not self.jobs_data:
            print("No data to save!")
            return
        
        df = pd.DataFrame(self.jobs_data)
        df.to_csv(filename, index=False)
        print(f"✓ Data saved to {filename}")
        return filename
    
    def save_to_json(self, filename="indeed_jobs.json"):
        """Save scraped jobs to JSON file"""
        if not self.jobs_data:
            print("No data to save!")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.jobs_data, f, indent=2, ensure_ascii=False)
        print(f"✓ Data saved to {filename}")
        return filename
    
    def get_summary(self):
        """Print summary statistics"""
        if not self.jobs_data:
            print("No data available!")
            return
        
        df = pd.DataFrame(self.jobs_data)
        
        print(f"\n{'='*60}")
        print(f"SCRAPING SUMMARY")
        print(f"{'='*60}")
        print(f"Total jobs collected: {len(self.jobs_data)}")
        print(f"\nTop 5 Companies:")
        print(df['company'].value_counts().head())
        print(f"\nTop 5 Locations:")
        print(df['location'].value_counts().head())
        print(f"{'='*60}\n")


def main():
    """Main function to run the scraper"""
    print("\n" + "="*60)
    print("INDEED JOB SCRAPER - IT INDUSTRY")
    print("="*60 + "\n")
    
    # Configuration
    query = input("Enter job search query (default: 'IT jobs'): ").strip() or "IT jobs"
    location = input("Enter location (default: ''): ").strip()
    
    keywords_input = input("Enter keywords to filter (comma-separated, default: 'IT,Software,Developer'): ").strip()
    keywords = [k.strip() for k in keywords_input.split(',')] if keywords_input else ["IT", "Software", "Developer"]
    
    year_input = input("Enter year to filter (e.g., 2021, or press Enter for no filter): ").strip()
    year_filter = int(year_input) if year_input.isdigit() else None
    
    max_pages_input = input("Enter maximum pages to scrape (default: 5): ").strip()
    max_pages = int(max_pages_input) if max_pages_input.isdigit() else 5
    
    # Create scraper instance
    scraper = IndeedScraper(keywords=keywords, year_filter=year_filter, max_pages=max_pages)
    
    # Scrape jobs
    scraper.scrape_jobs(query=query, location=location)
    
    # Save results
    if scraper.jobs_data:
        csv_file = scraper.save_to_csv()
        json_file = scraper.save_to_json()
        scraper.get_summary()
        
        print(f"\nFiles saved:")
        print(f"  - {csv_file}")
        print(f"  - {json_file}")
    else:
        print("\nNo jobs were scraped. Please try different search parameters.")


if __name__ == "__main__":
    main()
