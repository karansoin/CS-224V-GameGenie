#!/usr/bin/env python3
"""
Merge room-based structure with multi-source info data
Takes hint_tiers from forsaken_city_level1.json and converts to info array with sources
"""
import json

# Load the room-based structure (with hint_tiers)
with open("database/forsaken_city_level1.json", "r") as f:
    room_data = json.load(f)

# Load the multi-source structured data
with open("database/forsaken_city_level1_structured.json", "r") as f:
    source_data = json.load(f)

print("="*80)
print("Merging Room Structure with Multi-Source Data")
print("="*80)

# Create a mapping of strawberry_id to info array
strawberry_info_map = {}
for sub_chapter in source_data["sub_chapters"]:
    strawberry_id = sub_chapter["strawberry_id"]
    strawberry_info_map[strawberry_id] = sub_chapter["info"]

# Process each room and update hint_tiers to info structure
for room in room_data["rooms"]:
    room_name = room["room_name"]

    # Extract strawberry number from room name if it exists
    strawberry_num = None
    if "Strawberry #" in room_name:
        # Extract number after "Strawberry #"
        import re
        match = re.search(r'Strawberry #(\d+)', room_name)
        if match:
            strawberry_num = match.group(1)
    elif "Crystal Heart" in room_name:
        strawberry_num = "crystal_heart"
    elif "Cassette" in room_name or "B-Side" in room_name:
        strawberry_num = "cassette_tape"

    # Convert hint_tiers to info structure
    if "hint_tiers" in room:
        hint_tiers = room["hint_tiers"]
        del room["hint_tiers"]  # Remove old structure

        # Create new info array
        room["info"] = []

        # Add hint tiers as individual info entries
        for i, hint in enumerate(hint_tiers):
            tier_num = i + 1
            room["info"].append({
                "instruction": hint,
                "source": room.get("provenance_url", "https://celeste.ink/wiki/Forsaken_City"),
                "hint_tier": tier_num
            })

        # If this room corresponds to a strawberry, add multi-source data
        if strawberry_num and strawberry_num in strawberry_info_map:
            print(f"  Merging sources for {room_name} (strawberry_id: {strawberry_num})")
            multi_sources = strawberry_info_map[strawberry_num]

            # Add all sources from structured data
            for source_info in multi_sources:
                room["info"].append({
                    "instruction": source_info["instruction"],
                    "source": source_info["source"],
                    "hint_tier": None  # These are raw source data, not tiered hints
                })

            print(f"    Added {len(multi_sources)} additional sources")
        else:
            print(f"  Converted {room_name} (no additional sources)")

    # Remove old provenance_url field (now in info sources)
    if "provenance_url" in room:
        del room["provenance_url"]

# Save updated structure
output_file = "database/forsaken_city_level1.json"
with open(output_file, "w", encoding='utf-8') as f:
    json.dump(room_data, f, indent=2, ensure_ascii=False)

print("\n" + "="*80)
print("Merge Complete!")
print("="*80)
print(f"\nUpdated: {output_file}")
print("\nStructure:")
print("- Rooms preserved with room_id and room_name")
print("- hint_tiers converted to info array")
print("- Each info entry has: instruction, source, hint_tier")
print("- Multi-source data merged where available")
print("\nReady for hint generation with full source attribution!")
