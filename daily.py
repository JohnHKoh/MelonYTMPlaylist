import json
import melon_retriever
from ytmusicapi import YTMusic
from datetime import date, datetime

f = open('config.json')
config = json.load(f)

if ('brand_account' in config):
    ytmusic = YTMusic('headers_auth.json', config['brand_account'], language="ko")
else:
    ytmusic = YTMusic('headers_auth.json', language="ko")

playlistId = config['playlist_id']
playlist = ytmusic.get_playlist(playlistId)
tracks = playlist['tracks']
if (len(tracks) > 0):
    print("Clearing playlist...")
    ytmusic.remove_playlist_items(playlistId, tracks)
    print("Playlist cleared")
songs = melon_retriever.get_daily()
toAdd = []
for i in range(100):
    print("#{}: Searching for {} {} {}".format(i + 1, songs[i].title, songs[i].artist, songs[i].album))
    results = ytmusic.search("{} {} {}".format(songs[i].title, songs[i].artist, songs[i].album), "songs")
    toAdd.append(results[0]['videoId']) # assume the top result is correct
    
print("Adding playlist items...")
ytmusic.add_playlist_items(playlistId, toAdd, duplicates=True)
print("All items added")

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
ytmusic.edit_playlist(playlistId, description=description)
print("Playlist description updated")
