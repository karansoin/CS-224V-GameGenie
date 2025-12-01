#!/usr/bin/env python3
"""
Load and use the Forsaken City Level 1 database
"""
import json

# Load the database
with open("database/forsaken_city_level1.json", "r") as f:
    level1_db = json.load(f)

print("="*80)
print(f"Loaded: Chapter {level1_db['chapter']} - {level1_db['chapter_name']} (Side {level1_db['side']})")
print("="*80)
print(f"\n📊 Stats:")
print(f"  Total Rooms: {len(level1_db['rooms'])}")
print(f"  Total Strawberries: {level1_db['collectibles']['strawberries']['total']}")
print(f"  Regular Strawberries: {level1_db['collectibles']['strawberries']['regular']}")
print(f"  Winged Strawberries: {level1_db['collectibles']['strawberries']['winged']}")
print(f"  Mechanics Introduced: {len(level1_db['mechanics_introduced'])}")
print(f"  Characters: {', '.join(level1_db['characters'])}")

print(f"\n🎮 Mechanics Introduced:")
for i, mechanic in enumerate(level1_db['mechanics_introduced'], 1):
    print(f"  {i}. {mechanic.replace('_', ' ').title()}")

print(f"\n\n📍 Sample Rooms:")
print("-"*80)

# Show first 5 rooms as examples
for room in level1_db['rooms'][:5]:
    print(f"\nRoom {room['room_id']}: {room['room_name']}")
    print(f"  Difficulty: {room['difficulty']}")
    print(f"  Objective: {room['objective']}")
    print(f"  Mechanics: {', '.join(room['mechanics_involved'])}")
    print(f"  Hint Tier 1: {room['hint_tiers'][0]}")
    print(f"  Optional: {'Yes' if room['is_optional'] else 'No'}")

print("\n" + "="*80)
print("Full database available at: database/forsaken_city_level1.json")
print("="*80)
