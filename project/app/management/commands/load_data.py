# import_data.py
import csv
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from app.models import Dash


class Command(BaseCommand):
    help = 'Load data from file into Dash model'
    
    def handle(self, *args, **kwargs):
        # Define the path to your CSV file
        datafile = settings.BASE_DIR / 'Data' / 'final_dataset.csv'  # Adjust the file name as necessary
        
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    # Parse date
                    Release_Date = datetime.strptime(row['Release Date'], '%Y-%m-%d').date()
                except ValueError as e:
                    print(f"Error parsing date: {e}. Skipping this row.")
                    continue  # Skip to the next row

                try:
                    # Convert numeric fields
                    All_Time_Rank = int(row['All Time Rank'])
                    Track_Score = float(row['Track Score'])
                    Spotify_Streams = float(row['Spotify Streams'].replace(',', ''))  # Handle commas in numbers
                    Spotify_Playlist_Count = float(row['Spotify Playlist Count'].replace(',', ''))
                    Spotify_Playlist_Reach = float(row['Spotify Playlist Reach'].replace(',', ''))
                    Spotify_Popularity = float(row['Spotify Popularity'])
                    YouTube_Views = float(row['YouTube Views'].replace(',', ''))
                    YouTube_Likes = float(row['YouTube Likes'].replace(',', ''))
                    TikTok_Posts = float(row['TikTok Posts'].replace(',', ''))
                    TikTok_Likes = float(row['TikTok Likes'].replace(',', ''))
                    TikTok_Views = float(row['TikTok Views'].replace(',', ''))
                    YouTube_Playlist_Reach = float(row['YouTube Playlist Reach'].replace(',', ''))
                    Apple_Music_Playlist_Count = float(row['Apple Music Playlist Count'])
                    AirPlay_Spins = float(row['AirPlay Spins'].replace(',', ''))
                    SiriusXM_Spins = float(row['SiriusXM Spins'].replace(',', ''))
                    Deezer_Playlist_Count = float(row['Deezer Playlist Count'])
                    Deezer_Playlist_Reach = float(row['Deezer Playlist Reach'].replace(',', ''))
                    Amazon_Playlist_Count = float(row['Amazon Playlist Count'])
                    Pandora_Streams = float(row['Pandora Streams'].replace(',', ''))
                    Pandora_Track_Stations = float(row['Pandora Track Stations'].replace(',', ''))
                    Soundcloud_Streams = float(row['Soundcloud Streams'].replace(',', ''))
                    Shazam_Counts = float(row['Shazam Counts'].replace(',', ''))
                    TIDAL_Popularity = float(row['TIDAL Popularity'])
                    Explicit_Track = int(row['Explicit Track'])
                except ValueError as e:
                    print(f"Error parsing numeric values: {e}. Skipping this row.")
                    continue  # Skip to the next row

                # Create Dash object with processed values
                Dash.objects.create(
                    Track=row['Track'],
                    Album_Name=row['Album Name'],
                    Artist=row['Artist'],
                    Release_Date=Release_Date,
                    ISRC=row['ISRC'],
                    All_Time_Rank=All_Time_Rank,
                    Track_Score=Track_Score,
                    Spotify_Streams=Spotify_Streams,
                    Spotify_Playlist_Count=Spotify_Playlist_Count,
                    Spotify_Playlist_Reach=Spotify_Playlist_Reach,
                    Spotify_Popularity=Spotify_Popularity,
                    YouTube_Views=YouTube_Views,
                    YouTube_Likes=YouTube_Likes,
                    TikTok_Posts=TikTok_Posts,
                    TikTok_Likes=TikTok_Likes,
                    TikTok_Views=TikTok_Views,
                    YouTube_Playlist_Reach=YouTube_Playlist_Reach,
                    Apple_Music_Playlist_Count=Apple_Music_Playlist_Count,
                    AirPlay_Spins=AirPlay_Spins,
                    SiriusXM_Spins=SiriusXM_Spins,
                    Deezer_Playlist_Count=Deezer_Playlist_Count,
                    Deezer_Playlist_Reach=Deezer_Playlist_Reach,
                    Amazon_Playlist_Count=Amazon_Playlist_Count,
                    Pandora_Streams=Pandora_Streams,
                    Pandora_Track_Stations=Pandora_Track_Stations,
                    Soundcloud_Streams=Soundcloud_Streams,
                    Shazam_Counts=Shazam_Counts,
                    TIDAL_Popularity=TIDAL_Popularity,
                    Explicit_Track=Explicit_Track
                )
                print(f"Inserted: {row['Track']} by {row['Artist']}")