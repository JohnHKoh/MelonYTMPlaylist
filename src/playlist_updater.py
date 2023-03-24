import json
from util import Util
from ytmusicapi import YTMusic
from datetime import date, datetime, timedelta
from song import Song
from image_similarity import images_are_similar
import sys
import time

def create_ytm(config):
    if 'brand_account' in config:
        ytmusic = YTMusic('../headers_auth.json',
                            config['brand_account'], language="ko")
    else:
        ytmusic = YTMusic('../headers_auth.json', language="ko")

    return ytmusic

def similar_artist(a, b):
    a = a.lower()
    b = b.lower()
    return a in b or b in a or Util.similar(a, b)

class PlaylistUpdater:

    RETRY_COUNT = 3
    SONG_COUNT = 100
    config = Util.get_config()
    ytmusic = create_ytm(config)

    def __init__(self):
        pass

    def update_playlist(self, songs, listName, description):
        """
        Updates playlist from config with song list

        :param songs: List of `Song` objects
        :param listName: Key to search `playlists` value in "config.json"
        :param description: Updated description of playlist. Can specify `{playlist_url}` and `{today}` to be formatted
        """
        self.playlistId = self.config['playlists'][listName]['playlist_id']
        success = False
        for i in range(self.RETRY_COUNT):
            try:
                Util.log("Playlist update attempt #{}...".format(i + 1))
                self.playlist = self.get_playlist()
                self._update_playlist(self.playlist, songs, listName, description)
                Util.log("Verifying update...")
                Util.log("Getting playlist...", 2)
                playlist = self.get_playlist()
                Util.log("Playlist retrieved.", 2)
                trackCount = len(playlist['tracks']) # Buggy 'trackCount' key, use 'tracks' array length instead
                Util.log("Playlist trackCount is {}.".format(trackCount), 2)
                if trackCount != self.SONG_COUNT:
                    raise Exception("'trackCount' returned {} instead of {}.".format(trackCount, self.SONG_COUNT))
                success = True
                break
            except Exception as e:
                Util.log("Encountered exception in playlist update loop. {}".format(str(e)))

        if success:
            Util.log("Playlist update completed at {}.".format(datetime.now()))
            sys.exit(0)
        else:
            Util.log("Playlist update failed at {}.".format(datetime.now()))
            sys.exit(1)

    def _update_playlist(self, playlist, songs, listName, description):
        """
        Internal function to updates playlist from config with song list

        :param songs: List of `Song` objects
        :param listName: Key to search `playlists` value in "config.json"
        :param description: Updated description of playlist. Can specify `{playlist_url}` and `{today}` to be formatted
        """

        Util.log("Starting playlist update at {}...".format(datetime.now()))
        
        # Various sleep calls seem to prevent transient 409 Conflict errors
        try:
            to_add = self.get_song_ids(songs)
            if playlist['trackCount'] > 0:
                self.clear_playlist()
                time.sleep(3)
            self.add_playlist_items(to_add)
            time.sleep(3)
            self.update_playlist_description(listName, description)
            time.sleep(3)
        except Exception as e:
            Util.log("Encountered exception while trying to update playlist. {}".format(str(e)))
            raise e
        
        Util.log("Playlist update attempt completed at {}.".format(datetime.now()))

    def update_playlist_description(self, listName, description):
        Util.log("Updating playlist description...")
        date_str = "Unknown"
        today = date.today()
        if listName == "daily":
            date_str = today.strftime("%Y.%m.%d")
        if listName == "weekly":
            past_monday = today - timedelta(days=today.weekday(), weeks=1)
            past_sunday = past_monday + timedelta(days=6)
            date_str = "{past_monday} ~ {past_sunday}".format(past_monday=past_monday.strftime("%Y.%m.%d"), past_sunday=past_sunday.strftime("%Y.%m.%d"))
        description = description.format(playlist_url=self.config['playlists'][listName]['url'], date=date_str)
        edit_response = self.ytmusic.edit_playlist(self.playlistId, description=description)
        if 'SUCCEEDED' in edit_response:
            Util.log("Playlist description updated.")
        else:
            Util.log("Playlist description could not be updated.")
            Util.log(json.dumps(edit_response))

    def get_playlist(self):
        return self.ytmusic.get_playlist(self.playlistId, None)

    def add_playlist_items(self, song_ids):
        Util.log("Adding playlist items (total: {})...".format(len(song_ids)))
        add_response = self.ytmusic.add_playlist_items(self.playlistId, song_ids, duplicates=True)
        if 'status' in add_response and 'SUCCEEDED' in add_response['status']:
            Util.log("All items added.")
        else:
            Util.log("Items could not be added.")
            Util.log(json.dumps(add_response))

    def get_song_ids(self, songs):
        to_add = []

        for i in range(self.SONG_COUNT):
            song = self.get_song(songs[i], i)
            if song is None:
                continue

            Util.log("Adding '{}' by '{}' from '{}' to add list.".format(song.title, song.artist, song.album), 3)
            to_add.append(song.video_id)

        return to_add

    def clear_playlist(self):
        Util.log("Clearing playlist...")
        clear_response = self.ytmusic.remove_playlist_items(self.playlistId, self.playlist['tracks'])
        if "SUCCEEDED" in clear_response:
            Util.log("Playlist cleared.")
        else:
            Util.log("Could not clear playlist.")
            Util.log(json.dumps(clear_response))


    def get_song(self, song, index):
        search_query = "{} {} {}".format(song.title, song.artist, song.album).strip()
        manual_fixes = Util.get_manual_fixes()

        Util.log("#{}: Searching for '{}'".format(index + 1, search_query), 2)

        if search_query in manual_fixes:
            Util.log("Manual fix for '{}'".format(search_query), 3)
            song.video_id = manual_fixes[search_query]
            return song
        
        return self.search_for_song(song, search_query)
    
    def search_for_song(self, song, search_query):
        results = self.ytmusic.search(search_query, "songs")

        if len(results) == 0:
            Util.log("Could not find any song results with query '{}'. Skipping song.".format(search_query), 3)
            return None

        song_result = self.get_match_from_top_results(song, results)
        if song_result is None:
            Util.log("No results above threshold found, searching through album instead.", 3)
            song_result = self.get_match_from_album(song)

        if song_result is None:
            Util.log("Track not found in album. Assuming first result is correct.", 4)
            song_result = Song.MakeSong(results[0])

        return song_result


    def get_match_from_top_results(self, song, results, results_to_search = 3):
        for i in range(results_to_search):
            try:
                this_song = Song.MakeSong(results[i])
            except IndexError:
                Util.log("Less than {} results found.".format(results_to_search), 3)
                return None

            Util.log("Checking result #{}: '{}' by '{}' from '{}'".format(i + 1, this_song.title, this_song.artist, this_song.album), 3)

            if Util.similar(song.title, this_song.title) and similar_artist(song.artist, this_song.artist) and Util.similar(song.album, this_song.album):
                Util.log("Match found.", 4)
                return this_song
        
        return None

    def get_match_from_album(self, song):
        album = self.get_matching_album(song)
        if album is None:
            return None

        Util.log("Retrieving album '{}' by '{}'".format(album['title'], ', '.join([artist['name'] for artist in album['artists']])), 4)
        album = self.ytmusic.get_album(album['browseId'])
        tracks = album['tracks']
        for i, track in enumerate(tracks):
            this_album_song = Song.MakeSong(track)
            Util.log("Checking track #{}: '{}'".format(i + 1, this_album_song.title), 5)
            if Util.similar(song.title, this_album_song.title):
                Util.log("Match found.", 6)
                return this_album_song

        return None

    def get_matching_album(self, song, results_to_search = 3):
        album_search_query = "{} {}".format(song.artist, song.album).strip()
        album_results = self.ytmusic.search(album_search_query, "albums")
        if len(album_results) == 0:
            Util.log("Could not find any albums using query '{}'.".format(album_search_query), 4)
            return None
        
        for i in range(results_to_search):
            try:
                if Util.similar(song.album, album_results[i]['title']) and similar_artist(song.artist, ', '.join([artist['name'] for artist in album_results[i]['artists']])):
                    return album_results[i]
            except IndexError:
                return album_results[i-1]

        Util.log("Could not find any albums matching name and artist using query '{}'. Trying album image similarity...".format(album_search_query), 4)
        return self.get_image_matching_album(song, album_results)

    def get_image_matching_album(self, song, album_results):
        try:
            for album in album_results:
                album_image_url = next(filter(lambda thumbnail: thumbnail['width'] == 120 and thumbnail['height'] == 120, album['thumbnails']))['url']
                if (images_are_similar(song.album_image, album_image_url)):
                    Util.log("Visually similar album image found.", 5)
                    return album
            
            Util.log("Could not find visually similar album image.", 5)
            return None
        except Exception as e:
            Util.log("Error while finding visually similar album image. {}".format(str(e)), 5)
            return None


