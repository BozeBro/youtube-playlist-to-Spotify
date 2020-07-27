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

class Playlist(object):
    def __init__(self, spotify={}, youtube={}):
        """
        make a resource to talk to spotify api and youtube api
        see spotify.py for params
        see youtube.py for params
        """
        self.sf = Spotfy(**spotify)
        self.yt = Youtube(**youtube_parser)
    def handle_playlist(self, func, sf_playlist="", description="", mode="w", **kwargs):
        """
        Handles making and updating a playlist
        if making playlist, func=sf.add_tracks, mode="w", failed=[]
        if updating a playlist, func=sf.update, mode ="r"
        """
        if func == self.sf.add_tracks:
            self.sf.playlist_id = sf.sp.user_playlist_create(
                self.sf.user_id, name=sf_playlist, public=sf.public, description=description
            )["id"]
        yt.get_playlist()
        yt.get_videos()
        tracks = youtube_parser.second_parser(yt.video_titles)
        func(spotify_playlist, tracks, mode, **kwargs)

if __name__ == "__main__":
    playlist = Playlist(spotify={"public": True}, youtube={"authenticate":True, "playlist_name": "Music"})
    playlist.handle_playlist(playlist.sf.update_playlist, sf_playlist="Music", mode="a")
