import json
import melon_retriever
from ytmusicapi import YTMusic
from datetime import date
from difflib import SequenceMatcher
from song import Song

SIMILARITY_THREADSHOLD = 0.9
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio() > SIMILARITY_THREADSHOLD

f = open('../config.json')
config = json.load(f)

if 'brand_account' in config:
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
    song_title = songs[i].title
    song_artist = songs[i].artist
    song_album = songs[i].album
    search_query = "{} {} {}".format(song_title, song_artist, song_album).strip()
    print("-- #{}: Searching for '{}'".format(i + 1, search_query))

    if search_query in manual_fixes:
        print("---- Manual fix for {}".format(search_query))
        result = manual_fixes[search_query]
    else:
        results = ytmusic.search(search_query, "songs")
        similar_result_found = False
        if len(results) == 0:
            print("---- Could not find any results query {}. Skipping song.".format(search_query))
        for j in range(3):
            try:
                this_song = Song.MakeSong(results[j])
            except IndexError:
                print("---- Less than 3 results found. Using current best match.")
                top_match_song = this_song
                break;

            print("---- Checking result #{}: '{}' by '{}' from '{}'".format(j + 1, this_song.title, this_song.artist, this_song.album))
            if similar(song_title, this_song.title) and similar(song_artist, this_song.artist) and similar(song_album, this_song.album):
                print("------ Match found.")
                result = results[j]['videoId']
                top_match_song = this_song
                similar_result_found = True
                break
        
        if not similar_result_found:
            print("---- No results above threshold found, searching through album instead.")
            album_search_query = "{} {}".format(song_artist, song_album).strip()
            album_results = ytmusic.search(album_search_query, "albums")
            album_track_found = False
            if len(album_results) == 0:
                print("---- Could not find any results using query {}.".format(album_search_query))
            else:
                top_album_result = album_results[0]
                print("------ Retreiving album '{}' by '{}'.".format(top_album_result['title'], ', '.join([artist['name'] for artist in top_album_result['artists']])))
                album = ytmusic.get_album(top_album_result['browseId'])
                tracks = album['tracks']
                for k, track in enumerate(tracks):
                    this_album_song = Song.MakeSong(track)
                    print("-------- Checking track #{}: '{}'".format(k + 1, this_album_song.title))
                    if similar(song_title, this_album_song.title):
                        print("---------- Match found.")
                        result = track['videoId']
                        top_match_song = this_album_song
                        album_track_found = True
                        break
            
            if not album_track_found:
                print("------ Track not found in album. Assuming first result is correct.")
                result = results[0]['videoId']
                top_match_song = Song.MakeSong(results[0])

            
    
    print("---- Adding '{}' by '{}' from '{}' to playlist.".format(top_match_song.title, top_match_song.artist, top_match_song.album))
    # If a better match was not found, append the original top result
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
