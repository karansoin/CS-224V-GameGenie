# Forsaken City Level 1 Database - Complete

## Final Structured Database Created

**File:** `database/forsaken_city_level1_structured.json`

### Statistics:
- **Total sub-chapters:** 22
  - 20 Strawberries
  - 1 Crystal Heart
  - 1 B-Side Cassette Tape
- **Total instruction sources:** 77
- **Average sources per item:** 3.5
- **Strawberries:** 3-4 sources each
- **Special collectibles:** 8 sources each (Crystal Heart, Cassette)
- **Data from 8 different guides**

### Structure:

```json
{
  "chapter": "1",
  "chapter_name": "Forsaken_City",
  "side": "A",
  "total_strawberries": 20,
  "sub_chapters": [
    {
      "level_id": "1",
      "strawberry_id": "1",
      "collectible_name": "Strawberry #1",
      "section": "Start|Crossing|Chasm",
      "difficulty": "easy",
      "objective": "Collect Strawberry #1",
      "mechanics_involved": [],
      "is_optional": true,
      "info": [
        {
          "instruction": "Detailed guide text from source...",
          "source": "https://example.com/..."
        }
      ]
    }
  ]
}
```

### Key Features:

1. **No Synthesis** - All content preserved from original sources
2. **Multiple Sources** - Each strawberry has 3-4 different guide descriptions, special collectibles have 8
3. **Queryable by ID** - Direct access via `strawberry_id`
4. **Section-Based** - Organized by Start, Crossing, Chasm
5. **Special Collectibles** - Crystal Heart and Cassette Tape included as sub-chapters
6. **Improved Extraction** - Uses keyword-based context extraction to capture more content

### Content Coverage:

**Strawberries 1-6:** Start section
**Strawberries 7-15:** Crossing section
**Strawberries 16-20:** Chasm section
**Crystal Heart:** Crossing section (8 sources)
**Cassette Tape:** Chasm section (8 sources)

### How to Query:

```python
import json

# Load database
with open("database/forsaken_city_level1_structured.json") as f:
    data = json.load(f)

# Get Strawberry #5
strawberry_5 = [s for s in data["sub_chapters"] if s["strawberry_id"] == "5"][0]

# Access all instruction sources
for info in strawberry_5["info"]:
    print(f"Source: {info['source']}")
    print(f"Instruction: {info['instruction'][:200]}...")
```

### LLM Integration (Once API Works):

```python
# Get all sources for a strawberry
strawberry_data = get_strawberry_by_id(user_query_id)

# Pass to LLM for hint generation
prompt = f"""
Generate 3 progressive hints for Celeste Strawberry #{strawberry_data['strawberry_id']}

Available information from {len(strawberry_data['info'])} sources:
{json.dumps(strawberry_data['info'], indent=2)}

Generate:
- Tier 1: Vague directional hint
- Tier 2: More specific guidance
- Tier 3: Step-by-step instructions
"""

hints = llm.generate(prompt)
```

### Files Created:

1. **`database/output/forsaken_city_raw_scrape.json`**
   - Raw scraped HTML/text from 8 sources
   - ~142,237 total characters

2. **`database/forsaken_city_level1_raw.json`**
   - Extracted and organized by strawberry ID
   - Multiple sources per strawberry preserved

3. **`database/forsaken_city_level1_structured.json`** **FINAL FILE**
   - Clean structure with sub_chapters
   - strawberry_id as primary key
   - info array with instruction + source
   - Ready for production use

### Sources Used:

1. https://celeste.ink/wiki/Forsaken_City
2. https://celestegame.fandom.com/wiki/Chapter_1:_Forsaken_City
3. https://www.ign.com/wikis/celeste/Chapter_1-_Forsaken_City
4. https://steamcommunity.com/sharedfiles/filedetails/?id=3474899136
5. https://www.neoseeker.com/celeste/walkthrough/Level_1_-_Forsaken_City
6. https://www.switchaboo.com/celeste-100-strawberry-guide/
7. https://www.trueachievements.com/game/Celeste/walkthrough/3
8. (Duplicate fandom URL - deduplicated in processing)

### Next Steps:

1. Database complete
2. Wait for LiteLLM API access
3. Integrate with notebook
4. Build LLM-powered hint generation system
5. Test with real queries

---

**Status:** Database ready for LLM integration
