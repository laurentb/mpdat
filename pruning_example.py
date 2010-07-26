#!/usr/bin/env python
from mpdrast import MPDrastClient

from os import environ

mpd_host = environ.get("MPD_HOST", "localhost")
mpd_port = environ.get("MPD_PORT", 6600)

m = MPDrastClient()
m.connect_from_env(mpd_host, mpd_port)

# Keep only one album in the playlist
m.clean_but(1, "album")

