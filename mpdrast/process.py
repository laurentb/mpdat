from os.path import dirname

"""
Process MPDrastClient responses
"""

def get_files_and_dirs_from_db(items):
    """
    Returns (files, directories) from a source with files and directories mixed.
    """
    files = []
    dirs = []
    for item in items:
        if item.has_key("directory"):
            dirs.append(item["directory"])
        elif item.has_key("file"):
            files.append(item["file"])

    return (files, dirs)

def process_song(item):
    """
    Adds a "dir" attribute to songs, change "pos" to int
    """
    if item.has_key("file"):
        item["dir"] = dirname(item["file"])

    if item.has_key("pos"):
        item["pos"] = int(item["pos"])

    return item
