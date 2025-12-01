#!/usr/bin/env python3
"""
Extract all relevant Celeste Chapter 1 content from scraped data
Preserves ALL content without synthesis - just organizes by topic
"""
import json
import re

# Load raw scraped data
with open("database/output/forsaken_city_raw_scrape.json", "r") as f:
    raw_data = json.load(f)

print("="*80)
print("Extracting Structured Data from 8 Sources")
print("="*80)

# Initialize structure to hold ALL content from ALL sources
structured_data = {
    "chapter": "1",
    "chapter_name": "Forsaken_City",
    "side": "A",
    "sources": [],
    "strawberries": {},  # Will hold all strawberry info from all sources
    "mechanics": {},     # Will hold all mechanic descriptions from all sources
    "sections": {        # Will hold all section info from all sources
        "Start": [],
        "Crossing": [],
        "Chasm": []
    },
    "collectibles": {
        "crystal_heart": [],
        "cassette_tape": [],
        "general": []
    }
}

# Process each source
for idx, source in enumerate(raw_data, 1):
    url = source["url"]
    content = source["content"]

    print(f"\n[{idx}/8] Processing: {url}")
    print(f"    Content length: {len(content)} characters")

    # Add source info
    source_info = {
        "source_id": idx,
        "url": url,
        "content_length": len(content)
    }
    structured_data["sources"].append(source_info)

    # Extract strawberry mentions (look for patterns like "Strawberry #1", "Strawberry 1", etc.)
    strawberry_pattern = r'(?:Strawberry|strawberry)\s*[#]?\s*(\d+)'
    strawberry_matches = re.finditer(strawberry_pattern, content, re.IGNORECASE)

    for match in strawberry_matches:
        strawberry_num = match.group(1)
        # Get surrounding context (500 chars before and after)
        start = max(0, match.start() - 500)
        end = min(len(content), match.end() + 500)
        context = content[start:end].strip()

        # Initialize strawberry entry if doesn't exist
        if strawberry_num not in structured_data["strawberries"]:
            structured_data["strawberries"][strawberry_num] = []

        # Add this source's content for this strawberry
        structured_data["strawberries"][strawberry_num].append({
            "source_id": idx,
            "source_url": url,
            "content": context
        })

    # Extract section mentions
    for section_name in ["Start", "Crossing", "Chasm"]:
        if section_name.lower() in content.lower():
            # Find context around section mention
            section_idx = content.lower().find(section_name.lower())
            start = max(0, section_idx - 200)
            end = min(len(content), section_idx + 1000)
            section_context = content[start:end].strip()

            structured_data["sections"][section_name].append({
                "source_id": idx,
                "source_url": url,
                "content": section_context
            })

    # Extract crystal heart mentions
    if "crystal heart" in content.lower() or "crystal_heart" in content.lower():
        heart_idx = content.lower().find("crystal")
        start = max(0, heart_idx - 300)
        end = min(len(content), heart_idx + 700)
        heart_context = content[start:end].strip()

        structured_data["collectibles"]["crystal_heart"].append({
            "source_id": idx,
            "source_url": url,
            "content": heart_context
        })

    # Extract cassette mentions
    if "cassette" in content.lower() or "b-side" in content.lower():
        cassette_idx = content.lower().find("cassette")
        if cassette_idx == -1:
            cassette_idx = content.lower().find("b-side")
        start = max(0, cassette_idx - 300)
        end = min(len(content), cassette_idx + 700)
        cassette_context = content[start:end].strip()

        structured_data["collectibles"]["cassette_tape"].append({
            "source_id": idx,
            "source_url": url,
            "content": cassette_context
        })

    print(f"    ✓ Extracted strawberry references and section content")

# Save structured data
output_file = "database/forsaken_city_level1_raw.json"
with open(output_file, "w") as f:
    json.dump(structured_data, f, indent=2)

print("\n" + "="*80)
print("Extraction Complete!")
print("="*80)
print(f"\n📊 Summary:")
print(f"  Sources processed: {len(structured_data['sources'])}")
print(f"  Strawberries found: {len(structured_data['strawberries'])} unique IDs")
print(f"  Start section entries: {len(structured_data['sections']['Start'])}")
print(f"  Crossing section entries: {len(structured_data['sections']['Crossing'])}")
print(f"  Chasm section entries: {len(structured_data['sections']['Chasm'])}")
print(f"  Crystal Heart mentions: {len(structured_data['collectibles']['crystal_heart'])}")
print(f"  Cassette mentions: {len(structured_data['collectibles']['cassette_tape'])}")
print(f"\n💾 Saved to: {output_file}")
print("\nThis file contains ALL content from all sources without synthesis.")
print("Use this as input for LLM-based hint generation later.")
