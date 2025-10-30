import requests
import json

def test_seo_audit(url):
    print(f"\nTesting URL: {url}")
    try:
        response = requests.post(
            "http://localhost:8000/analyze",
            json={"url": url}
        )
        data = response.json()
        
        # Extract platform info
        platform_info = data.get("platform_info", {})
        print("\nPlatform Detection Results:")
        print("-" * 30)
        print(f"CMS: {platform_info.get('cms', 'Unknown')}")
        print(f"Framework: {platform_info.get('framework', 'Unknown')}")
        print(f"Hosting: {platform_info.get('hosting', 'Unknown')}")
        print("\nTechnologies:")
        for tech in platform_info.get("technologies", []):
            print(f"- {tech}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

# Test with different types of websites
test_urls = [
    "https://www.shopify.com",          # Shopify
    "https://www.wix.com",              # Wix
    "https://wordpress.org",            # WordPress
    "https://www.squarespace.com",      # Squarespace
    "https://vercel.com",               # Vercel (Next.js)
    "https://www.netlify.com",          # Netlify
]

for url in test_urls:
    test_seo_audit(url)