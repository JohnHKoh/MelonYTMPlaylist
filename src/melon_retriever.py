from pyquery import PyQuery as pq
from song import Song
from util import Util

def get_songs(listName: str) -> list:
    """
    Gets Melon Chart as list of `Song` objects

    :return: List with Melon Top100 songs
    """
    url = Util.get_config()['playlists'][listName]['url']
    return get_melon_songs(url)

    
def get_melon_songs(url: str) -> list:
    songs = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    
    d = pq(url=url, headers=headers)
    album_images = d("#tb_list tbody tr td:nth-child(4)")
    song_album_images = album_images.find("img")
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
        album_image = d(song_album_images[i]).attr("src")
        songs.append(Song(title, artist, album, album_image))

    return songs