# backend/app/services/crawler.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from seo_scorer import SEOScorer # Remove the leading dot
import time
import re
from collections import Counter
from typing import Dict, List, Any, Optional
import os
import json
import hashlib
from datetime import datetime, timedelta

# Persistent requests session to reuse connections
SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})

# Simple file cache directory
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '.cache')
os.makedirs(CACHE_DIR, exist_ok=True)

def _cache_path_for_url(url: str) -> str:
    key = hashlib.md5(url.encode('utf-8')).hexdigest()
    return os.path.join(CACHE_DIR, f"{key}.json")

def _load_cache(url: str, ttl_seconds: int) -> Optional[dict]:
    path = _cache_path_for_url(url)
    if not os.path.exists(path):
        return None
    try:
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        if datetime.now() - mtime > timedelta(seconds=ttl_seconds):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def _save_cache(url: str, data: dict) -> None:
    path = _cache_path_for_url(url)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception:
        pass

def detect_platform(soup: BeautifulSoup, html_content: str, url: str) -> Dict[str, Any]:
    """
    Detects the CMS platform, hosting service, and other technologies used by the website.
    """
    platform_data = {
        "cms": "Unknown",
        "hosting": "Unknown",
        "framework": "Unknown",
        "technologies": [],
        "server": "Unknown",
        "cdn": "Unknown"
    }
    
    # Convert HTML content to lowercase for case-insensitive matching
    html_lower = html_content.lower()
    
    # CMS Detection with version if available
    cms_patterns = {
        'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
        'Shopify': ['shopify', '.myshopify.com'],
        'Wix': ['wix-viewer', 'wixsite.com', '_wixCss', '_wixJs'],
        'Squarespace': ['squarespace', 'static1.squarespace'],
        'Webflow': ['webflow', '.webflow.com', 'webflow.js'],
        'Drupal': ['drupal', 'sites/all', 'drupal.js'],
        'Joomla': ['joomla', '/administrator/', 'mosConfig'],
        'Ghost': ['ghost.io', 'ghost-theme', 'ghost-foot'],
        'Medium': ['medium.com', 'cdn-client.medium.com'],
        'HubSpot': ['hubspot', 'hs-scripts', 'hstc.'],
        'Magento': ['magento', 'mage/', '/skin/frontend/'],
        'PrestaShop': ['prestashop', '/modules/'],
        'OpenCart': ['opencart', 'route=product'],
        'BigCommerce': ['bigcommerce', '.mybigcommerce.com'],
        'Salesforce Commerce': ['demandware.', 'commerce-cloud']
    }
    # Detect CMS by checking patterns; require at least one pattern match
    for cms_name, patterns in cms_patterns.items():
        if any(p in html_lower for p in patterns):
            platform_data["cms"] = cms_name
            break
    
    # Framework detection
    frameworks = {
        'react': ['react.js', 'reactjs', 'react-dom'],
        'angular': ['ng-', 'angular.js', 'angular/'],
        'vue': ['vue.js', 'vuejs'],
        'bootstrap': ['bootstrap.css', 'bootstrap.min.css'],
        'jquery': ['jquery.js', 'jquery.min.js'],
        'next.js': ['__next', '_next/static'],
        'gatsby': ['gatsby-', '/page-data/'],
        'tailwind': ['tailwind.css', 'tailwindcss']
    }
    
    detected_frameworks = []
    for framework, indicators in frameworks.items():
        if any(indicator in html_lower for indicator in indicators):
            detected_frameworks.append(framework)
    
    if detected_frameworks:
        platform_data["framework"] = ", ".join(detected_frameworks)
    
    # Hosting detection
    hosting_indicators = {
        'Netlify': ['netlify.app', 'netlify.com'],
        'Vercel': ['vercel.app', 'vercel.com'],
        'GitHub Pages': ['github.io'],
        'AWS': ['amazonaws.com'],
        'Heroku': ['herokuapp.com'],
        'Firebase': ['firebaseapp.com'],
        'Azure': ['azurewebsites.net'],
        'DigitalOcean': ['digitaloceanspaces.com'],
    }
    
    for host, indicators in hosting_indicators.items():
        if any(indicator in url.lower() for indicator in indicators):
            platform_data["hosting"] = host
            break
    
    # Technology detection
    meta_generator = soup.find('meta', attrs={'name': 'generator'})
    if meta_generator and meta_generator.get('content'):
        platform_data["technologies"].append(meta_generator['content'])
    
    # Additional technology detection
    common_technologies = {
        'Google Analytics': ['ga.js', 'analytics.js', 'gtag'],
        'Google Tag Manager': ['gtm.js'],
        'Facebook Pixel': ['connect.facebook.net'],
        'Cloudflare': ['cloudflare'],
        'reCAPTCHA': ['recaptcha'],
        'Font Awesome': ['font-awesome'],
        'Google Fonts': ['fonts.googleapis.com'],
    }
    
    for tech, indicators in common_technologies.items():
        if any(indicator in html_lower for indicator in indicators):
            platform_data["technologies"].append(tech)
    
    return platform_data

