# Melon Chart to YouTube Music Playlist Auto-Generator
This project aims to automatically update YouTube Music playlists with the top 100 songs from the daily domestic Melon chart (멜론 일간차트 - 국내종합).

https://www.melon.com/chart/day/index.htm?classCd=DM0000

This project uses [ytmusicapi: Unofficial API for YouTube Music](https://ytmusicapi.readthedocs.io/en/latest/).

### Setup
1. Install [Python 3](https://www.python.org/downloads/).
2. Create a "raw_headers.txt" in the root directory with the [instructions found here](https://ytmusicapi.readthedocs.io/en/latest/setup.html#copy-authentication-headers).
3. Create a "config.json" in the root directory with the following information:
```
{
    "brand_account": "<optional brand account ID>",
    "playlist_id": "<playlist ID to update>"
}
```

See the "examples/" folder for examples of how "raw_headers.txt" and "config.json" should look like.

### Usage
1. Run `cd src` to traverse into the "src" directory.
2. Run `python setup.py`. This should generate the "headers_auth.json" file in the root directory.
3. Run `python daily.py`.

The playlist specified in the "config.json"'s `playlist_id` should now be updated with the latest songs.