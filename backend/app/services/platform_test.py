# C:\Users\Vinay bm\OneDrive\Desktop\ai-seo-auditor\backend\app\services\platform_test.py

import requests
from bs4 import BeautifulSoup
from crawler import detect_platform # Import the function from crawler.py
from typing import Dict, Any # For type hinting

# Define a requests session with a user agent (important for some sites)
SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})

def print_results(url: str, results: Dict[str, Any]) -> None:
    """Helper function to print the detected platform information."""
    print(f"\nPlatform Detection Results for {url}:")
    print("--------------------------------------------------")
    print(f"CMS Platform: {results.get('cms', 'Unknown')}")
    print(f"Hosting Provider: {results.get('hosting', 'Unknown')}")
    print(f"Framework: {results.get('framework', 'Unknown')}")
    print(f"Server: {results.get('server', 'Unknown')}")
    print(f"CDN: {results.get('cdn', 'Unknown')}")
    
    technologies = results.get('technologies', [])
    if technologies:
        print("\nDetected Technologies:")
        for tech in technologies:
            print(f"  - {tech}")
    else:
        print("\nNo specific technologies detected.")
    print("-" * 50)

# --- Main script execution ---
if __name__ == "__main__":
    url_to_test = input("Enter the website URL to test (e.g., https://example.com): ").strip()

    if not url_to_test.startswith(('http://', 'https://')):
        print(f"Error: Invalid URL '{url_to_test}'. Please include http:// or https://")
    else:
        print(f"\nTesting URL: {url_to_test}")
        try:
            # --- Make the HTTP request ---
            response = SESSION.get(url_to_test, timeout=15) # Increased timeout
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            
            # --- Parse the HTML ---
            soup = BeautifulSoup(response.content, 'html.parser')
            html_content = response.text # Use the decoded text content for analysis

            # --- Call the detection function ---
            # Pass the soup object, the raw HTML text, and the URL
            platform_results = detect_platform(soup, html_content, url_to_test) 
            
            # --- Print the results ---
            print_results(url_to_test, platform_results)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url_to_test}: {e}")
        except Exception as e:
            # Catch any other unexpected errors during parsing or detection
            print(f"An unexpected error occurred while processing {url_to_test}: {e}")