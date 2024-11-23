from django import forms
import pandas as pd

# Path to your dataset
DATASET_PATH = '/Users/asheshlalshrestha/Desktop/Datanal/Project/DMQL-Project/project/final_dataset.csv'

class ArtistForm(forms.Form):
    # Load the dataset into a pandas DataFrame
    df = pd.read_csv(DATASET_PATH)
    
    # Extract distinct artists from the 'Artist' column
    artists = df['Artist'].dropna().unique()
    
    # Create the choices list for the dropdown
    artist_choices = [(artist, artist) for artist in artists]
    
    # Create the ChoiceField with the artist choices
    artist = forms.ChoiceField(choices=artist_choices)
