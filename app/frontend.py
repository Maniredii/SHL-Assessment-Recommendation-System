# -*- coding: utf-8 -*-

import streamlit as st
import requests
from typing import List, Dict, Any
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scraper import SHLScraper

# Set page config
st.set_page_config(
    page_title="SHL Assessment Catalog",
    page_icon="📊",
    layout="wide"
)

# Initialize scraper
scraper = SHLScraper()

def safe_get(dictionary: Dict, key: str, default: Any = "N/A") -> Any:
    """Safely get a value from a dictionary with a default if the key doesn't exist."""
    return dictionary.get(key, default)

def main():
    st.title("SHL Assessment Catalog")
    
    # Load assessments
    assessments = scraper.load_assessments()
    if not assessments:
        with st.spinner("Loading assessments..."):
            assessments = scraper.scrape_assessments()
    
    # Sidebar filters
    st.sidebar.title("Filters")
    
    # Job Family filter
    job_family = st.sidebar.selectbox(
        "Job Family",
        ["All", "Business", "Clerical", "Contact Center", "Customer Service", 
         "Information Technology", "Safety", "Sales"]
    )
    
    # Job Level filter
    job_level = st.sidebar.selectbox(
        "Job Level",
        ["All", "Director", "Entry-Level", "Executive", "Front Line Manager",
         "General Population", "Graduate", "Manager", "Mid-Professional",
         "Professional Individual Contributor", "Supervisor"]
    )
    
    # Industry filter
    industry = st.sidebar.selectbox(
        "Industry",
        ["All", "Banking/Finance", "Healthcare", "Hospitality", "Insurance",
         "Manufacturing", "Oil & Gas", "Retail", "Telecommunications"]
    )
    
    # Test Type multiselect
    test_types = st.sidebar.multiselect(
        "Test Types",
        ["A - Ability & Aptitude", 
         "B - Biodata & Situational Judgement",
         "C - Competencies",
         "D - Development & 360",
         "E - Assessment Exercises",
         "K - Knowledge & Skills",
         "P - Personality & Behavior",
         "S - Simulations"]
    )
    
    # Remote Testing filter
    remote_only = st.sidebar.checkbox("Show only remote testing available")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Search box
        search_query = st.text_input("Search assessments by keyword")
    
    # Filter assessments
    filtered_assessments = scraper.filter_assessments(
        assessments,
        search_query=search_query,
        job_family=job_family,
        job_level=job_level,
        industry=industry,
        test_types=test_types,
        remote_only=remote_only
    )
    
    # Display number of results
    st.write(f"Found {len(filtered_assessments)} assessments")
    
    # Create columns for assessment cards
    if filtered_assessments:
        cols = st.columns(3)
        for idx, assessment in enumerate(filtered_assessments):
            with cols[idx % 3]:
                with st.expander(safe_get(assessment, "name", "Unnamed Assessment"), expanded=True):
                    st.markdown(f"**Test Types:** {safe_get(assessment, 'test_types')}")
                    st.markdown(f"**Job Family:** {safe_get(assessment, 'job_family')}")
                    st.markdown(f"**Job Level:** {safe_get(assessment, 'job_level')}")
                    st.markdown(f"**Industry:** {safe_get(assessment, 'industry')}")
                    st.markdown(f"**Remote Testing:** {'Yes' if safe_get(assessment, 'remote_testing', False) else 'No'}")
                    st.markdown(f"**Adaptive/IRT:** {'Yes' if safe_get(assessment, 'adaptive_irt', False) else 'No'}")
                    st.markdown(f"**Description:** {safe_get(assessment, 'description')}")
    else:
        st.info("No assessments found matching your criteria. Try adjusting your filters.")
    
    # Add legend for test types
    st.sidebar.markdown("""
    ### Test Type Legend
    - A: Ability & Aptitude
    - B: Biodata & Situational Judgement
    - C: Competencies
    - D: Development & 360
    - E: Assessment Exercises
    - K: Knowledge & Skills
    - P: Personality & Behavior
    - S: Simulations
    """)

if __name__ == "__main__":
    main()
