import discogs_client
import os
import sys
from dotenv import load_dotenv 
import json
import heapq
from itertools import count

# loading variables from .env file
load_dotenv() 

d = discogs_client.Client('dnb/0.1', user_token=os.getenv("DISCOG_ACCESS_TOKEN"))

'''
VISUALIZATION 1:
country-based geographic distribution of releases from 5-year increments with clusters of datapoints
Hovering over a cluster will show the number of releases from that geographic area and the top 5 releases from that area
'''

# Searching for releases in the Drum n Bass style
def process_dnb_releases(year):
    dnb_releases = d.search('', style='Drum n Bass', type='release', year=year)

    country_release_counts = {}
    country_top_releases = {}
    tie_breaker = count()
    print(f"{len(dnb_releases)} releases found for {year}")
    # Build release counts and top-5 releases per country in one pass
    for release in dnb_releases:
        data = release.data

        country = data.get('country')
        if not country:
            continue

        have_count = data.get('community', {}).get('have', 0) or 0
        release_info = {'have_count': have_count}

        title = data.get('title')
        if title:
            release_info['title'] = title

        release_info['year'] = data.get('year') or "Unknown Year"

        image_url = data.get('cover_image') or data.get('thumb')
        if image_url:
            release_info['image_url'] = image_url

        release_url = data.get('uri')
        if release_url:
            release_info['release_url'] = release_url

        country_release_counts[country] = country_release_counts.get(country, 0) + 1

        heap = country_top_releases.setdefault(country, [])
        heap_entry = (have_count, next(tie_breaker), release_info)
        if len(heap) < 5:
            heapq.heappush(heap, heap_entry)
        elif have_count > heap[0][0]:
            heapq.heapreplace(heap, heap_entry)

    json_data = []
    for country, release_count in country_release_counts.items():
        top_5_releases = [
            entry[2] for entry in sorted(country_top_releases[country], key=lambda entry: entry[0], reverse=True)
        ]
        json_data.append({
            "country": country,
            "release_count": release_count,
            "top_releases": top_5_releases
        })
        

    # Output JSON data to a file for further processing
    with open(f'dnb_viz_{year}_releases.json', 'w') as f:
        json.dump(json_data, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 discogs_script.py <year_range>")
        print("Example: python3 discogs_script.py 1990-1999")
        sys.exit(1)
    
    year_range = sys.argv[1]
    process_dnb_releases(year_range)