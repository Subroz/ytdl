# (c) Aryan Vikash & @AbirHasan2005

import subprocess as sp
import json


def probe(vid_file_path):
    """
    Give a json from ffprobe command line
    @vid_file_path : The absolute (full) path of the video file, string.
    """
    if type(vid_file_path) != str:
        raise Exception('Give ffprobe a full file path of the file')

    command = [
        "ffprobe",
        "-loglevel", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        vid_file_path
    ]

    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()
    return json.loads(out)
