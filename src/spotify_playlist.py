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
    spotify_playlist = "My Youtube Playlist try #5"
    description = "My Youtube Playlist in Spotify using Python"
    sf = spotify.Spotify(public=public)
    sf.playlist_id = sf.sp.user_playlist_create(
        sf.user_id, name=spotify_playlist, public=sf.public, description=description
    )["id"]
    # Get the youtube playlist and its video titles
    playlist_name = "Music"
    authenticate = True
    yt = Youtube(playlist_name=playlist_name, authenticate=authenticate)
    yt.get_playlist()
    yt.get_videos()
    artists, tracks, failed = youtube_parser.parse_titles(yt.video_titles)
    # Search for songs on Spotify
    fail = 0
    for artist, track in zip(artists, tracks):
        try:
            sf.search_tracks(artist=artist, track=track)
            sf.sp.user_playlist_add_tracks(sf.user_id, sf.playlist_id, sf.track_uri)
        except:
            print(sf.track_uri)
            fail += 1
    # List of songs that did not get added
    # Allow to manually add unadded songs
    print(fail)
    with open(f"failed {spotify_playlist}.txt", "w") as filed:
        for i in failed:
            filed.write(f"{i}, ")


if __name__ == "__main__":
    main()
