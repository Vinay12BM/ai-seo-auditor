# backend/app/services/crawler.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def crawl_website_data(url: str) -> dict:
    """
    Simulates crawling a URL to extract core SEO data.
    In a real-world app, this would be much more extensive (e.g., using Puppeteer, checking all links, etc.)
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Basic SEO data extraction
        title = soup.find('title').text if soup.find('title') else "N/A"
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description['content'] if meta_description else "N/A"
        
        h1 = soup.find('h1').text if soup.find('h1') else "N/A"
        
        # Count links (Internal vs. External would be better, but we keep it simple here)
        all_links = soup.find_all('a', href=True)
        link_count = len(all_links)

        # Basic technical metrics (simulated)
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        return {
            "url": url,
            "domain": domain,
            "html_head_data": {
                "title": title,
                "meta_description": description,
            },
            "on_page_elements": {
                "h1_content": h1,
                "total_links_found": link_count,
            },
            "simulated_metrics": {
                "page_load_time_s": 2.1,
                "mobile_friendly": "Yes",
                "structured_data_present": "No (Missing)",
                "robots_txt_status": "Found",
            }
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Error crawling website: {e}"}