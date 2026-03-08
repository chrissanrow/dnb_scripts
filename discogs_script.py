import discogs_client
import os
from dotenv import load_dotenv 
import json

# loading variables from .env file
load_dotenv() 

d = discogs_client.Client('dnb/0.1', user_token=os.getenv("DISCOG_ACCESS_TOKEN"))

'''
VISUALIZATION 1:
country-based geographic distribution of releases from 5-year increments with clusters of datapoints
Hovering over a cluster will show the number of releases from that geographic area and the top 5 releases from that area
'''

# Searching for releases in the Drum n Bass style
dnb_songs = d.search('', style='Drum n Bass', type='release', year='1990-1994')
# Forming JSON data for further processing with pandas
json_data = []
for song in dnb_songs:
    song_data = {
        'title': song.title,
        'year': song.year,
        'country': song.country,
        'have_marketplace': song.data.get('community', {}).get('have', 0)
    }
    json_data.append(song_data)

# Output JSON data to a file for further processing
with open('dnb_songs.json', 'w') as f:
    json.dump(json_data, f, indent=4)
'''
print(f"Number of users who have this release in the marketplace: {have_marketplace}")
have = dnb_songs[0].data.get('community', {}).get('have', 'N/A')
print(f"Number of users who have this release: {have}")
'''

'''
bristol_labels = d.search('', type='label')
print("LABEL STRUCTURE: ", dir(bristol_labels[1]))
print("PROFILE STRUCTURE: ", dir(bristol_labels[1].profile))
print("PROFILE: ", bristol_labels[1].profile)
print("CONTACT STRUCTURE: ", dir(bristol_labels[1].contact_info))
print("CONTACT: ", bristol_labels[1].contact_info)'''

'''
dnb_artist = d.search('', type='artist')
print(f"Found {len(dnb_artist)} artists in the Drum n Bass style.")
print("ARTIST STRUCTURE: ", dir(dnb_artist[0]))
print("ARTIST PROFILE: ", dnb_artist[0].profile)
'''

'''
write_string = ""
for song in dnb_songs:
    write_string += f"Title: {song.title}, Year: {song.year}, Country: {song.country}\n"

with open('dnb_songs.txt', 'w') as f:
    f.write(write_string)
'''