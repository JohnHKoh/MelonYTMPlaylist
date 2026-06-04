import melon_retriever
from playlist_updater import PlaylistUpdater
from datetime import date, timedelta
from chart import Chart

listName = "weekly"
today = date.today()
past_monday = today - timedelta(days=today.weekday(), weeks=1)
past_sunday = past_monday + timedelta(days=6)
date_str = "{past_monday} ~ {past_sunday}".format(past_monday=past_monday.strftime("%Y.%m.%d"), past_sunday=past_sunday.strftime("%Y.%m.%d"))
description = """
Melon(Korean: 멜론) is a South Korean online music store and music streaming service. 
They have a weekly chart of the top 100 songs that reflects streaming 40% + download 60% of weekly service usage. This is the weekly(주간) chart of Korean domestic songs(국내종합).

{playlist_url}

Updated for: {date}

This playlist is auto-generated.
View the code here: https://github.com/JohnHKoh/MelonYTMPlaylist
"""
PlaylistUpdater().update_playlist(Chart(listName, None, description, date_str))