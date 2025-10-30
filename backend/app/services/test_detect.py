from crawler import detect_platform
from bs4 import BeautifulSoup
import requests

def test_detection(url):
    print(f"\nTesting URL: {url}")
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        platform_info = detect_platform(soup, str(soup), url)
        print("\nPlatform Detection Results:")
        print("-" * 30)
        print(f"CMS: {platform_info['cms']}")
        print(f"Framework: {platform_info['framework']}")
        print(f"Hosting: {platform_info['hosting']}")
        print("\nTechnologies:")
        for tech in platform_info['technologies']:
            print(f"- {tech}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

# Test with WordPress
test_detection("https://wordpress.org")
# Test with a known React site
test_detection("https://reactjs.org")