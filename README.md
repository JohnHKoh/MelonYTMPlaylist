# Melon Chart to YouTube Music Playlist Auto-Generator
This project aims to automatically update YouTube Music playlists with the top 100 songs from the daily domestic Melon chart (멜론 일간차트 - 국내종합).

https://www.melon.com/chart/day/index.htm?classCd=DM0000

This project uses [ytmusicapi: Unofficial API for YouTube Music](https://ytmusicapi.readthedocs.io/en/latest/).

## Usage
1. Install [Python 3](https://www.python.org/downloads/).
2. Create a "raw_headers.txt" in the root directory with the [instructions found here](https://ytmusicapi.readthedocs.io/en/latest/setup.html#copy-authentication-headers).
3. Run `python setup.py`. This should generate the "headers_auth.json" file.
4. Create a "config.json" with the following information:
```
{
    "brand_account": "<optional brand account ID>",
    "playlist_id": "<playlist ID to update>"
}
```
5. Run `python daily.py`.
6. The playlist specified in the "config.json"'s `playlist_id` should now be updated with the latest songs.