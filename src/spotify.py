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
        self.fail_add = []
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

    def search_tracks(self, track, artist):
        # query parameters
        q = f"{track}&{artist}"
        response = self.sp.search(q, limit=5, type="track")
        # Get the first song's uri from the search
        self.track_uri = response["tracks"]["items"][0]["uri"]
    def search_tracker(self, track, artist):
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            track,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.access_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # only use the first song
        try:
            self.track_uri = songs[0]["uri"]
        except:
            self.track_uri = ""
    def add_tracks(self):
        pass


if __name__ == "__main__":
    # Testing
    public = False
    name = "Youtube Playlist"
    description = "This is a playlist from youtube made with Spotipy"
    sf = Spotify(public=public)
    playlist_id = sf.sp.user_playlist_create(
        sf.user_id, name="billy bobs", public=public, description=description
    )

    # sf.make_playlist()
    m = sf.search_tracker(track="Flashing Lights", artist="Kanye West")
    print(sf.track_uri)
    # sf.sp.user_playlist_add_tracks(sf.user_id, sf.playlist_id, sf.track_uri)
