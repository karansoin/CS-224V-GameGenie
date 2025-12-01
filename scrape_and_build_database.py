#!/usr/bin/env python3
"""
Comprehensive web scraper and database builder for Celeste Chapter 1
Scrapes multiple sources and extracts all available information
"""
import json
import re
import os
from dotenv import load_dotenv
from exa_py import Exa

# Load environment variables
load_dotenv()
exa_api_key = os.getenv("EXA_API_KEY")

if not exa_api_key:
    raise ValueError("EXA_API_KEY not found in .env file")

# Initialize Exa client
exa = Exa(api_key=exa_api_key)

print("="*80)
print("Celeste Chapter 1 - Comprehensive Web Scraper")
print("="*80)

# ============================================================================
# CONFIGURATION
# ============================================================================

# URLs to scrape (add or remove as needed)
URLS_TO_SCRAPE = [
    "https://celestegame.fandom.com/wiki/Chapter_1:_Forsaken_City",
    "https://www.ign.com/wikis/celeste/Chapter_1-_Forsaken_City",
    "https://steamcommunity.com/sharedfiles/filedetails/?id=3474899136",
    "https://www.neoseeker.com/celeste/walkthrough/Level_1_-_Forsaken_City",
    "https://www.switchaboo.com/celeste-100-strawberry-guide/",
    "https://www.trueachievements.com/game/Celeste/walkthrough/3",
]

# Scraping parameters
SUBPAGES = 3  # Number of subpages to crawl per URL
SUBPAGE_KEYWORDS = [
    "strawberry",
    "collectible",
    "guide",
    "walkthrough",
    "secret",
    "crystal heart",
    "cassette"
]

# Output files
RAW_OUTPUT = "database/raw_scraped_data.json"
FINAL_OUTPUT = "database/celeste_chapter1_database.json"


# ============================================================================
# STEP 1: SCRAPE ALL URLS
# ============================================================================

def scrape_all_sources():
    """Scrape all URLs with subpage crawling"""
    print(f"\nStep 1: Scraping {len(URLS_TO_SCRAPE)} sources...")
    print(f"  Subpages per URL: {SUBPAGES}")
    print(f"  Subpage keywords: {', '.join(SUBPAGE_KEYWORDS)}")

    all_scraped_data = []

    for i, url in enumerate(URLS_TO_SCRAPE, 1):
        print(f"\n[{i}/{len(URLS_TO_SCRAPE)}] Scraping: {url}")

        try:
            result = exa.get_contents(
                [url],
                text=True,
                subpages=SUBPAGES,
                subpage_target=SUBPAGE_KEYWORDS
            )

            # Extract content
            if result.results and len(result.results) > 0:
                content = result.results[0].text
                char_count = len(content)

                all_scraped_data.append({
                    "url": url,
                    "content": content,
                    "char_count": char_count,
                    "status": "success"
                })

                print(f"  Success! Scraped {char_count:,} characters")
            else:
                print(f"  Warning: No content returned")
                all_scraped_data.append({
                    "url": url,
                    "content": "",
                    "char_count": 0,
                    "status": "no_content"
                })

        except Exception as e:
            print(f"  Error: {e}")
            all_scraped_data.append({
                "url": url,
                "content": "",
                "char_count": 0,
                "status": f"error: {str(e)}"
            })

    # Save raw scraped data
    os.makedirs("database", exist_ok=True)
    with open(RAW_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_scraped_data, f, indent=2, ensure_ascii=False)

    total_chars = sum(d["char_count"] for d in all_scraped_data)
    successful = sum(1 for d in all_scraped_data if d["status"] == "success")

    print(f"\n  Total scraped: {total_chars:,} characters from {successful}/{len(URLS_TO_SCRAPE)} sources")
    print(f"  Saved to: {RAW_OUTPUT}")

    return all_scraped_data


# ============================================================================
# STEP 2: EXTRACT AND STRUCTURE DATA
# ============================================================================

def clean_text(text):
    """Remove invisible Unicode characters and excessive whitespace"""
    # Remove zero-width spaces and other invisible characters
    text = re.sub(r'[\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff]', '', text)
    text = text.replace('\u200e', '').replace('\u200f', '').replace('\ufeff', '')
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def extract_strawberry_info(source_content, source_url, strawberry_num):
    """Extract detailed instruction for a specific strawberry"""

    # Multiple keyword variations to search for
    search_patterns = [
        f"strawberry #{strawberry_num}",
        f"strawberry {strawberry_num}",
        f"berry #{strawberry_num}",
        f"berry {strawberry_num}",
        f"#{strawberry_num}",
    ]

    content_lower = source_content.lower()
    found_contexts = []

    for pattern in search_patterns:
        pattern_lower = pattern.lower()
        idx = content_lower.find(pattern_lower)

        if idx != -1:
            # Extract generous context around the mention
            start = max(0, idx - 300)
            end = min(len(source_content), idx + 1200)
            context = source_content[start:end]

            # Clean and store
            context = clean_text(context)
            if len(context) > 100 and context not in found_contexts:
                found_contexts.append(context)

    # Return the longest/most detailed context found
    if found_contexts:
        return max(found_contexts, key=len)

    return None


