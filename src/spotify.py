import json
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
cache_path = 'token_locations.json'
class Spotify(object):
    def __init__(self, public=True, cache_path=cache_path):
        scope = ("playlist-modify-private", "playlist-modify-public")[public]
        #scope = "user-library-read"
        self.OAuth = SpotifyOAuth(scope=scope, cache_path=cache_path)
        self.sp = spotipy.Spotify(auth_manager=self.OAuth)
        self.user_id = self.sp.current_user()['id']
        self.access_token = self.OAuth.get_cached_token()["access_token"] 
    def make_playlist(self, name="Youtube Playlist", **kwargs):
        """
        Does the same thing as user_playlist_create() but it utilizes the request library/http reqests. 
        :param
        name: name of playlist
            defaultis Youtube Playlist
        **kwargs: all kwargs are passed into payload
        """
        payload = json.dumps({
            "name": name,
            **kwargs
        })
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        r = requests.post(f"https://api.spotify.com/v1/users/{self.user_id}/playlists", data=payload, headers=headers)
        self.playlist_id = r.json()["id"]
if __name__ == "__main__":
    public = True
    name = "Youtube Playlist"
    description = "This is a playlist from youtube made with Spotipy"
    sf = Spotify(public=public)
    #sf.find_playlist()
    #sf.make_playlist(name=name, description=description, public=str(public))
    sf.playlist_id = sf.sp.user_playlist_create(user=sf.user_id, name=name, public=public, description=description)
    # sf.sp.user_playlist_add_tracks(user=sf.user_id, # playlist_id="fill", tracks=['https://www.youtube.com/watch?# v=FSnuF1FPSIU&list=RDFSnuF1FPSIU&start_radio=1'])