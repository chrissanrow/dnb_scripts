import json
import glob
from geopy.geocoders import OpenCage
from geopy.extra.rate_limiter import RateLimiter

import os
from dotenv import load_dotenv 

load_dotenv()

geocoder = OpenCage(api_key=os.getenv("OPEN_CAGE_API_KEY"))

geocode = RateLimiter(geocoder.geocode, min_delay_seconds=1)

# persistent cache for geocoding results
CACHE_FILE = 'geocoding_cache.json'

def load_cache():
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

cache = load_cache()

def get_coords(location_string):
    """Fetches coordinates with caching and rate limiting."""
    if location_string in cache:
        return cache[location_string]
    
    print(f"Querying API for: {location_string}...")
    try:
        location = geocode(location_string)
        if location:
            result = {"lat": location.latitude, "lng": location.longitude}
            cache[location_string] = result
            save_cache(cache) # Save after every new hit
            return result
    except Exception as e:
        print(f"Error geocoding {location_string}: {e}")
    
    return None

UK_cities = ["London", "Bristol", "Manchester", "Leeds", "Sheffield", "Birmingham", "Glasgow", "Brighton", "Nottingham", "Liverpool"]

city_to_coords = {}
for city in UK_cities:
    coords = cache.get(city) or get_coords(city)
    if coords:
        city_to_coords[city] = coords
        print(f"{city}: {coords['lat']}, {coords['lng']}")
    else:
        print(f"Could not geocode: {city}")

for file in glob.glob('dnb_local_viz_releases.json'):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    missing_count = 0

    for entry in data:
        city = entry.get('city')
        if city == "Unknown" or city == "Worldwide" or ("&" in city):
            data.remove(entry)
            continue
        coords = city_to_coords.get(city)
        if coords:
            entry['coordinates'] = {
                'lat': coords['lat'],
                'lng': coords['lng']
            }
            updated_count += 1
        else:
            entry['coordinates'] = None
            missing_count += 1
            # Remove missing country from json
            data.remove(entry)
            print(f"Missing coordinates for: {country}")

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Updated {file}: {updated_count} with coordinates, {missing_count} missing")

