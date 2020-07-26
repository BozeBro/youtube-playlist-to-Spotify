from youtube_title_parse import get_artist_title
from youtube_dl import YoutubeDL


def parse_titles(titles):
    tracks, artists, failed = [], [], []
    for title in titles:
        try:
            artist, track = get_artist_title(title)
            artist, track = artist.split("(")[0], track.split("(")[0]
            if artist or track:
                artists.append(artist)
                tracks.append(track)
            else:
                raise
        except:
            failed.append(title)
    return artists, tracks, failed
