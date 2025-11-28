import json
import csv
import os
from setup import exa_client

def perform_search(query, **options):
    """Perform a search with Exa API"""
    return exa_client.search(query, **options)

def search_and_save_json(query, output_path="search_results.json", **options):
    """Search and save results as JSON"""
    results = perform_search(query, **options)
    
    # Convert to serializable format
    serializable_results = []
    for result in results.results:
        serializable_results.append({
            "title": result.title,
            "url": result.url,
            "id": result.id,
            "published_date": result.published_date,
            "score": result.score
        })
    
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    # Save to JSON file
    with open(output_path, "w") as f:
        json.dump(serializable_results, f, indent=2)
    
    return results