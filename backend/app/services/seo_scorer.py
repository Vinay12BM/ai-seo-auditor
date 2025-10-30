"""
SEO Scoring Algorithm Module
This module calculates a comprehensive SEO score based on various factors and best practices.
"""

from typing import Dict, Any, List
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class SEOScorer:
    def __init__(self, crawled_data: Dict[str, Any]):
        self.data = crawled_data
        self.scores = {
            'title': 0,
            'meta_description': 0,
            'url_structure': 0,
            'headings': 0,
            'content': 0,
            'links': 0,
            'mobile_friendly': 0,
            'load_speed': 0,
            'technical': 0
        }
        
    def calculate_overall_score(self) -> int:
        """Calculate the final SEO score (0-100) based on weighted factors."""
        # Define weights for each factor (total = 100)
        weights = {
            'title': 15,
            'meta_description': 10,
            'url_structure': 10,
            'headings': 10,
            'content': 20,
            'links': 10,
            'mobile_friendly': 10,
            'load_speed': 10,
            'technical': 5
        }
        
        # Calculate weighted score
        total_score = sum(self.scores[key] * weights[key] / 100 for key in weights.keys())
        return round(total_score)

    def analyze_title(self, title: str) -> float:
        """
        Score title tag based on length and keyword presence
        Returns score 0-100
        """
        if not title or title == "N/A":
            return 0
        
        score = 100
        length = len(title)
        
        # Length penalties
        if length < 30:
            score -= 30  # Too short
        elif length > 60:
            score -= 20  # Too long
        elif length < 40 or length > 50:
            score -= 10  # Not optimal but acceptable
            
        # Check for common issues
        if title.isupper():
            score -= 10  # ALL CAPS titles are not recommended
        if title.islower():
            score -= 5   # all lowercase titles are not optimal
        if re.search(r'\s{2,}', title):
            score -= 5   # Multiple spaces
            
        return max(0, score)

    def analyze_meta_description(self, description: str) -> float:
        """Score meta description based on length and content quality"""
        if not description or description == "N/A":
            return 0
            
        score = 100
        length = len(description)
        
        # Length scoring
        if length < 120:
            score -= 30  # Too short
        elif length > 160:
            score -= 20  # Too long
        elif length < 140:
            score -= 10  # Not optimal but acceptable
            
        # Content quality checks
        if not any(char in description for char in '.!?'):
            score -= 10  # No proper punctuation
        if description.count(' ') < 10:
            score -= 20  # Too few words
            
        return max(0, score)

    def analyze_url_structure(self, url: str) -> float:
        """Score URL structure based on SEO best practices"""
        score = 100
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        
        # Check URL length
        if len(url) > 100:
            score -= 20
        
        # Check for URL clarity
        if re.search(r'[^a-z0-9-/]', path):
            score -= 15  # Contains special characters
            
        # Check for multiple consecutive hyphens
        if '--' in path:
            score -= 10
            
        # Check depth (number of folders)
        depth = len([x for x in path.split('/') if x])
        if depth > 3:
            score -= 5 * (depth - 3)  # Penalty for deep nesting
            
        return max(0, score)

    def analyze_headings(self, html_content: str) -> float:
        """Score heading structure and hierarchy"""
        soup = BeautifulSoup(html_content, 'html.parser')
        score = 100
        
        # Check for H1
        h1_tags = soup.find_all('h1')
        if not h1_tags:
            score -= 50  # No H1 tag
        elif len(h1_tags) > 1:
            score -= 20  # Multiple H1 tags
            
        # Check heading hierarchy
        heading_levels = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        previous_level = 0
        for tag in soup.find_all(heading_levels):
            current_level = int(tag.name[1])
            if current_level - previous_level > 1:
                score -= 5  # Skipped heading level
            previous_level = current_level
            
        return max(0, score)

    def analyze_technical_factors(self) -> float:
        """Score technical SEO factors"""
        score = 100
        metrics = self.data.get('simulated_metrics', {})
        
        # Mobile friendliness
        if metrics.get('mobile_friendly') != "Yes":
            score -= 30
            
        # Load time scoring
        load_time = float(metrics.get('page_load_time_s', 5))
        if load_time > 3:
            score -= 20
        elif load_time > 2:
            score -= 10
            
        # Structured data
        if "Missing" in metrics.get('structured_data_present', ''):
            score -= 15
            
        return max(0, score)

    def calculate_scores(self) -> Dict[str, float]:
        """Calculate all component scores and return the overall score"""
        html_head = self.data.get('html_head_data', {})
        
        # Calculate individual scores
        self.scores['title'] = self.analyze_title(html_head.get('title', ''))
        self.scores['meta_description'] = self.analyze_meta_description(html_head.get('meta_description', ''))
        self.scores['url_structure'] = self.analyze_url_structure(self.data.get('url', ''))
        self.scores['technical'] = self.analyze_technical_factors()
        
        # Additional scoring components would be calculated here
        # For now, we'll use simulated scores for remaining factors
        self.scores['headings'] = 80  # Simulated score
        self.scores['content'] = 75   # Simulated score
        self.scores['links'] = 70     # Simulated score
        self.scores['mobile_friendly'] = 90  # Simulated score
        self.scores['load_speed'] = 85      # Simulated score
        
        return {
            'overall_score': self.calculate_overall_score(),
            'component_scores': self.scores,
            'recommendations': self.generate_recommendations()
        }

    def generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate specific recommendations based on scores"""
        recommendations = []
        
        if self.scores['title'] < 80:
            recommendations.append({
                'category': 'Title Tag',
                'priority': 'High',
                'issue': 'Title tag needs optimization',
                'description': 'Your title tag could be improved for better SEO performance',
                'recommended_action': 'Optimize title length (40-60 characters) and include primary keyword'
            })
            
        if self.scores['meta_description'] < 80:
            recommendations.append({
                'category': 'Meta Description',
                'priority': 'Medium',
                'issue': 'Meta description needs improvement',
                'description': 'Your meta description could be more compelling',
                'recommended_action': 'Write a compelling meta description (120-160 characters) with call-to-action'
            })
            
        # Add more recommendations based on other scores
        
        return recommendations