def build_structured_database(scraped_data):
    """Build structured database from scraped data"""
    print("\n\nStep 2: Building structured database...")

    database = {
        "chapter": "1",
        "chapter_name": "Forsaken_City",
        "side": "A",
        "total_strawberries": 20,
        "collectibles": []
    }

    # Process strawberries 1-20
    print("\n  Processing strawberries...")
    for strawberry_num in range(1, 21):
        print(f"    Strawberry #{strawberry_num}...", end=" ")

        collectible = {
            "collectible_id": f"strawberry_{strawberry_num}",
            "collectible_type": "strawberry",
            "collectible_number": strawberry_num,
            "section": "Start" if strawberry_num <= 6 else ("Crossing" if strawberry_num <= 15 else "Chasm"),
            "info": []
        }

        # Extract from all sources
        for source in scraped_data:
            if source["status"] != "success":
                continue

            url = source["url"]
            content = source["content"]

            instruction = extract_strawberry_info(content, url, strawberry_num)

            if instruction and len(instruction) > 50:
                collectible["info"].append({
                    "instruction": instruction,
                    "source": url
                })

        # Deduplicate
        seen = set()
        unique_info = []
        for info in collectible["info"]:
            fingerprint = info["instruction"][:100]
            if fingerprint not in seen:
                seen.add(fingerprint)
                unique_info.append(info)

        collectible["info"] = unique_info

        if collectible["info"]:
            database["collectibles"].append(collectible)
            print(f"{len(unique_info)} sources")
        else:
            print("no data found")

    # Process Crystal Heart
    print("\n  Processing Crystal Heart...", end=" ")
    crystal_heart = {
        "collectible_id": "crystal_heart",
        "collectible_type": "crystal_heart",
        "collectible_number": None,
        "section": "Crossing",
        "info": []
    }

    for source in scraped_data:
        if source["status"] != "success":
            continue

        url = source["url"]
        content = source["content"]

        if "crystal heart" in content.lower():
            idx = content.lower().find("crystal heart")
            start = max(0, idx - 500)
            end = min(len(content), idx + 1000)
            context = clean_text(content[start:end])

            if len(context) > 100:
                crystal_heart["info"].append({
                    "instruction": context,
                    "source": url
                })

    if crystal_heart["info"]:
        database["collectibles"].append(crystal_heart)
        print(f"{len(crystal_heart['info'])} sources")

    # Process Cassette Tape
    print("  Processing Cassette Tape...", end=" ")
    cassette = {
        "collectible_id": "cassette_tape",
        "collectible_type": "cassette_tape",
        "collectible_number": None,
        "section": "Chasm",
        "info": []
    }

    for source in scraped_data:
        if source["status"] != "success":
            continue

        url = source["url"]
        content = source["content"]

        if "cassette" in content.lower() or "b-side" in content.lower():
            keywords = ["cassette", "b-side"]
            for keyword in keywords:
                if keyword in content.lower():
                    idx = content.lower().find(keyword)
                    start = max(0, idx - 500)
                    end = min(len(content), idx + 1000)
                    context = clean_text(content[start:end])

                    if len(context) > 100:
                        cassette["info"].append({
                            "instruction": context,
                            "source": url
                        })
                    break

    if cassette["info"]:
        database["collectibles"].append(cassette)
        print(f"{len(cassette['info'])} sources")

    # Save final database
    with open(FINAL_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=2, ensure_ascii=False)

    # Statistics
    total_collectibles = len(database["collectibles"])
    total_info_entries = sum(len(c["info"]) for c in database["collectibles"])
    avg_sources = total_info_entries / total_collectibles if total_collectibles > 0 else 0

    print(f"\n  Total collectibles: {total_collectibles}")
    print(f"  Total info entries: {total_info_entries}")
    print(f"  Average sources per collectible: {avg_sources:.1f}")
    print(f"  Saved to: {FINAL_OUTPUT}")

    return database


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Step 1: Scrape
    scraped_data = scrape_all_sources()

    # Step 2: Build database
    database = build_structured_database(scraped_data)

    print("\n" + "="*80)
    print("Database Generation Complete!")
    print("="*80)
    print(f"\nOutput files:")
    print(f"  1. Raw scraped data: {RAW_OUTPUT}")
    print(f"  2. Final database:   {FINAL_OUTPUT}")
    print("\nReady for use!")
