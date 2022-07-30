class Song:
  def __init__(self, title, artist, album):
    self.title = title
    self.artist = artist
    self.album = album
  
  @staticmethod
  def MakeSong(track):
    title = track['title']
    artist = ', '.join([artist['name'] for artist in track['artists']])
    album = track['album']['name'] if type(track['album']) == dict else track['album']
    return Song(title, artist, album)

  def __repr__(self):
    return "{} - {} - {}".format(self.title, self.artist, self.album)
