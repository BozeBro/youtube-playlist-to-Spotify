import unittest
import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth

# Not guaranteed to work. Not maintained or updated


class Spotify(unittest.TestCase):
    def setUp(self):
        scope = "user-library-read"
        OAuth = SpotifyOAuth(scope=scope, cache_path="token_locations.json")
        self.sp = spotipy.Spotify(auth_manager=OAuth)

    def test_Oconnect(self):
        results = None
        results = self.sp.current_user_saved_tracks()
        self.assertEqual(type(results["items"]), list)

    def test_make_playlist(
        self, name="Youtube Playlist", public="True", collaborative="False"
    ):
        payload = json.dumps(
            {"name": name, "public": public, "collaborative": collaborative}
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
        self.assertEqual(r.ok, True)
        self.assertEqual(type(self.playlist_id), str)
        print(r.status)


if __name__ == "__main__":
    unittest.main()
