#!/usr/bin/env python3
"""
Build comprehensive Forsaken City (Level 1) data by scraping wikis
"""
import os
import json
from dotenv import load_dotenv
from exa_py import Exa

# Load environment
load_dotenv()
exa = Exa(api_key=os.getenv("EXA_API_KEY"))

# URLs to scrape
URLS_TO_SCRAPE = [
    "https://celeste.ink/wiki/Forsaken_City",
    "https://celestegame.fandom.com/wiki/Chapter_1:_Forsaken_City",
    "https://www.ign.com/wikis/celeste/Chapter_1-_Forsaken_City",
]

print("="*80)
print("Building Forsaken City (Level 1) Database")
print("="*80)

# Scrape each URL
all_scraped_data = []

for url in URLS_TO_SCRAPE:
    print(f"\n📥 Scraping: {url}")
    try:
        result = exa.get_contents([url], text=True)
        if result.results:
            content = result.results[0].text
            all_scraped_data.append({
                "url": url,
                "content": content[:5000],  # First 5000 chars
                "full_length": len(content)
            })
            print(f"   ✅ Scraped {len(content)} characters")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Save raw scraped data
output_dir = "database/output"
os.makedirs(output_dir, exist_ok=True)

with open(f"{output_dir}/forsaken_city_raw_scrape.json", "w") as f:
    json.dump(all_scraped_data, f, indent=2)
    print(f"\n💾 Saved raw scrape data to: {output_dir}/forsaken_city_raw_scrape.json")

print("\n" + "="*80)
print("Raw data collection complete!")
print("="*80)
print("\nNext: Review the scraped data and manually structure it into the schema:")
print("  - level_id/chapter")
print("  - room_id")
print("  - difficulty")
print("  - objective")
print("  - mechanics_involved")
print("  - hint_tiers: [tier1, tier2, tier3]")
print("  - is_optional")
print("  - provenance_url")
