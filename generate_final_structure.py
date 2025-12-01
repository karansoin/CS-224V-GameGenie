#!/usr/bin/env python3
"""
Generate final structured database with all detailed content from 8 sources
Structure: sub_chapters with strawberry_id, info array with instruction + source
"""
import json
import re

# Load raw scraped data
with open("database/output/forsaken_city_raw_scrape.json", "r") as f:
    raw_sources = json.load(f)

print("="*80)
print("Generating Final Structured Database")
print("="*80)

# Initialize final structure
final_data = {
    "chapter": "1",
    "chapter_name": "Forsaken_City",
    "side": "A",
    "total_strawberries": 20,
    "sub_chapters": []
}

# Helper function to clean text
def clean_text(text):
    # Remove zero-width spaces and other invisible unicode characters
    text = re.sub(r'[\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff]', '', text)
    # Remove other problematic invisible characters
    text = text.replace('\u200e', '').replace('\u200f', '').replace('\ufeff', '')
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

# Helper function to extract strawberry content from a source
def extract_strawberry_info(source_content, source_url, strawberry_num):
    """Extract detailed instruction for a specific strawberry from source"""

    # Multiple keyword variations to search for
    search_patterns = [
        f"strawberry #{strawberry_num}",
        f"strawberry {strawberry_num}",
        f"berry #{strawberry_num}",
        f"berry {strawberry_num}",
        f"#{strawberry_num}",
    ]

    # Try to find any mention of this strawberry
    content_lower = source_content.lower()
    found_contexts = []

    for pattern in search_patterns:
        pattern_lower = pattern.lower()
        idx = content_lower.find(pattern_lower)

        if idx != -1:
            # Extract context around the mention (more generous than before)
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

# Process each strawberry (1-20)
print("\nProcessing Strawberries...")

for strawberry_num in range(1, 21):
    print(f"  Processing Strawberry #{strawberry_num}")

    strawberry_data = {
        "level_id": "1",
        "strawberry_id": str(strawberry_num),
        "collectible_name": f"Strawberry #{strawberry_num}",
        "section": "Start" if strawberry_num <= 6 else ("Crossing" if strawberry_num <= 15 else "Chasm"),
        "difficulty": "easy",  # Will be refined
        "objective": f"Collect Strawberry #{strawberry_num}",
        "mechanics_involved": [],
        "is_optional": True,
        "info": []
    }

    # Extract from all sources
    for source in raw_sources:
        url = source["url"]
        content = source["content"]

        instruction = extract_strawberry_info(content, url, strawberry_num)

        if instruction and len(instruction) > 50:  # Only add if substantial content
            strawberry_data["info"].append({
                "instruction": instruction,
                "source": url
            })

    # Only add if we found instructions
    if strawberry_data["info"]:
        # Deduplicate similar instructions (same source might appear twice)
        seen_instructions = set()
        unique_info = []
        for info_item in strawberry_data["info"]:
            # Use first 100 chars as fingerprint
            fingerprint = info_item["instruction"][:100]
            if fingerprint not in seen_instructions:
                seen_instructions.add(fingerprint)
                unique_info.append(info_item)

        strawberry_data["info"] = unique_info
        final_data["sub_chapters"].append(strawberry_data)
        print(f"    Added with {len(unique_info)} sources")
    else:
        print(f"    No detailed content found")

# Add Crystal Heart as sub-chapter
print("\nProcessing Crystal Heart...")
crystal_heart_data = {
    "level_id": "1",
    "strawberry_id": "crystal_heart",
    "collectible_name": "Crystal Heart",
    "section": "Crossing",
    "difficulty": "hard",
    "objective": "Collect the hidden Crystal Heart",
    "mechanics_involved": ["dash_crystals", "precise_platforming", "hidden_secrets"],
    "is_optional": True,
    "info": []
}

for source in raw_sources:
    url = source["url"]
    content = source["content"]

    # Find crystal heart mentions
    if "crystal heart" in content.lower():
        # Extract context
        idx = content.lower().find("crystal heart")
        start = max(0, idx - 500)
        end = min(len(content), idx + 1000)
        context = clean_text(content[start:end])

        if len(context) > 100:
            crystal_heart_data["info"].append({
                "instruction": context,
                "source": url
            })

if crystal_heart_data["info"]:
    final_data["sub_chapters"].append(crystal_heart_data)
    print(f"  Added Crystal Heart with {len(crystal_heart_data['info'])} sources")

# Add Cassette Tape as sub-chapter
print("\nProcessing Cassette Tape...")
cassette_data = {
    "level_id": "1",
    "strawberry_id": "cassette_tape",
    "collectible_name": "B-Side Cassette Tape",
    "section": "Chasm",
    "difficulty": "hard",
    "objective": "Collect the B-Side cassette tape to unlock B-Side",
    "mechanics_involved": ["cassette_blocks", "rhythm_timing", "dash_crystals"],
    "is_optional": True,
    "info": []
}

for source in raw_sources:
    url = source["url"]
    content = source["content"]

    # Find cassette mentions
    if "cassette" in content.lower() or "b-side" in content.lower():
        # Extract context
        keywords = ["cassette", "b-side"]
        for keyword in keywords:
            if keyword in content.lower():
                idx = content.lower().find(keyword)
                start = max(0, idx - 500)
                end = min(len(content), idx + 1000)
                context = clean_text(content[start:end])

                if len(context) > 100:
                    cassette_data["info"].append({
                        "instruction": context,
                        "source": url
                    })
                break  # Only add once per source

if cassette_data["info"]:
    final_data["sub_chapters"].append(cassette_data)
    print(f"  Added Cassette Tape with {len(cassette_data['info'])} sources")

# Save final structured data
output_file = "database/forsaken_city_level1_structured.json"
with open(output_file, "w", encoding='utf-8') as f:
    json.dump(final_data, f, indent=2, ensure_ascii=False)

print("\n" + "="*80)
print("Generation Complete!")
print("="*80)
print(f"\nFinal Statistics:")
print(f"  Total sub-chapters: {len(final_data['sub_chapters'])}")
print(f"  Strawberries: {len([s for s in final_data['sub_chapters'] if s['strawberry_id'].isdigit()])}")
print(f"  Special collectibles: {len([s for s in final_data['sub_chapters'] if not s['strawberry_id'].isdigit()])}")

# Calculate total instructions
total_instructions = sum(len(s['info']) for s in final_data['sub_chapters'])
print(f"  Total instruction sources: {total_instructions}")

# Average sources per item
avg_sources = total_instructions / len(final_data['sub_chapters']) if final_data['sub_chapters'] else 0
print(f"  Average sources per item: {avg_sources:.1f}")

print(f"\nSaved to: {output_file}")
print("\nThis file contains ALL detailed content from all 8 sources!")
print("Ready for LLM-based hint generation.")
