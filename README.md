# Melon Chart to YouTube Music Playlist Auto-Generator
This project aims to automatically update YouTube Music playlists with the top 100 songs from the daily or weekly domestic Melon chart (멜론 일간차트 - 국내종합).

https://www.melon.com/chart/day/index.htm?classCd=DM0000

This project uses [ytmusicapi: Unofficial API for YouTube Music](https://ytmusicapi.readthedocs.io/en/latest/).

### Setup
1. Install [Python 3](https://www.python.org/downloads/).
2. Create a "raw_headers.txt" in the root directory with the [instructions found here](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html#copy-authentication-headers).
3. Create a "config.json" in the root directory with the following information:
```
{
    "brand_account": "<optional brand account ID>",
    "playlist": {
        "daily": {
            "url": "<playlist url>",
            "playlist_id": "<playlist id>"
        }
}
```

See the "examples/" folder for examples of how "raw_headers.txt" and "config.json" should look like.

### Usage
1. Run `cd src` to traverse into the "src" directory.
2. Run `python setup.py`. This should generate the "headers_auth.json" file in the root directory.
3. Run `python daily.py` or `python weekly.py`.

The playlist specified in the "config.json"'s `playlist_id` should now be updated with the latest songs.

### Disclaimer
The code searches YouTube Music's song catalog using a song's title, artist, and album provided by Melon. While this usually returns the correct song, there is a chance that it does not so there is a chance this script does not work 100%. This is usually because of translation listing differences between the two platforms. For example, the Melon chart may have the song title as "헤픈 우연" but YouTube Music would list the song title as "HAPPEN (헤픈 우연)". 

To mitigate such instances, the "data/manual_fixes.json" file has been added to account for problematic songs.

### To Do
- Add Top 100, ~~Weekly~~, and Monthly charts
- Use some string compare algorithm to see if the wrong song has been found and remediate automatically. This could mean searching for the album instead and searching the song in there.
- Add genre filtering options that Melon offers ![](https://i.imgur.com/D1w9RBg.png)
- Cache song results