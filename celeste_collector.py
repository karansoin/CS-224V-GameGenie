import json
import os
from setup import exa_client

# Preferred source domains for Celeste information
PREFERRED_DOMAINS = [
    "celeste.ink",           # Celeste Wiki Main
    "celestegame.fandom.com", # Fandom Wiki
    "ign.com",               # IGN Walkthrough
    "reddit.com",            # r/celestegame
]

# Known direct URLs for each chapter (to crawl directly)
CHAPTER_URLS = {
    1: {
        "name": "Forsaken City",
        "direct_urls": [
            "https://celeste.ink/wiki/Forsaken_City",
            "https://celestegame.fandom.com/wiki/Chapter_1:_Forsaken_City",
            "https://www.ign.com/wikis/celeste/Chapter_1-_Forsaken_City",
        ]
    },
    2: {
        "name": "Old Site",
        "direct_urls": [
            "https://celeste.ink/wiki/Old_Site",
            "https://celestegame.fandom.com/wiki/Chapter_2:_Old_Site",
            "https://www.ign.com/wikis/celeste/Chapter_2-_Old_Site",
        ]
    },
    3: {
        "name": "Celestial Resort",
        "direct_urls": [
            "https://celeste.ink/wiki/Celestial_Resort",
            "https://celestegame.fandom.com/wiki/Chapter_3:_Celestial_Resort",
            "https://www.ign.com/wikis/celeste/Chapter_3-_Celestial_Resort",
        ]
    }
}


def crawl_direct_urls(urls):
    """
    Directly crawl known URLs using get_contents.
    This is more reliable for known wiki pages.
    Uses subpages to get linked content as well.
    """
    print(f"  Crawling {len(urls)} direct URLs (with subpages)...")

    try:
        results = exa_client.get_contents(
            urls,
            text=True,
            subpages=5,  # Crawl up to 5 linked pages from each main page
            livecrawl="preferred"  # Prefer live crawling for fresh content
        )

        crawled_data = []
        for result in results.results:
            data = {
                "source_type": "direct_crawl",
                "title": result.title,
                "url": result.url,
                "published_date": getattr(result, 'published_date', None),
                "text": getattr(result, 'text', ''),
            }

            # Include subpages if they exist
            subpages = getattr(result, 'subpages', [])
            if subpages:
                data["subpages"] = []
                for subpage in subpages:
                    data["subpages"].append({
                        "title": subpage.title,
                        "url": subpage.url,
                        "text": getattr(subpage, 'text', ''),
                    })
                print(f"    ✓ Crawled: {result.title[:50]}... (+{len(subpages)} subpages)")
            else:
                print(f"    ✓ Crawled: {result.title[:50]}...")

            crawled_data.append(data)

        return crawled_data

    except Exception as e:
        print(f"    Error crawling URLs: {e}")
        return []


def search_chapter_content(chapter_num, chapter_name, queries):
    """
    Search for additional chapter content using search_and_contents.
    Focuses on preferred domains.
    """
    search_results = []

    for query in queries:
        print(f"  Searching: {query}")

        try:
            results = exa_client.search_and_contents(
                query,
                type="auto",
                num_results=5,
                text=True,
                include_domains=PREFERRED_DOMAINS
            )

            for result in results.results:
                search_results.append({
                    "source_type": "search",
                    "query": query,
                    "title": result.title,
                    "url": result.url,
                    "published_date": getattr(result, 'published_date', None),
                    "text": getattr(result, 'text', ''),
                })
                print(f"    Found: {result.title[:50]}...")

        except Exception as e:
            print(f"    Error: {e}")

    return search_results


def collect_chapter_data(chapter_num):
    """
    Collect comprehensive data for a Celeste chapter.
    Uses both direct URL crawling and search.
    """
    chapter_info = CHAPTER_URLS[chapter_num]
    chapter_name = chapter_info["name"]

    chapter_data = {
        "chapter_number": chapter_num,
        "chapter_name": chapter_name,
        "sources": []
    }

    # 1. Direct crawl of known wiki pages
    print(f"\n  Step 1: Crawling known wiki pages...")
    direct_sources = crawl_direct_urls(chapter_info["direct_urls"])
    chapter_data["sources"].extend(direct_sources)

    # 2. Search for additional content (Reddit discussions, etc.)
    print(f"\n  Step 2: Searching for additional content...")
    search_queries = [
        f"Celeste {chapter_name} strawberries locations guide",
        f"Celeste Chapter {chapter_num} B-side cassette tape",
        f"Celeste {chapter_name} crystal heart",
        f"site:reddit.com/r/celestegame {chapter_name} tips",
    ]

    search_sources = search_chapter_content(chapter_num, chapter_name, search_queries)
    chapter_data["sources"].extend(search_sources)

    # Remove duplicates based on URL
    seen_urls = set()
    unique_sources = []
    for source in chapter_data["sources"]:
        if source["url"] not in seen_urls:
            seen_urls.add(source["url"])
            unique_sources.append(source)

    chapter_data["sources"] = unique_sources
    chapter_data["total_sources"] = len(unique_sources)

    return chapter_data


def save_chapter_data(chapter_data, output_dir="output/chapters"):
    """Save chapter data to JSON file."""
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{output_dir}/chapter_{chapter_data['chapter_number']}_{chapter_data['chapter_name'].lower().replace(' ', '_')}.json"

    with open(filename, 'w') as f:
        json.dump(chapter_data, f, indent=2, default=str)

    print(f"\n  ✓ Saved to {filename}")
    print(f"    Total sources: {chapter_data['total_sources']}")
    return filename


def collect_all_chapters():
    """Collect data for Celeste chapters 1-3."""

    all_data = {}

    for chapter_num in [1, 2, 3]:
        chapter_name = CHAPTER_URLS[chapter_num]["name"]

        print(f"\n{'='*60}")
        print(f"CHAPTER {chapter_num}: {chapter_name.upper()}")
        print('='*60)

        chapter_data = collect_chapter_data(chapter_num)

        # Save individual chapter file
        save_chapter_data(chapter_data)

        all_data[f"chapter_{chapter_num}"] = chapter_data

    # Save combined file
    os.makedirs("output", exist_ok=True)
    with open("output/celeste_chapters_1_3.json", 'w') as f:
        json.dump(all_data, f, indent=2, default=str)

    print(f"\n{'='*60}")
    print("ALL DATA COLLECTION COMPLETE")
    print('='*60)
    print(f"Combined data saved to: output/celeste_chapters_1_3.json")

    total_sources = sum(data["total_sources"] for data in all_data.values())
    print(f"Total sources collected: {total_sources}")

    return all_data


if __name__ == "__main__":
    collect_all_chapters()
