"""
I use authenticate a lot in the program, but it is really authorized not authenticated:
    the program is given certain permissions (authorize), not perceived as an actual user (authenticate).
The youtube class creates a resource object to interact with the Youtube API
    The functions goals are to
        check if authorized or not
        locate a user's id
        find the desired playlist belonging to the user
        make a container containing all the video ids
        obtain information from each video id in the container
    There are two ways that you can interact with the Youtube API
        Take the OAuth route
        Take the API_KEY route
        OAuth requires authorization from the user to access playlists
            OAuth path allows for private and public playlists
            You do not need to know your channel id
        API_KEY path only gets public playlist
            You need to know your channel id
            Less requirements to get your api_key and no need to understand OAuth ideas
            Easieir to setup and run if you want a quick script
            No need to download a clients_secrets file
"""

import os
from googleapiclient.discovery import build
import youtube_parser


class Youtube:
    def __init__(
        self,
        playlist_name,
        authenticate=None,
        api_key=None,
        playlist_id=None,
        channel_id=None,
    ):
        """
        Allows you to go two routes, API_KEY route which does not need authentication
        OAuth requres authentication (program has access to parts of your data)
        :param
        playlist_name: name of the playlist (not case sensitive)
        Required
        Choose 1
            1. authenticate: set to True if you want to go through the OAuth route
            2. api_key: api_key needed to use the youtube api. See Youtube API Docs or Corey Scafer on      creation
               channel_id: required if you go API_KEY route
        playlist_id: if you know the playlist_id, no need to search for it.
        Optional
        """
        self.authenticate = authenticate
        credentials = self.is_authenticated()
        self.playlist_name = playlist_name
        self.playlist_id = playlist_id
        self.channel_id = channel_id
        self.video_titles = []
        self.youtube_resource = build(
            "youtube", "v3", developerKey=api_key, credentials=credentials
        )

    def is_authenticated(self):
        if self.authenticate:
            # prereqs for authentication
            # YOUTUBE API sample page
            from google_auth_oauthlib import flow
            from googleapiclient import errors

            scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
            # Don't use os... = "1" in actual production code
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
            client_secrets_file = os.environ["CLIENT_SECRETS_FILE"]

            flow = flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes
            )
            return flow.run_console()

    def get_playlist(self, part="snippet", most=50):
        """
        loops through the playlist to find the desired playlist, called self.playlist_name
        """
        request = self.youtube_resource.playlists().list(
            part=part,
            mine=self.authenticate,
            channelId=self.channel_id,
            maxResults=most,
        )
        while request:
            response = request.execute()
            for playlist_id in response["items"]:
                if playlist_id["snippet"]["title"] == self.playlist_name:
                    self.playlist_id = playlist_id["id"]
                    return
            request = self.youtube_resource.playlistItems().list_next(request, response)

    def get_videos(self, part="snippet, contentDetails", most=50):
        """
        loops through a playlist to obtain all the song ids into the form self.video_ids
        """
        request = self.youtube_resource.playlistItems().list(
            part=part, playlistId=self.playlist_id, maxResults=most
        )
        self.artists, self.tracks, self.failed = [], [], []
        while request:
            response = request.execute()
            some_titles = [
                video_id["snippet"]["title"] for video_id in response["items"]
            ]
            self.video_titles.extend(some_titles)
            request = self.youtube_resource.playlistItems().list_next(request, response)

    def decor_vids(loop_videos):
        def stream(self, most=50, **kwargs):
            """
            There is a cap on values for id in loop_videos()
            stream the values at "most"values at a time
            """
            i, j = 0, 1
            while i * most < len(self.video_ids):
                some_tracks = loop_videos(self, i * most, j * most, most=most, **kwargs)
                i += 1
                j += 1

        return stream

    @decor_vids
    def get_video_info(self, start, end, part="contentDetails", most=50):
        """
        Retrieves information on a youtube video.
        id takes a comma separated list that can find info on one or more ids
        """
        request = self.youtube_resource.videos().list(
            part=part, id=",".join(self.video_ids[start:end]), maxResults=most
        )
        response = request.execute()
        return response


if __name__ == "__main__":
    # Testing
    # Obtaining the youtube class
    youtube = Youtube(
        playlist_name="Music",
        channel_id="UCPFpJ1tgPaT-hsvoaFDuuRw",
        playlist_id="PLLecTHfXLdJOwTuUCsrQd6ZujmWVP2pT_",
        api_key=os.environ["API_KEY"],
    )
    # Obtaining the specified playlist
    youtube.get_playlist()
    # Obtaining the video ids
    youtube.get_videos()
    # Obtaining info on each video
    # youtube.get_video_info()
    artists, tracks, failed = youtube_parser.parse_titles(youtube.video_titles)