def analyze_content_context(text: str, title: str, description: str) -> Dict[str, List[str]]:
    """
    Analyzes the content to identify business context, main topics, and target audience.
    """
    # Combine all text for analysis
    all_text = f"{title} {description} {text}".lower()
    
    # Common business category indicators
    business_indicators = {
        'consulting': ['consulting', 'consultant', 'advisory', 'strategy', 'solutions'],
        'technology': ['software', 'technology', 'digital', 'it ', 'tech'],
        'legal': ['law', 'legal', 'attorney', 'lawyer', 'firm'],
        'healthcare': ['health', 'medical', 'healthcare', 'clinic', 'hospital'],
        'education': ['education', 'training', 'learning', 'course', 'school'],
        'ecommerce': ['shop', 'store', 'product', 'buy', 'purchase'],
        'finance': ['financial', 'finance', 'investment', 'banking', 'insurance'],
        'marketing': ['marketing', 'advertising', 'media', 'brand', 'digital'],
        'real_estate': ['real estate', 'property', 'housing', 'realty', 'mortgage']
    }
    
    # Detect business category
    category_scores = {}
    for category, terms in business_indicators.items():
        score = sum(1 for term in terms if term in all_text)
        category_scores[category] = score
    
    main_category = max(category_scores.items(), key=lambda x: x[1])[0]
    
    # Extract potential service offerings based on category
    services = []
    words = all_text.split()
    word_pairs = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    
    # Look for service-related phrases
    service_indicators = [
        r'we (offer|provide|deliver|specialize in)',
        r'our (services|solutions|products|expertise)',
        r'specialized in',
        r'expert in',
        r'consulting for'
    ]
    
    for pattern in service_indicators:
        matches = re.finditer(pattern, all_text)
        for match in matches:
            # Get the text after the match
            start = match.end()
            end = start + 100  # Look at next 100 characters
            service_text = all_text[start:end].split('.')[0]  # Get first sentence
            if service_text:
                services.append(service_text.strip())
    
    # Identify main topics
    # Remove common words and get word frequency
    common_words = {'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    words = [w for w in re.findall(r'\w+', all_text) if w not in common_words and len(w) > 3]
    word_freq = Counter(words).most_common(10)
    main_topics = [word for word, _ in word_freq]
    
    # Detect target audience
    audience_indicators = {
        'businesses': ['business', 'company', 'corporate', 'enterprise', 'organization'],
        'consumers': ['individual', 'personal', 'consumer', 'customer', 'user'],
        'professionals': ['professional', 'expert', 'specialist', 'practitioner'],
        'students': ['student', 'learner', 'education', 'academic'],
    }
    
    audience = []
    for audience_type, indicators in audience_indicators.items():
        if any(indicator in all_text for indicator in indicators):
            audience.append(audience_type)
    
    return {
        "main_topics": main_topics,
        "services": services[:5],  # Top 5 services
        "audience": audience,
        "business_category": main_category
    }

def crawl_website_data(url: str, fast: bool = False, cache_ttl: int = 300) -> dict:
    """
    Crawls a URL to extract SEO data and calculate SEO scores.

    Parameters:
      - url: website to crawl
      - fast: when True, performs a lightweight, faster analysis (shorter timeouts, limited parsing)
      - cache_ttl: seconds to cache the result (0 to disable caching)
    """
    try:
        # Check cache first
        if cache_ttl > 0 and not fast:
            cached = _load_cache(url, cache_ttl)
            if cached:
                cached['_from_cache'] = True
                return cached

        # Record start time for actual load time calculation
        start_time = time.time()
        timeout = 6 if fast else 10
        response = SESSION.get(url, timeout=timeout)
        response.raise_for_status()

        # Calculate actual load time
        load_time = time.time() - start_time

        content = response.content
        if fast and len(content) > 200_000:
            content = content[:200_000]

        soup = BeautifulSoup(content, 'html.parser')

        # Enhanced SEO data extraction (lightweight where possible)
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else "N/A"

        # Meta tags analysis
        meta_description = soup.find('meta', attrs={'name': 'description'})
        if not meta_description:
            meta_description = soup.find('meta', attrs={'property': 'og:description'})
        description = meta_description['content'].strip() if meta_description and meta_description.get('content') else "N/A"

        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        robots_content = meta_robots['content'] if meta_robots else "index, follow"

        # Headings analysis (limit counts to reduce parsing time)
        headings = {
            'h1': [h.text.strip() for h in soup.find_all('h1')[:2]],
            'h2': [h.text.strip() for h in soup.find_all('h2')[:5]],
            'h3': [h.text.strip() for h in soup.find_all('h3')[:5]]
        }

        # Link analysis
        links = soup.find_all('a', href=True)
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        internal_links = [l for l in links if domain in l.get('href', '') or l.get('href', '').startswith('/')]
        external_links = [l for l in links if l not in internal_links]

        # Images analysis (limit search in fast mode)
        images = soup.find_all('img') if not fast else soup.find_all('img')[:40]
        images_without_alt = [img for img in images if not img.get('alt')]

        # Structured data detection
        structured_data = bool(soup.find_all('script', {'type': 'application/ld+json'}))

        # Mobile viewport check
        has_viewport = bool(soup.find('meta', attrs={'name': 'viewport'}))

        # Extract main text content; prefer <main> or <article> where available
        main_candidate = soup.find('main') or soup.find('article') or soup.find('body')
        if main_candidate:
            text_content = main_candidate.get_text(separator=' ', strip=True)
        else:
            text_content = ' '.join([p.text for p in soup.find_all(['p', 'li', 'h1', 'h2', 'h3'])])
        if fast:
            text_content = text_content[:1000]

        # Extract service/product pages (skip heavy link scanning in fast mode)
        service_pages = []
        if not fast:
            for link in internal_links:
                href = link.get('href', '').lower()
                text = link.text.strip().lower()
                if any(term in href or term in text for term in ['service', 'product', 'solution', 'consulting', 'about']):
                    service_pages.append({
                        'url': href,
                        'text': link.text.strip()
                    })

        # Analyze main topics and industry terms
        content_analysis = analyze_content_context(text_content, title, description)

        # Detect platform and technologies
        platform_info = detect_platform(soup, str(soup), url)

        # Collect crawled data
        crawled_data = {
            "url": url,
            "domain": domain,
            "platform_info": platform_info,
            "html_head_data": {
                "title": title,
                "meta_description": description,
                "robots_directive": robots_content
            },
            "on_page_elements": {
                "headings": headings,
                "internal_links": len(internal_links),
                "external_links": len(external_links),
                "images": len(images),
                "images_without_alt": len(images_without_alt),
                "service_pages": service_pages
            },
            "content_analysis": content_analysis,
            "extracted_text": text_content[:1000],  # First 1000 characters for context
            "simulated_metrics": {
                "page_load_time_s": round(load_time, 2),
                "mobile_friendly": "Yes" if has_viewport else "No",
                "structured_data_present": "Yes" if structured_data else "No (Missing)",
                "robots_txt_status": "Found"  # This would need actual checking in production
            },
            # Avoid storing huge raw HTML in fast mode
            "raw_html": (str(soup) if not fast else None)
        }

        # Calculate SEO scores
        scorer = SEOScorer(crawled_data)
        seo_scores = scorer.calculate_scores()

        # Combine crawled data with scores
        crawled_data.update({
            "seo_scores": seo_scores["component_scores"],
            "overall_seo_score": seo_scores["overall_score"],
            "recommendations": seo_scores["recommendations"]
        })

        # Save to cache for faster subsequent runs (skip caching in fast mode)
        if cache_ttl > 0 and not fast:
            try:
                _save_cache(url, crawled_data)
            except Exception:
                pass

        return crawled_data

    except requests.exceptions.RequestException as e:
        return {"error": f"Error crawling website: {e}"}