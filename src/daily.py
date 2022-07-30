import melon_retriever
from playlist_updater import PlaylistUpdater

songs = melon_retriever.get_daily()
description = """
Melon(Korean: 멜론) is a South Korean online music store and music streaming service. 
They have a daily chart of the top 100 songs that reflects streaming 40% + download 60% of weekly service usage. This is the daily(일간) chart of Korean domestic songs(국내종합).

{playlist_url}

Updated for: {today}

This playlist is auto-generated.
View the code here: https://github.com/JohnHKoh/MelonYTMPlaylist
"""
PlaylistUpdater().update_playlist(songs, "daily", description)
