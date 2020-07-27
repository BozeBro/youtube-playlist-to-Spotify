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
        self.public = public
        scope = ("playlist-modify-private", "playlist-modify-public")[self.public]
        scope += " user-read-private"
        self.OAuth = SpotifyOAuth(scope=scope, cache_path=cache_path)
        self.sp = spotipy.Spotify(auth_manager=self.OAuth)
        self.user_id = self.sp.current_user()["id"]
        self.access_token = self.OAuth.get_cached_token()["access_token"]
        self.playlist_id = None

    def make_playlist(
        self, name="Youtube Playlist", collaborative=False, description=""
    ):
        """
        Does the same thing as user_playlist_create() but it utilizes the request library/http reqests. 

        :param
         - name: name of playlist
            defaultis Youtube Playlist
        """
        payload = json.dumps(
            {
                "name": name,
                "public": self.public,
                "collaborative": collaborative,
                "description": description,
            }
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
        """
        Searches for a track on Spotify

        :param
         - track: The track to search for
        """
        q = track.replace(" ", "+")
        # Encode the track title
        response = self.sp.search(q, limit=5, type="track")
        # Get the first song's uri from the search
        try:
            self.track_uri = response["tracks"]["items"][0]["uri"]
        except:
            self.track_uri = False

    def add_tracks(self, playlist_name, tracks, failed, mode="w"):
        """
        Tries to add tracks onto Spotify playlist

        :param
         - tracks: tracks to add
         - failed: Will contain songs that could not have been added
         - mode: "w" when making playlist. "a" when updating playlist
        """
        for track in tracks:
            self.search_tracks(track)
            if self.track_uri:
                self.sp.user_playlist_add_tracks(
                    self.user_id, self.playlist_id, [self.track_uri]
                )
            else:
                # Have failed to find tracks for user to see
                failed.append(track)
        with open(f"failed {playlist_name}.txt", mode) as f:
            for i in failed:
                f.write(f"{i}, ")

    def get_playlist_id(self, name, **kwargs):
        playlists = self.sp.current_user_playlists(**kwargs)
        for playlist in playlists["items"]:
            if playlist["name"] == name:
                self.playlist_id = playlist["id"]
                return

    def update_playlist(self, name, tracks, **kwargs):
        self.get_playlist_id(name, **kwargs)
        try:
            with open(f"failed {name}", "r") as f:
                # Don't make an instance each iteration
                listing = next(f)
                failed = set(listing)
        except FileNotFoundError:
            listing, failed = [], set()
        tracks = list(set(tracks) - failed)
        self.add_tracks(name, tracks, listing, mode="a")


if __name__ == "__main__":
    # Testing
    public = True
    name = "Youtube Playlist"
    description = "This is a playlist from youtube made with Spotipy"
    sf = Spotify(public=public)
    # m = sf.search_tracks(track="Flashing Lights", artist="Kanye West")
    tracks = sf.sp.current_user_playlists()
    idm = tracks["items"][0].keys()
    print(idm)
# print(track)
