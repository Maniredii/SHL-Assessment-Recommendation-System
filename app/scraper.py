import requests
from bs4 import BeautifulSoup
import json
import os
from typing import List, Dict, Any
import time

class SHLScraper:
    def __init__(self):
        self.base_url = "https://www.shl.com/solutions/products/product-catalog/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.data_dir = "data"
        self.ensure_data_dir()

    def ensure_data_dir(self):
        """Ensure the data directory exists."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def scrape_assessments(self) -> List[Dict[str, Any]]:
        """Scrape assessment data from SHL product catalog."""
        try:
            # For now, return sample data since we can't directly scrape the website
            assessments = [
                {
                    "name": "Account Manager Solution",
                    "test_types": "C P A B",
                    "remote_testing": True,
                    "adaptive_irt": False,
                    "description": "Comprehensive assessment solution for Account Manager roles",
                    "job_family": "Sales",
                    "job_level": "Professional Individual Contributor",
                    "industry": "All"
                },
                {
                    "name": "Administrative Professional - Short Form",
                    "test_types": "A K P",
                    "remote_testing": True,
                    "adaptive_irt": True,
                    "description": "Quick assessment for Administrative Professional positions",
                    "job_family": "Clerical",
                    "job_level": "Entry-Level",
                    "industry": "All"
                },
                {
                    "name": "Agency Manager Solution",
                    "test_types": "A B P S",
                    "remote_testing": True,
                    "adaptive_irt": False,
                    "description": "Complete assessment package for Agency Manager positions",
                    "job_family": "Business",
                    "job_level": "Manager",
                    "industry": "Insurance"
                },
                {
                    "name": "Bank Collections Agent - Short Form",
                    "test_types": "A B P",
                    "remote_testing": True,
                    "adaptive_irt": True,
                    "description": "Focused assessment for Bank Collections Agent roles",
                    "job_family": "Customer Service",
                    "job_level": "Entry-Level",
                    "industry": "Banking/Finance"
                },
                {
                    "name": "IT Developer Assessment",
                    "test_types": "K S A",
                    "remote_testing": True,
                    "adaptive_irt": True,
                    "description": "Technical and aptitude assessment for software developers",
                    "job_family": "Information Technology",
                    "job_level": "Professional Individual Contributor",
                    "industry": "All"
                },
                {
                    "name": "Sales Manager Solution",
                    "test_types": "C P B D",
                    "remote_testing": True,
                    "adaptive_irt": False,
                    "description": "Comprehensive assessment for Sales Manager positions",
                    "job_family": "Sales",
                    "job_level": "Manager",
                    "industry": "All"
                }
            ]
            
            # Save to file
            self.save_assessments(assessments)
            return assessments
            
        except Exception as e:
            print(f"Error scraping assessments: {str(e)}")
            return []

    def get_assessment_description(self, url: str) -> str:
        """Get detailed description for an assessment."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            description = ""
            
            # Find description content
            description_div = soup.find('div', class_='description')
            if description_div:
                description = description_div.text.strip()
            
            return description
            
        except Exception as e:
            print(f"Error getting description for {url}: {str(e)}")
            return ""

    def save_assessments(self, assessments: List[Dict[str, Any]]):
        """Save assessments to a JSON file."""
        file_path = os.path.join(self.data_dir, "assessments.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(assessments, f, indent=2, ensure_ascii=False)

    def load_assessments(self) -> List[Dict[str, Any]]:
        """Load assessments from the JSON file."""
        file_path = os.path.join(self.data_dir, "assessments.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def filter_assessments(
        self,
        assessments: List[Dict[str, Any]],
        search_query: str = "",
        job_family: str = "All",
        job_level: str = "All",
        industry: str = "All",
        test_types: List[str] = None,
        remote_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Filter assessments based on criteria."""
        filtered = assessments

        # Apply search query
        if search_query:
            filtered = [
                a for a in filtered
                if search_query.lower() in a.get("name", "").lower() or
                   search_query.lower() in a.get("description", "").lower()
            ]

        # Apply job family filter
        if job_family != "All":
            filtered = [
                a for a in filtered 
                if a.get("job_family", "").lower() == job_family.lower()
            ]

        # Apply job level filter
        if job_level != "All":
            filtered = [
                a for a in filtered 
                if a.get("job_level", "").lower() == job_level.lower()
            ]

        # Apply industry filter
        if industry != "All":
            filtered = [
                a for a in filtered 
                if a.get("industry", "").lower() == industry.lower()
            ]

        # Apply test types filter
        if test_types:
            filtered = [
                a for a in filtered
                if any(t.split(" - ")[0] in a.get("test_types", "") for t in test_types)
            ]

        # Apply remote testing filter
        if remote_only:
            filtered = [
                a for a in filtered 
                if a.get("remote_testing", False)
            ]

        return filtered 