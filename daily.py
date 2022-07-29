import json
import melon_retriever
from ytmusicapi import YTMusic
from datetime import date

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
ytmusic.edit_playlist(playlistId, description="Auto-updating Melon Daily chart. Last updated {}".format(date.today()))
print("Playlist description updated")
