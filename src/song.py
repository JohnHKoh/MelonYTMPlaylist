class Song:
  def __init__(self, title, artist, album, album_image = "", video_id = ""):
    self.title = title
    self.artist = artist
    self.album = album
    self.album_image = album_image
    self.video_id = video_id
  
  def MakeSong(track):
    title = track['title']
    artist = ', '.join([artist['name'] for artist in track['artists']])
    album = track['album']['name'] if type(track['album']) == dict else track['album']
    video_id = track['videoId']
    return Song(title, artist, album, video_id = video_id)

  def __repr__(self):
    return "{} - {} - {}".format(self.title, self.artist, self.album)
