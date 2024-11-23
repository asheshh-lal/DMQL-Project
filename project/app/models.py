from django.db import models

class Dash(models.Model):
    # Basic Information
    Track = models.CharField(max_length=255)  # Track Name
    Album_Name = models.CharField(max_length=100)  # Album Name
    Artist = models.CharField(max_length=100)  # Artist Name
    Release_Date = models.DateField()  # Release Date
    ISRC = models.CharField(max_length=100)  # ISRC code

    # Rank and Scores
    All_Time_Rank = models.IntegerField()  # All Time Rank
    Track_Score = models.FloatField()  # Track Score

    # Spotify Data
    Spotify_Streams = models.FloatField()  # Spotify Streams
    Spotify_Playlist_Count = models.FloatField()  # Spotify Playlist Count
    Spotify_Playlist_Reach = models.FloatField()  # Spotify Playlist Reach
    Spotify_Popularity = models.FloatField()  # Spotify Popularity

    # YouTube Data
    YouTube_Views = models.FloatField()  # YouTube Views
    YouTube_Likes = models.FloatField()  # YouTube Likes
    YouTube_Playlist_Reach = models.FloatField()  # YouTube Playlist Reach

    # TikTok Data
    TikTok_Posts = models.FloatField()  # TikTok Posts
    TikTok_Likes = models.FloatField()  # TikTok Likes
    TikTok_Views = models.FloatField()  # TikTok Views

    # Apple Music Data
    Apple_Music_Playlist_Count = models.FloatField()  # Apple Music Playlist Count

    # AirPlay and SiriusXM Data
    AirPlay_Spins = models.FloatField()  # AirPlay Spins
    SiriusXM_Spins = models.FloatField()  # SiriusXM Spins

    # Deezer Data
    Deezer_Playlist_Count = models.FloatField()  # Deezer Playlist Count
    Deezer_Playlist_Reach = models.FloatField()  # Deezer Playlist Reach

    # Amazon Data
    Amazon_Playlist_Count = models.FloatField()  # Amazon Playlist Count

    # Pandora Data
    Pandora_Streams = models.FloatField()  # Pandora Streams
    Pandora_Track_Stations = models.FloatField()  # Pandora Track Stations

    # SoundCloud Data
    Soundcloud_Streams = models.FloatField()  # Soundcloud Streams
    Shazam_Counts = models.FloatField()  # Shazam Counts

    # TIDAL Data
    TIDAL_Popularity = models.FloatField()  # TIDAL Popularity

    # Explicit Track (binary: 0 or 1)
    Explicit_Track = models.IntegerField()  # Explicit Track (0 or 1)

    def __str__(self):
        return f'{self.Track} - {self.Album_Name} - {self.Artist}'
