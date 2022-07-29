class Song:
  def __init__(self, title, artist, album):
    self.title = title
    self.artist = artist
    self.album = album

  def __repr__(self):
    return "{} - {} - {}".format(self.title, self.artist, self.album)
