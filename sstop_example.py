#!/usr/bin/env python
from mpdat import MPDatClient
from os import environ

mpd_host = environ.get("MPD_HOST", "localhost")
mpd_port = environ.get("MPD_PORT", 6600)

m = MPDatClient()
m.connect_from_env(mpd_host, mpd_port)

m.single_stop()
