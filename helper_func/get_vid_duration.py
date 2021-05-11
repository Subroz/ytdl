# (c) Aryan Vikash & @AbirHasan2005

from helper_func.get_vid_data import probe


def duration(vid_file_path):
    """
    Video's duration in seconds, return a float number
    """
    _json = probe(vid_file_path)
    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])
        else:
            return 400
    elif 'streams' in _json:
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])
            else:
                return 400
    else:
        return 400
