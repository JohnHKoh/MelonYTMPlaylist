import json
import melon_retriever
from ytmusicapi import YTMusic
from datetime import date

f = open('../config.json')
config = json.load(f)

if ('brand_account' in config):
    ytmusic = YTMusic('../headers_auth.json', config['brand_account'], language="ko")
else:
    ytmusic = YTMusic('../headers_auth.json', language="ko")

playlistId = config['playlist_id']
playlist = ytmusic.get_playlist(playlistId)
tracks = playlist['tracks']
if (len(tracks) > 0):
    print("Clearing playlist...")
    clear_response = ytmusic.remove_playlist_items(playlistId, tracks)
    if "SUCCEEDED" in clear_response:
        print("Playlist cleared")
    else:
        print("Could not clear playlist")
        print(json.dumps(clear_response))
    
songs = melon_retriever.get_daily()
toAdd = []

f2 = open('../data/manual_fixes.json', 'r', encoding='utf-8')
manual_fixes = json.load(f2)

for i in range(100):
    search_query = "{} {} {}".format(songs[i].title, songs[i].artist, songs[i].album).strip()
    print("#{}: Searching for {}".format(i + 1, search_query))
    if search_query in manual_fixes:
        print("Manual fix for {}".format(search_query))
        result = manual_fixes[search_query]
    else:
        results = ytmusic.search("{} {} {}".format(songs[i].title, songs[i].artist, songs[i].album), "songs")
        result = results[0]['videoId'] # assume the top result is correct
    
    toAdd.append(result) 
    
print("Adding playlist items...")
add_response = ytmusic.add_playlist_items(playlistId, toAdd, duplicates=True)
if 'status' in add_response and 'SUCCEEDED' in add_response['status']:
    print("All items added")
else:
    print("Items could not added")
    print(json.dumps(add_response))

print("Updating playlist description...")
today = date.today();
today_str = today.strftime("%Y.%m.%d")
description = """
Melon(Korean: 멜론) is a South Korean online music store and music streaming service. 
They have a daily chart of the top 100 songs that reflects streaming 40% + download 60% of weekly service usage. This is the daily(일간) chart of Korean domestic songs(국내종합).


https://www.melon.com/chart/day/index.htm?classCd=DM0000

Updated for: {}

This playlist is auto-generated.
View the code here: https://github.com/JohnHKoh/MelonYTMPlaylist
""".format(today_str)
edit_response = ytmusic.edit_playlist(playlistId, description=description)
if 'SUCCEEDED' in edit_response:
    print("Playlist description updated")
else:
    print("Playlist description could not be updated")
    print(json.dumps(edit_response))
