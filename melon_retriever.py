from pyquery import PyQuery as pq
from song import Song

def get_daily():

    songs = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    url = 'https://www.melon.com/chart/day/index.htm?classCd=DM0000'
    
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