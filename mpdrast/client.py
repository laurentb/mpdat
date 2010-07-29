import mpd

import time
import random

import mpdrast.process as process

class MPDrastClient(mpd.MPDClient):
    def __init__(self):
        mpd.MPDClient.__init__(self)
        self.final_dirs = []


    def connect_from_env(self, host, port):
        """
        Connect from MPD_HOST (host parameter) and MPD_PORT (port parameter)
        like most MPD clients do.

        >>> from os import environ
        >>> mpd_host = environ.get("MPD_HOST", "localhost")
        >>> mpd_port = environ.get("MPD_PORT", 6600)
        >>> m = MPDrastClient()
        >>> m.connect_from_env(mpd_host, mpd_port)
        >>> m.ping()
        """
        password = None
        infos = host.split('@')
        if len(infos) == 2:
            password = infos[0]
            host = infos[1]

        self.connect(host, port)
        if password:
            self.password(password)


    def update_final_dirs(self, path="", first=True):
        """
        Compute a list of directory containing only files.
        They can be considered as full albums. Remember that MPD indexes
        only music; if a directory has subdirectories of non-music files,
        it will not prevent the directory from being added (which is good).

        If first is True, the function considers that it represents the root,
        and will clear the existing list of "final dirs". If not, it will
        append to the list. The function is recursive, hence this paratemer.
        There should be no need to call it with first=False manually.

        The root path can be any subdirectory of the database, any directory
        not in the path will be ignored.
        """
        if first:
            self.final_dirs = []

        items = self.lsinfo(path)
        if first and not items:
            raise Exception("database is empty")

        files, dirs = process.get_files_and_dirs_from_db(items)
        if len(files) and len(dirs) == 0:
            self.final_dirs.append(path)
        else:
            for dir in dirs:
                self.update_final_dirs(dir, False)


    def wait_for_update(self):
        """
        If mpd is updating the database, block until it has finished.
        """
        while self.status().has_key("updating_db"):
            time.sleep(1)


    def get_random_dir(self):
        return random.choice(self.final_dirs)


    def is_playlist_hungry(self, hungriness=100):
        return int(self.status()["playlistlength"]) < hungriness


    def is_playlist_empty(self):
        return int(self.status()["playlistlength"]) == 0


    def _find_changing_pos(self, number, type):
        pl = (process.process_song(item) for item in self.playlistinfo())
        value = None
        count = -1
        for song in pl:
            if value != song[type]:
                count = count + 1
                value = song[type]
            if count == number:
                return song["pos"]


    def clean_but(self, number=1, type="album"):
        pos = self._find_changing_pos(number, type)

        if pos:
            try:
                while True:
                    self.delete(pos)
            except mpd.CommandError:
                pass

