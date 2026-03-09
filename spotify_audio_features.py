import http.client
import os
import dotenv

'''

# FETCH AUDIO FEATURES

dotenv.load_dotenv()

conn = http.client.HTTPSConnection("spotify-extended-audio-features-api.p.rapidapi.com")

headers = {
    'x-rapidapi-key': os.getenv("RAPID_API_KEY"),
    'x-rapidapi-host': "spotify-extended-audio-features-api.p.rapidapi.com"
}

spotify_track_id = "3ZQs8RHO3lPZoUwpavPENL"
conn.request("GET", f"/v1/audio-features/{spotify_track_id}", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

# output data to JSON file for further processing
with open('spotify_audio_features.json', 'w') as f:
    f.write(data.decode("utf-8"))
'''

# ANALYZE JSONS AND PREPARE VISUALIZATION DATA

import json

london_features_path = 'london_features.json'
bristol_features_path = 'bristol_features.json'

'''
Goldie - Inner City Life (https://open.spotify.com/track/0O7xFEqePrcTUgOi4qe0uB)
Ed Rush & Optical - Alien Girl
(https://open.spotify.com/track/091ZwHWVsGPHFjOVT1lVUe)
Dillinja - The Angels Fell (https://open.spotify.com/track/2KL9mHCn3aSZJzxpJM4HNb)
Bad Company UK - The Nine (https://open.spotify.com/track/0awLvZO3LzER9SrsS8PgKT)
Photek - The Hidden Camera (https://open.spotify.com/track/5N8VkEzambxF3o4hAD1bUE)
'''

london_track_titles = ["Goldie - Inner City Life", "Ed Rush & Optical - Alien Girl", "Dillinja - The Angels Fell", "Bad Company UK - The Nine", "Photek - The Hidden Camera"]

'''
Roni Size / Reprazent - Brown Paper Bag (https://open.spotify.com/track/3ZQs8RHO3lPZoUwpavPENL)
Dj Die - Clear Skyz (https://open.spotify.com/track/2AjQxmqazcuu4zz2APsAa5)
Krust - Warhead (https://open.spotify.com/track/5aHkhW2AgKCsvgYyqLxkrh)
Roni Size & Dj Die - It's a Jazz Thing (https://open.spotify.com/track/1BWzM0r2zEcTPgkis7HP9o)
Dazee & Euphonique - Skip De Du Dat (https://open.spotify.com/track/0vFLfTngpiXhXhbY4yPkBc)
'''

bristol_track_titles = ["Roni Size / Reprazent - Brown Paper Bag", "Dj Die - Clear Skyz", "Krust - Warhead", "Roni Size & Dj Die - It's a Jazz Thing", "Dazee & Euphonique - Skip De Du Dat"]

def add_titles_to_features(path, titles):
    with open(path, 'r', encoding='utf-8') as f:
        feature_data = json.load(f)

    for item, title in zip(feature_data, titles):
        item['title'] = title

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(feature_data, f, indent=4, ensure_ascii=False)


# Add track titles to the JSON data for better visualization labels
add_titles_to_features(london_features_path, london_track_titles)
add_titles_to_features(bristol_features_path, bristol_track_titles)

# Compute mean data for Danceability, Energy, Valence, Acousticness, Instrumentalness for each city
def compute_mean_features(path):
    with open(path, 'r', encoding='utf-8') as f:
        feature_data = json.load(f)
    mean_features = {}
    for item in feature_data:
        for key in ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness']:
            mean_features[key] = mean_features.get(key, 0) + item.get(key, 0)
    count = len(feature_data)
    for key in mean_features:
        mean_features[key] /= count
    return mean_features

summary = {
    "London": compute_mean_features(london_features_path),
    "Bristol": compute_mean_features(bristol_features_path)
}

# Output summary data to a JSON file for visualization
with open('city_feature_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=4, ensure_ascii=False)