"""
The purpose of the Spotify class is to talk to the Spotify API,
to make a playlist, and add to that playlist
You will need to have Auth credentials to use this object
The Spotify API requires you to go through the OAUTH
"""

import json
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Spotify:
    def __init__(self, public=True, cache_path="spotify_tokens.json"):
        # Stores tokens in this file. Either already created or created at runtime
        self.public = public
        scope = ("playlist-modify-private", "playlist-modify-public")[self.public]
        scope += " user-read-private"
        # scope = "user-library-read"
        self.OAuth = SpotifyOAuth(scope=scope, cache_path=cache_path)
        self.sp = spotipy.Spotify(auth_manager=self.OAuth)
        self.user_id = self.sp.current_user()["id"]
        self.access_token = self.OAuth.get_cached_token()["access_token"]

    def make_playlist(self, name="Youtube Playlist", description=""):
        """
        Does the same thing as user_playlist_create() but it utilizes the request library/http reqests. 
        :param
        name: name of playlist
            defaultis Youtube Playlist
        """
        payload = json.dumps(
            {"name": name, "public": self.public, "description": description,}
        )
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        r = requests.post(
            f"https://api.spotify.com/v1/users/{self.user_id}/playlists",
            data=payload,
            headers=headers,
        )
        self.playlist_id = r.json()["id"]

    def search_tracks(self, track):
        # q = f"artist:{track}%artist:{artist}"
        q = track.replace(" ", "+")
        response = self.sp.search(q, limit=5, type="track")
        # Get the first song's uri from the search
        try:
            self.track_uri = response["tracks"]["items"][0]["uri"]
        except:
            self.track_uri = False


if __name__ == "__main__":
    # Testing
    public = True
    name = "Youtube Playlist"
    description = "This is a playlist from youtube made with Spotipy"
    sf = Spotify(public=public)

    # sf.make_playlist()
    m = sf.search_tracks(track="Flashing Lights", artist="Kanye West")
