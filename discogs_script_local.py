import discogs_client
import os
import sys
import time
from dotenv import load_dotenv 
import json
import heapq
from itertools import count
from discogs_client.exceptions import HTTPError

# loading variables from .env file
load_dotenv() 

d = discogs_client.Client('dnb/0.1', user_token=os.getenv("DISCOG_ACCESS_TOKEN"))
d.backoff_enabled = True  # Enable automatic backoff handling for rate limits

'''
VISUALIZATION 2:
local distribution of UK DnB releases and artists by city/region from 1990-2005
'''

UK_cities = ["London", "Bristol", "Manchester", "Leeds", "Sheffield", "Birmingham", "Glasgow", "Brighton", "Nottingham", "Liverpool"]

# Searching for releases in the Drum n Bass style
def process_dnb_releases(year):
    dnb_releases = d.search('', style='Drum n Bass', type='release', year=year, country='UK')

    city_release_counts = {city: 0 for city in UK_cities}
    city_top_releases = {city: {"release_count": 0, "top_releases": []} for city in UK_cities}
    tie_breaker = count()
    artist_profile_cache = {}  # Cache profiles by artist ID
    num_releases = len(dnb_releases)
    print(f"{num_releases} releases found")
    # Build release counts and top-5 releases per city in one pass
    for release in dnb_releases:
        num_releases -= 1
        print(num_releases)
        data = release.data

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

        try:
            release_artists = release.artists
        except (HTTPError, json.JSONDecodeError, Exception) as e:
            # Skip releases with API errors (rate limit, invalid JSON, deleted, etc.)
            continue

        if not release_artists:
            continue

        try:
            release_artist_profile = release_artists[0].profile.lower()
        except (HTTPError, json.JSONDecodeError, Exception) as e:
            # Skip artists with API errors (rate limit, invalid JSON, deleted, etc.)
            continue
            
        for c in UK_cities:
            if c.lower() in release_artist_profile:
                city_release_counts[c] += 1

                heap = city_top_releases[c].setdefault('top_releases', [])
                heap_entry = (have_count, next(tie_breaker), release_info)
                if len(heap) < 5:
                    heapq.heappush(heap, heap_entry)
                elif have_count > heap[0][0]:
                    heapq.heapreplace(heap, heap_entry)
        
        # Rate limiting: respect API limits
        # time.sleep(0.5)


    json_data = []
    for city, release_count in city_release_counts.items():
        top_5_releases = [
            entry[2] for entry in sorted(city_top_releases[city]['top_releases'], key=lambda entry: entry[0], reverse=True)
        ]
        json_data.append({
            "city": city,
            "release_count": release_count,
            "top_releases": top_5_releases
        })
        

    # Output JSON data to a file for further processing
    with open(f'dnb_local_viz_releases.json', 'w') as f:
        json.dump(json_data, f, indent=4)

process_dnb_releases('1990-1994')