#!/usr/bin/env python
import mpdrast
from os import environ

mpd_host = environ.get("MPD_HOST", "localhost")
mpd_port = environ.get("MPD_PORT", 6600)

m = mpdrast.MPDrastClient()
m.connect(mpd_host, mpd_port)

# the user can run mpc update before; wait for completion
m.wait_for_update()

# get all "final" directories
m.update_final_dirs("")

# if the playlist is empty, add one random album
if m.is_playlist_hungry(1):
  m.add(m.get_random_dir())

print m.status()
