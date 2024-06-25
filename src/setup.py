import ytmusicapi

with open("../raw_headers.txt", "r") as f:
    raw_headers = f.read()

ytmusic = ytmusicapi.setup(filepath="../headers_auth.json", headers_raw=raw_headers)