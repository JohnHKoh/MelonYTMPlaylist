from ytmusicapi import YTMusic

with open("../raw_headers.txt", "r") as f:
    raw_headers = f.read()

ytmusic = YTMusic.setup(filepath="../headers_auth.json", headers_raw=raw_headers)