#!/usr/bin/env python
from mpdat import MPDatClient
from os import environ

import datetime


def humandelta(seconds):
    return str(datetime.timedelta(seconds=seconds))

BRIGHT = '\x1b[1m'
NORMAL = '\x1b[22m'

mpd_host = environ.get("MPD_HOST", "localhost")
mpd_port = environ.get("MPD_PORT", 6600)

m = MPDatClient()
m.connect_from_env(mpd_host, mpd_port)


for time, album in m.get_playlist_albums_time():
    print '%s: %s%s%s' % (album[0]["dir"], BRIGHT, humandelta(time), NORMAL)

print
print 'TOTAL: %s%s%s' % (BRIGHT, humandelta(m.get_playlist_time()), NORMAL)
