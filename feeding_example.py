#!/usr/bin/env python3
from os import environ

from mpdat import MPDatClient

mpd_host = environ.get("MPD_HOST", "localhost")
mpd_port = environ.get("MPD_PORT", 6600)

m = MPDatClient()
m.connect_from_env(mpd_host, mpd_port)

# the user can run mpc update before; wait for completion
m.wait_for_update()

# get all "final" directories
nb_dirs = len(m.get_final_dirs())
print("We have found %s albums." % nb_dirs)

# if the playlist is empty, add one random album
while m.is_playlist_hungry(100) and nb_dirs:
    rdir = m.get_random_dir()
    m.add(rdir)
    print("Added %s" % rdir)

print(m.status())
print(m.stats())
