# app/services/job_scraper.py
import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional
from urllib.parse import urlparse, urljoin
import time
import json

class JobDescriptionScraper:
    """
    Service to scrape job descriptions from various job posting websites
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Timeout settings
        self.timeout = 10
        
        # Initialize site-specific scrapers
        self.scrapers = {
            'linkedin.com': self._scrape_linkedin,
            'indeed.com': self._scrape_indeed,
            'glassdoor.com': self._scrape_glassdoor,
            'monster.com': self._scrape_monster,
            'dice.com': self._scrape_dice,
            'stackoverflow.com': self._scrape_stackoverflow,
            'angel.co': self._scrape_angellist,
            'wellfound.com': self._scrape_angellist,  # AngelList rebranded
            'lever.co': self._scrape_lever,
            'greenhouse.io': self._scrape_greenhouse,
            'workday.com': self._scrape_workday,
            'bamboohr.com': self._scrape_bamboohr,
            'smartrecruiters.com': self._scrape_smartrecruiters
        }
    
    def scrape_job_description(self, url: str) -> Dict:
        """
        Main method to scrape job description from URL
        """
        try:
            print(f"🔍 Scraping job description from: {url}")
            
            # Validate URL
            if not self._is_valid_url(url):
                raise ValueError("Invalid URL provided")
            
            # Parse domain
            domain = urlparse(url).netloc.lower()
            domain = domain.replace('www.', '')
            
            # Try specific scraper first
            scraper = None
            for site_domain, scraper_func in self.scrapers.items():
                if site_domain in domain:
                    scraper = scraper_func
                    break
            
            if scraper:
                result = scraper(url)
            else:
                # Fallback to generic scraping
                result = self._scrape_generic(url)
            
            if result and result.get('description'):
                print(f"✅ Successfully scraped {len(result['description'])} characters")
                return {
                    'success': True,
                    'title': result.get('title', 'Job Title'),
                    'company': result.get('company', 'Company Name'),
                    'location': result.get('location', ''),
                    'description': result['description'],
                    'requirements': result.get('requirements', ''),
                    'benefits': result.get('benefits', ''),
                    'url': url,
                    'scraped_from': domain
                }
            else:
                raise Exception("No job description content found")
                
        except requests.exceptions.Timeout:
            raise Exception("Request timeout - the website took too long to respond")
        except requests.exceptions.ConnectionError:
            raise Exception("Connection error - unable to reach the website")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Scraping error: {str(e)}")
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate if URL is properly formatted"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _get_page_content(self, url: str) -> BeautifulSoup:
        """Get page content with error handling"""
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        return BeautifulSoup(response.content, 'html.parser')
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        
        # Remove HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        
        return text.strip()
    
    # Site-specific scrapers
    def _scrape_linkedin(self, url: str) -> Dict:
        """Scrape LinkedIn job posting"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Job title
        title_elem = soup.find('h1', {'class': 'top-card-layout__title'}) or \
                    soup.find('h1', class_=re.compile(r'.*job.*title.*'))
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Company name
        company_elem = soup.find('a', {'class': 'topcard__org-name-link'}) or \
                      soup.find('span', class_=re.compile(r'.*company.*name.*'))
        result['company'] = self._clean_text(company_elem.get_text()) if company_elem else ""
        
        # Location
        location_elem = soup.find('span', {'class': 'topcard__flavor--bullet'}) or \
                       soup.find('span', class_=re.compile(r'.*location.*'))
        result['location'] = self._clean_text(location_elem.get_text()) if location_elem else ""
        
        # Job description
        description_elem = soup.find('div', {'class': 'description__text'}) or \
                          soup.find('div', class_=re.compile(r'.*description.*')) or \
                          soup.find('section', class_=re.compile(r'.*job.*details.*'))
        
        if description_elem:
            result['description'] = self._clean_text(description_elem.get_text())
        else:
            # Fallback - get all paragraph text
            paragraphs = soup.find_all('p')
            result['description'] = '\n'.join([self._clean_text(p.get_text()) for p in paragraphs])
        
        return result
    
    def _scrape_indeed(self, url: str) -> Dict:
        """Scrape Indeed job posting"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Job title
        title_elem = soup.find('h1', {'data-testid': 'jobsearch-JobInfoHeader-title'}) or \
                    soup.find('h1', class_=re.compile(r'.*title.*'))
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Company
        company_elem = soup.find('span', {'data-testid': 'jobsearch-CompanyInfoWithoutHeaderImage'}) or \
                      soup.find('a', {'data-testid': 'jobsearch-CompanyInfoContainer'})
        result['company'] = self._clean_text(company_elem.get_text()) if company_elem else ""
        
        # Description
        description_elem = soup.find('div', {'id': 'jobDescriptionText'}) or \
                          soup.find('div', class_=re.compile(r'.*job.*description.*'))
        
        if description_elem:
            result['description'] = self._clean_text(description_elem.get_text())
        else:
            # Fallback
            job_content = soup.find('div', class_=re.compile(r'.*content.*'))
            result['description'] = self._clean_text(job_content.get_text()) if job_content else ""
        
        return result
    
    def _scrape_glassdoor(self, url: str) -> Dict:
        """Scrape Glassdoor job posting"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Job title
        title_elem = soup.find('div', {'data-test': 'job-title'}) or \
                    soup.find('h1', class_=re.compile(r'.*title.*'))
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Company
        company_elem = soup.find('div', {'data-test': 'employer-name'}) or \
                      soup.find('span', class_=re.compile(r'.*employer.*'))
        result['company'] = self._clean_text(company_elem.get_text()) if company_elem else ""
        
        # Description
        description_elem = soup.find('div', {'data-test': 'jobDescriptionContent'}) or \
                          soup.find('div', class_=re.compile(r'.*description.*'))
        
        result['description'] = self._clean_text(description_elem.get_text()) if description_elem else ""
        
        return result
    
    def _scrape_dice(self, url: str) -> Dict:
        """Scrape Dice job posting"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Job title
        title_elem = soup.find('h1', {'data-cy': 'jobTitle'}) or soup.find('h1')
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Company
        company_elem = soup.find('a', {'data-cy': 'companyNameLink'})
        result['company'] = self._clean_text(company_elem.get_text()) if company_elem else ""
        
        # Description
        description_elem = soup.find('div', {'data-cy': 'jobDescription'})
        result['description'] = self._clean_text(description_elem.get_text()) if description_elem else ""
        
        return result
    
    def _scrape_stackoverflow(self, url: str) -> Dict:
        """Scrape Stack Overflow Jobs"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Job title
        title_elem = soup.find('h1', class_=re.compile(r'.*title.*')) or soup.find('h1')
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Company
        company_elem = soup.find('span', class_=re.compile(r'.*company.*'))
        result['company'] = self._clean_text(company_elem.get_text()) if company_elem else ""
        
        # Description
        description_elem = soup.find('div', class_=re.compile(r'.*description.*|.*content.*'))
        result['description'] = self._clean_text(description_elem.get_text()) if description_elem else ""
        
        return result
    
    def _scrape_angellist(self, url: str) -> Dict:
        """Scrape AngelList/Wellfound job posting"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # These sites often use React, so content might be loaded dynamically
        # Try to get basic info from meta tags and visible content
        
        # Job title from meta or header
        title_elem = soup.find('h1') or soup.find('title')
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Get all text content as description
        main_content = soup.find('main') or soup.find('div', {'id': 'root'})
        if main_content:
            result['description'] = self._clean_text(main_content.get_text())
        else:
            result['description'] = self._clean_text(soup.get_text())
        
        return result
    
    def _scrape_lever(self, url: str) -> Dict:
        """Scrape Lever job posting"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Job title
        title_elem = soup.find('h2', {'data-qa': 'posting-name'}) or soup.find('h1') or soup.find('h2')
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Company
        company_elem = soup.find('div', {'data-qa': 'posting-company'})
        result['company'] = self._clean_text(company_elem.get_text()) if company_elem else ""
        
        # Description
        description_elem = soup.find('div', {'data-qa': 'posting-description'}) or \
                          soup.find('div', class_=re.compile(r'.*content.*'))
        result['description'] = self._clean_text(description_elem.get_text()) if description_elem else ""
        
        return result
    
    def _scrape_greenhouse(self, url: str) -> Dict:
        """Scrape Greenhouse job posting"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Job title
        title_elem = soup.find('h1', {'data-test': 'job-title'}) or soup.find('h1')
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Description
        description_elem = soup.find('div', {'data-test': 'job-description'}) or \
                          soup.find('div', class_=re.compile(r'.*content.*|.*description.*'))
        result['description'] = self._clean_text(description_elem.get_text()) if description_elem else ""
        
        return result
    
    def _scrape_workday(self, url: str) -> Dict:
        """Scrape Workday job posting"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Workday uses specific data attributes
        title_elem = soup.find('h1', {'data-automation-id': 'jobPostingHeader'}) or soup.find('h1')
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Description
        description_elem = soup.find('div', {'data-automation-id': 'jobPostingDescription'})
        result['description'] = self._clean_text(description_elem.get_text()) if description_elem else ""
        
        return result
    
    def _scrape_bamboohr(self, url: str) -> Dict:
        """Scrape BambooHR job posting"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Job title
        title_elem = soup.find('h1') or soup.find('h2', class_=re.compile(r'.*title.*'))
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Description
        description_elem = soup.find('div', class_=re.compile(r'.*description.*|.*content.*'))
        result['description'] = self._clean_text(description_elem.get_text()) if description_elem else ""
        
        return result
    
    def _scrape_smartrecruiters(self, url: str) -> Dict:
        """Scrape SmartRecruiters job posting"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Job title
        title_elem = soup.find('h1') or soup.find('div', class_=re.compile(r'.*title.*'))
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Description
        description_elem = soup.find('div', class_=re.compile(r'.*description.*|.*content.*'))
        result['description'] = self._clean_text(description_elem.get_text()) if description_elem else ""
        
        return result
    
    def _scrape_monster(self, url: str) -> Dict:
        """Scrape Monster job posting"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Job title
        title_elem = soup.find('h1', {'data-testid': 'svx-job-header-title'}) or soup.find('h1')
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else ""
        
        # Company
        company_elem = soup.find('span', {'data-testid': 'svx-job-header-company-name'})
        result['company'] = self._clean_text(company_elem.get_text()) if company_elem else ""
        
        # Description
        description_elem = soup.find('div', {'data-testid': 'svx-job-description-content'})
        result['description'] = self._clean_text(description_elem.get_text()) if description_elem else ""
        
        return result
    
    def _scrape_generic(self, url: str) -> Dict:
        """Generic scraper for unknown sites"""
        soup = self._get_page_content(url)
        
        result = {}
        
        # Try to find job title
        title_elem = soup.find('h1') or soup.find('h2') or soup.find('title')
        result['title'] = self._clean_text(title_elem.get_text()) if title_elem else "Job Title"
        
        # Try to find main content
        content_selectors = [
            'main', 'article', '[role="main"]',
            '.content', '.job-description', '.description',
            '.post-content', '.entry-content', '.job-details'
        ]
        
        description = ""
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                description = self._clean_text(content_elem.get_text())
                break
        
        # Fallback: get all paragraph text
        if not description:
            paragraphs = soup.find_all('p')
            description = '\n\n'.join([self._clean_text(p.get_text()) for p in paragraphs if len(p.get_text().strip()) > 50])
        
        # Final fallback: get all text
        if not description:
            description = self._clean_text(soup.get_text())
        
        result['description'] = description
        result['company'] = "Company Name"
        
        return result
