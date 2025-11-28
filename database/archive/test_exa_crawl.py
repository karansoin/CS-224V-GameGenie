import os
from exa import Exa
import json

EXA_API_KEY = os.getenv("EXA_API_KEY")

exa = Exa(api_key=EXA_API_KEY)

start_url = "https://celestegame.fandom.com/wiki/Celeste_Wiki"

results = exa.crawl(
    url=start_url,
    depth=1,          # Depth of crawl: 2 = main page + its sub-links
    max_pages=1,    # Cap total pages retrieved
    include_text=True # Retrieve page text along with URLs
)

print("Crawled pages:")
for r in results.results:
    # Filter only wiki article pages (avoid category/navigation links)
    if "/wiki/" in r.url:
        print(f"- {r.title}: {r.url}")

with open("celeste_initial_test.json", "w", encoding='utf-8') as f:
    json.dump(results, f)
