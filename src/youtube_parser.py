from youtube_title_parse import get_artist_title

def get_song_credentials(titles):
    # Parses titles into artist, track categories
    # Deprecrated
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

def title_parser(titles):
    # Removes unneccessary text that would throw off Spotify search
    # Much more effective than get_song_credentials
    # Preffered function
    return [title]
    track_titles = []
    for title in titles:
        title = title.split("[")[0]
        title = title.split("(")[0]
        title = title.split("lyrics")[0]
        title = title.split("remix")[0]
        title = title.split("version")[0]
        track_titles.append(title)
    return track_titles


