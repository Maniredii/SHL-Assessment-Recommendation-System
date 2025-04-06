#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SHL Assessment API Backend
This module provides a FastAPI-based REST API for accessing SHL assessments.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from pydantic import BaseModel
from app.scraper import SHLScraper

app = FastAPI(title="SHL Assessment API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scraper
scraper = SHLScraper()

class AssessmentResponse(BaseModel):
    name: str
    link: str
    remote_testing: str
    adaptive_irt: str
    test_types: str
    description: str

@app.get("/")
async def root():
    return {"message": "SHL Assessment API"}

@app.get("/assessments", response_model=List[AssessmentResponse])
async def get_assessments():
    """Get all assessments."""
    assessments = scraper.load_assessments()
    if not assessments:
        assessments = scraper.scrape_assessments()
    return assessments

@app.get("/assessments/search")
async def search_assessments(query: str = ""):
    """Search assessments by name."""
    assessments = scraper.load_assessments()
    if not assessments:
        assessments = scraper.scrape_assessments()
    
    if query:
        filtered = [
            a for a in assessments 
            if query.lower() in a["name"].lower()
        ]
        return filtered
    return assessments

@app.get("/assessments/filter")
async def filter_assessments(
    test_types: str = "",
    remote_only: bool = False
):
    """Filter assessments by test type and remote testing availability."""
    assessments = scraper.load_assessments()
    if not assessments:
        assessments = scraper.scrape_assessments()
    
    filtered = assessments
    
    if test_types:
        types = test_types.split(",")
        filtered = [
            a for a in filtered 
            if any(t in a["test_types"] for t in types)
        ]
    
    if remote_only:
        filtered = [
            a for a in filtered 
            if a["remote_testing"] == "Yes"
        ]
    
    return filtered

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 