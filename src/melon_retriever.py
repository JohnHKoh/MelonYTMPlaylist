from pyquery import PyQuery as pq
from song import Song
from util import Util

def get_daily():
    """
    Gets Melon Daily Top 100 List as list of `Song` objects

    :return: List with Melon Daily Top 100 songs
    """
    url = Util.get_config()['playlists']['daily']['url']
    return get_melon_songs(url)
    
def get_melon_songs(url):
    songs = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    
    d = pq(url, headers=headers)
    songs_info = d("#tb_list tbody tr td:nth-child(6)")
    song_titles = songs_info.find(".rank01")
    d('.rank02 span').remove()
    song_artists = songs_info.find(".rank02")
    albums_info = d("#tb_list tbody tr td:nth-child(7)")
    song_albums = albums_info.find(".rank03")
    for i in range(100):
        title = d(song_titles[i]).text()
        artist = d(song_artists[i]).text()
        album = d(song_albums[i]).text()
        songs.append(Song(title, artist, album))

    return songs