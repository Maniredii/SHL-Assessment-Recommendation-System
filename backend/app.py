from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import re
import logging
from typing import List, Dict, Tuple
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple CORS configuration
CORS(app, 
     resources={
         r"/*": {
             "origins": ["https://shl-assessment-nine.vercel.app"],
             "methods": ["GET", "POST", "OPTIONS"],
             "allow_headers": ["Content-Type"],
             "supports_credentials": False
         }
     })

# Error handler for all exceptions
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"An error occurred: {str(error)}")
    return jsonify({
        "error": "An internal server error occurred. Please try again."
    }), 500

# Update the base URL for all tests to point to the product catalog
BASE_CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

# Comprehensive database of SHL tests
SHL_TESTS = [
    {
        "name": "OPQ32",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Personality questionnaire measuring 32 characteristics for workplace behavior and preferences",
        "keywords": ["personality", "leadership", "behavior", "traits", "character", "management", "workplace behavior"]
    },
    {
        "name": "Verify G+",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Cognitive ability assessment measuring numerical, verbal, and logical reasoning abilities",
        "keywords": ["cognitive", "numerical", "verbal", "logical", "reasoning", "aptitude", "problem solving"]
    },
    {
        "name": "Verify Numerical",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Assessment focusing on numerical reasoning and data interpretation skills",
        "keywords": ["numerical", "mathematics", "data", "analysis", "quantitative", "calculations"]
    },
    {
        "name": "Verify Verbal",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Assessment of verbal reasoning and comprehension abilities",
        "keywords": ["verbal", "language", "comprehension", "communication", "reading"]
    },
    {
        "name": "Verify Mechanical",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Tests understanding of mechanical concepts and physical principles",
        "keywords": ["mechanical", "engineering", "technical", "physics", "machinery"]
    },
    {
        "name": "Coding Pro",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Technical assessment for software developers testing coding skills and problem-solving",
        "keywords": ["programming", "coding", "software", "development", "technical", "IT"]
    },
    {
        "name": "Sales Assessment",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Comprehensive assessment for sales roles measuring sales aptitude and skills",
        "keywords": ["sales", "customer service", "business development", "negotiation"]
    },
    {
        "name": "Call Center Assessment",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Assessment for contact center roles measuring customer service skills",
        "keywords": ["customer service", "call center", "communication", "support"]
    },
    {
        "name": "Workplace Personality Inventory",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Measures work-related personality traits and behavioral preferences",
        "keywords": ["personality", "workplace", "behavior", "traits", "professional"]
    },
    {
        "name": "Remote Work Assessment",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Evaluates capabilities and preferences for remote work environments",
        "keywords": ["remote work", "virtual", "work from home", "distributed teams"]
    },
    {
        "name": "Leadership Assessment",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Comprehensive assessment of leadership potential and capabilities",
        "keywords": ["leadership", "management", "executive", "strategic thinking"]
    },
    {
        "name": "Graduate Assessment",
        "url": BASE_CATALOG_URL,
        "remote_testing": True,
        "adaptive_irt": True,
        "description": "Assessment suite designed for graduate recruitment and development",
        "keywords": ["graduate", "entry level", "campus recruitment", "early career"]
    }
]

def clean_text(text):
    # Remove special characters and convert to lowercase
    return re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get text from paragraphs, headings, and list items
        text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
        return ' '.join([elem.text.strip() for elem in text_elements])
    except Exception as e:
        logger.error(f"Error extracting text from URL: {str(e)}")
        return None

def calculate_relevance_score(query_terms: List[str], test: Dict) -> float:
    """Calculate relevance score using keyword and description matching."""
    score = 0.0
    test_text = clean_text(test['description'] + ' ' + ' '.join(test['keywords']) + ' ' + test['name'])
    
    # Exact keyword matches (50% weight)
    keyword_matches = sum(clean_text(keyword) in query_terms for keyword in test['keywords'])
    score += (keyword_matches / len(test['keywords'])) * 0.5
    
    # Partial matches in query terms (30% weight)
    term_matches = 0
    for term in query_terms:
        if len(term) > 3:
            if term in test_text:
                term_matches += 1
            # Check for word stems
            if any(keyword for keyword in test['keywords'] if keyword.startswith(term)):
                term_matches += 0.5
    score += (term_matches / len(query_terms)) * 0.3
    
    # Name match bonus (20% weight)
    if any(term in clean_text(test['name']) for term in query_terms):
        score += 0.2
    
    return score

def find_relevant_tests(query, max_results=10):
    query = clean_text(query)
    query_terms = query.split()
    relevant_tests = []
    
    for test in SHL_TESTS:
        score = calculate_relevance_score(query_terms, test)
        
        if score > 0:
            test_copy = test.copy()
            test_copy['relevance_score'] = float(score)
            relevant_tests.append(test_copy)
    
    # Sort by relevance score
    relevant_tests.sort(key=lambda x: x['relevance_score'], reverse=True)
    recommended = relevant_tests[:max_results]
    
    return {
        'recommendations': recommended,
        'message': f'Found {len(recommended)} relevant tests.'
    }

@app.route('/', methods=['GET', 'OPTIONS'])
def home():
    return jsonify({
        'status': 'ok',
        'message': 'SHL Test Recommender API is running'
    })

@app.route('/recommend', methods=['POST', 'OPTIONS'])
def recommend_tests():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers['Access-Control-Allow-Origin'] = 'https://shl-assessment-nine.vercel.app'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 200
        
    try:
        logger.debug(f"Received request: {request.data}")
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        query = data.get('query', '').strip()
        url = data.get('url', '').strip()
        
        if not query and not url:
            return jsonify({'error': 'Please provide either a query or URL'}), 400
        
        if url:
            text = extract_text_from_url(url)
            if text:
                query = text
            else:
                return jsonify({'error': 'Could not extract text from URL'}), 400
        
        results = find_relevant_tests(query)
        
        if not results['recommendations']:
            return jsonify({
                'recommendations': [],
                'message': 'No matching tests found. Try different search terms.'
            })
        else:
            return jsonify({
                'recommendations': results['recommendations'],
                'message': f'Found {len(results["recommendations"])} relevant tests.'
            })
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

if __name__ == '__main__':
    logger.info("Starting SHL Test Recommender API...")
    try:
        # Use environment variable for port with fallback to 10000
        port = int(os.environ.get('PORT', 10000))
        # In production, bind to all interfaces
        app.run(host='0.0.0.0', port=port)
        logger.info(f"Server started successfully on port {port}")
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        exit(1) 