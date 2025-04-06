import os
import google.generativeai as genai
from typing import List, Dict
import pandas as pd
from dotenv import load_dotenv
from .scraper import SHLScraper
import json

load_dotenv()

class AssessmentRecommender:
    def __init__(self):
        self.scraper = SHLScraper()
        self.assessments_df = self.scraper.get_assessment_dataframe()
        
        # Initialize Gemini
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
        
    def process_query(self, query: str) -> Dict:
        """Process the query using Gemini to extract key requirements."""
        prompt = f"""
        Analyze this job description or query and extract key requirements:
        {query}
        
        Please identify:
        1. Required skills or competencies
        2. Desired duration (in minutes)
        3. Test type preferences (cognitive, personality, skills, behavioral)
        4. Any specific requirements (remote testing, adaptive testing)
        
        Format the response as a JSON object with these keys:
        - skills: list of required skills
        - duration: maximum duration in minutes (as integer)
        - test_types: list of preferred test types
        - requirements: list of specific requirements
        """
        
        response = self.model.generate_content(prompt)
        try:
            return json.loads(response.text)
        except:
            # Fallback if JSON parsing fails
            return {
                "skills": [],
                "duration": 60,
                "test_types": [],
                "requirements": []
            }
        
    def calculate_relevance_score(self, assessment: Dict, requirements: Dict) -> float:
        """Calculate relevance score for an assessment based on requirements."""
        score = 0.0
        
        # Check duration match
        if assessment['duration'] != "Unknown":
            try:
                duration = int(assessment['duration'].split()[0])
                if duration <= requirements['duration']:
                    score += 0.3
            except:
                pass
                
        # Check test type match
        if assessment['test_type'] != "Unknown":
            if any(test_type.lower() in assessment['test_type'].lower() 
                  for test_type in requirements['test_types']):
                score += 0.3
                
        # Check remote testing requirement
        if 'remote' in requirements['requirements'] and assessment['remote_testing']:
            score += 0.2
            
        # Check adaptive/IRT requirement
        if ('adaptive' in requirements['requirements'] or 'irt' in requirements['requirements']) and assessment['adaptive_irt']:
            score += 0.2
            
        return score
        
    def recommend_assessments(self, query: str, max_recommendations: int = 10) -> List[Dict]:
        """Recommend assessments based on the query."""
        try:
            # Process the query
            requirements = self.process_query(query)
            
            # Get all assessments
            assessments = self.scraper.load_assessments()
            
            # Calculate relevance scores
            scored_assessments = []
            for assessment in assessments:
                relevance_score = self.calculate_relevance_score(assessment, requirements)
                if relevance_score > 0:  # Only include assessments with some relevance
                    scored_assessment = assessment.copy()
                    scored_assessment['relevance_score'] = relevance_score
                    scored_assessments.append(scored_assessment)
            
            # Sort by relevance score and limit to max_recommendations
            recommendations = sorted(scored_assessments, 
                                  key=lambda x: x['relevance_score'], 
                                  reverse=True)[:max_recommendations]
            
            return recommendations
            
        except Exception as e:
            print(f"Error recommending assessments: {e}")
            return []
            
    def format_recommendations(self, recommendations: List[Dict]) -> str:
        """Format recommendations for display."""
        if not recommendations:
            return "No recommendations found."
            
        formatted = []
        for i, rec in enumerate(recommendations, 1):
            formatted.append(f"{i}. {rec['name']}")
            formatted.append(f"   URL: {rec['url']}")
            formatted.append(f"   Remote Testing: {'Yes' if rec['remote_testing'] else 'No'}")
            formatted.append(f"   Adaptive/IRT: {'Yes' if rec['adaptive_irt'] else 'No'}")
            formatted.append(f"   Duration: {rec['duration']}")
            formatted.append(f"   Test Type: {rec['test_type']}")
            formatted.append(f"   Relevance Score: {rec['relevance_score']:.2f}")
            formatted.append("")
            
        return "\n".join(formatted) 