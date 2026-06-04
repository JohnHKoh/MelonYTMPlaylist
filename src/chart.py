import melon_retriever

class Chart:

  def __init__(self, listName:str, title: str, description: str, date_str: str):
    self.songs = melon_retriever.get_songs(listName)
    self.listName = listName
    self.title = title
    self.description = description
    self.date_str = date_str