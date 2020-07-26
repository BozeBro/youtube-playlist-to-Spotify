# Youtube imports
import os
from googleapiclient.discovery import build

# Spotify imports
import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 3rd part parser
import youtube_title_parse

# File imports
import youtube_parser
from youtube import Youtube
import spotify


def main():
    public = True
    # Create the playlist
    spotify_playlist = "Automated Spotify Playlist"
    description = "My Youtube Playlist in Spotify using Python. All songs transported not guaranteed"
    sf = spotify.Spotify(public=public)
    sf.playlist_id = sf.sp.user_playlist_create(
        sf.user_id, name=spotify_playlist, public=sf.public, description=description
    )["id"]
    # Get the specified youtube playlist and its video titles
    playlist_name = "Music"
    authenticate = True
    yt = Youtube(playlist_name=playlist_name, authenticate=authenticate)
    yt.get_playlist()
    yt.get_videos()
    # parse video titles
    tracks = youtube_parser.second_parser(yt.video_titles)
    failed = []
    # Search for songs on Spotify
    for track in tracks:
        sf.search_tracks(track=track)
        if sf.track_uri:
            sf.sp.user_playlist_add_tracks(sf.user_id, sf.playlist_id, [sf.track_uri])
        else:
            # Have failed to find tracks for user to see
            failed.append(track)
    # List of songs that did not get added
    # Allow to manually add unadded songs
    with open(f"failed {spotify_playlist}.txt", "w") as f:
        for i in failed:
            f.write(f"{i}, ")


if __name__ == "__main__":
    main()
