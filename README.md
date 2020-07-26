# youtube-playlist-to-Spotify

This code will try to put all the songs from a youtube playlist into spotify. 
There are plans to have an update feature to add new songs in the future. (NOT GUARANTEED).

# Parsing

Much difficulty in transferring songs from youtube into spotify is trying to parse out youtube's flexible guidelines for song titles and listings of song names and artists. Youtube's API does not offer song name or artist so one has to manually parse evey video.

See youtube_parser.py for the main() function.

# Requirements

You will need to create OAUTH credentials for both Youtube API and Spotify API in order to use them. Store the credentials in a file or an environment variable.
