from video_type import VideoType

class Song:

  def __init__(self, title, artist, album, album_image):
    self.title = title
    self.artist = artist
    self.album = album
    self.album_image = album_image
  
  def MakeSong(track):
    title = track['title']
    artist = ', '.join([artist['name'] for artist in track['artists']])
    if "album" in track:
      album = track['album']['name'] if type(track['album']) == dict else track['album']
    else:
      album = None
    song = Song(title, artist, album, None)
    song.video_type = track['videoType']
    song.video_id = track['videoId']
    return song

  def __repr__(self):
    return "{} - {} - {}".format(self.title, self.artist, self.album)
