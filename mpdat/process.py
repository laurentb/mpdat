from os.path import dirname

"""
Process MPDatClient responses
"""


def get_files_and_dirs_from_db(items):
    """
    Returns (files, directories) from a source with files and directories mixed.
    """
    files = []
    dirs = []
    for item in items:
        if "directory" in item:
            dirs.append(item["directory"])
        elif "file" in item:
            files.append(item["file"])

    return (files, dirs)


def process_song(item):
    """
    Adds a "dir" attribute to songs, change "pos" to int
    """
    if "file" in item:
        item["dir"] = dirname(item["file"])
    if "pos" in item:
        item["pos"] = int(item["pos"])
    if "time" in item:
        item["time"] = int(item["time"])

    return item
