from django.shortcuts import render
import plotly.express as px
import pandas as pd
from django.utils.safestring import mark_safe
from . forms import ArtistForm

# Path to your dataset
DATASET_PATH = '/Users/asheshlalshrestha/Desktop/Datanal/Project/DMQL-Project/project/final_dataset.csv'


def generate_chart1_data(df):
    # Bar Chart: Number of Tracks by Artist
    artist_track_counts = (
        df.groupby('Artist')['Track']
        .count()
        .reset_index(name='Counts')
        .sort_values(by='Counts', ascending=False).head(10)
    )

    fig_bar = px.bar(
        artist_track_counts,
        x='Artist',
        y='Counts',
        title='Top 10 artists witht the most tracks',
        labels={'Counts': 'Number of Tracks', 'Artist': 'Artist'},
        text='Counts'
    )
    fig_bar.update_layout(
        xaxis={'categoryorder': 'total descending'},  # Order by count
        title_x=0.5  # Center the title
    )
    fig_bar.update_traces(textposition='outside')  # Position text outside bars

    # Convert Bar Chart to HTML
    bar_chart = fig_bar.to_html(full_html=False, include_plotlyjs=False)

    return bar_chart

def generate_chart2_data(df):
    # Get value counts and reset index for the 'Explicit Track' column
    explicit_track_counts = df['Explicit Track'].value_counts().reset_index(name='Counts')
    explicit_track_counts.rename(columns={'index': 'Explicit Track'}, inplace=True)

    # Create the pie chart
    fig = px.pie(
        explicit_track_counts,
        names='Explicit Track',
        values='Counts',
        title='Distribution of Explicit Tracks',
        labels={'Explicit Track': 'Explicit Track', 'Counts': 'Number of Tracks'},
        hole=0.3  # Optional: To make it a donut chart
    )

    # Update layout for better visual appeal
    fig.update_layout(title_x=0.5)  # Center the title

    # Convert chart to HTML
    pie_chart = fig.to_html(full_html=False, include_plotlyjs=False)

    return pie_chart

def generate_chart3_data(df):
    # Convert 'Release Date' to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df['Release Date']):
        df['Release Date'] = pd.to_datetime(df['Release Date'])

    # Extract the year and month from 'Release Date' and convert to string
    df['Release Month'] = df['Release Date'].dt.to_period('M').astype(str)

    # Group by Release Month and count the number of tracks
    monthly_track_counts = df.groupby('Release Month').size().reset_index(name='Track Count')

    # Create the line chart
    fig = px.line(
        monthly_track_counts,
        x='Release Month',
        y='Track Count',
        title='Number of Tracks Released by Month',
        labels={'Release Month': 'Month', 'Track Count': 'Number of Tracks'}
    )

    # Update layout for better visual appeal
    fig.update_layout(title_x=0.5)  # Center the title

    # Convert chart to HTML
    line_chart = fig.to_html(full_html=False, include_plotlyjs=False)

    return line_chart
    
def generate_chart4_data(df):
    # Ensure 'Release Date' is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['Release Date']):
        df['Release Date'] = pd.to_datetime(df['Release Date'])

    # Group by 'Release Date' and sum the 'Spotify Streams'
    total_streams = df.groupby('Release Date')['Spotify Streams'].sum().reset_index(name='Total Streams')

    # Create the line chart
    fig = px.line(
        total_streams,
        x='Release Date',
        y='Total Streams',
        title='Total Spotify Streams by Release Date',
        labels={'Release Date': 'Release Date', 'Total Streams': 'Total Spotify Streams'}
    )

    # Update layout for better visual appeal
    fig.update_layout(title_x=0.5)  # Center the title

    # Convert chart to HTML
    line_chart = fig.to_html(full_html=False, include_plotlyjs=False)

    return line_chart

def generate_chart5_data(df):
    # Create 'popularity_streams' column
    df['popularity_streams'] = df['Spotify Streams'] + df['YouTube Views'] + df['TikTok Views']

    # Group by Artist and sum the 'popularity_streams' for each
    artist_popularity = df.groupby('Artist')['popularity_streams'].sum().reset_index(name='counts').head(10)

    # Sort by 'counts' in descending order
    artist_popularity_sorted = artist_popularity.sort_values(by='counts', ascending=False)

    # Create the bar chart
    fig = px.bar(
        artist_popularity_sorted,
        x='Artist',
        y='counts',
        title='Artists with most streams on Tiktok, Youtube and Spotify (combined)',
        labels={'counts': 'Total Popularity Streams', 'Artist': 'Artist'},
        text='counts'  # Show the count values on the bars
    )

    # Update layout for better visual appeal
    fig.update_layout(
        xaxis={'categoryorder': 'total descending'},  # Order bars by total popularity
        title_x=0.5  # Center the title
    )
    fig.update_traces(textposition='outside')  # Position text outside bars

    # Convert chart to HTML for rendering
    bar_chart = fig.to_html(full_html=False, include_plotlyjs=False)

    return bar_chart


def render_combined_charts(request):
    # Load data into a DataFrame
    try:
        df = pd.read_csv(DATASET_PATH)
    except Exception as e:
        return render(request, 'app/error.html', {'error': f"Failed to load data: {e}"})

    # Generate the chart
    chart1 = generate_chart1_data(df)
    chart2 = generate_chart2_data(df)
    chart3 = generate_chart3_data(df)
    chart4 = generate_chart4_data(df)
    chart5 = generate_chart5_data(df)



    # Pass chart to the context
    context = {
        'chart1': mark_safe(chart1),
        'chart2': mark_safe(chart2),
        'chart3': mark_safe(chart3),
        'chart4': mark_safe(chart4),
        'chart5': mark_safe(chart5),


    }
    return render(request, 'app/chart.html', context)



def generate_custom_chart1_data(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        
        if form.is_valid():
            artist_name = form.cleaned_data['artist']  # Get artist name from form
            print(f"Selected Artist: {artist_name}")  # Print the artist name
            
            # Load the dataset into a pandas DataFrame
            df = pd.read_csv(DATASET_PATH)
            
            # Filter the DataFrame based on the selected artist
            artist_df = df[df['Artist'] == artist_name]
            
            # Create a new DataFrame with summed values for the specific artist
            artist_data = artist_df[['Artist', 'Spotify Streams', 'YouTube Views', 'TikTok Views']].sum()
            
            # Print the filtered data for debugging
            print(f"Data for artist {artist_name}:")
            print(artist_data)
            
            # Generate the bar chart
            bar_fig = px.bar(
                artist_data,
                x=artist_data.index,
                y=artist_data.values,
                title=f'Streams & Views for {artist_name}',
                labels={'x': 'Platform', 'y': 'Count'},
                text=artist_data.values  # Display values on bars
            )
            bar_fig.update_layout(title_x=0.5, xaxis={'categoryorder': 'total descending'})
            bar_fig.update_traces(textposition='outside')  # Display values outside bars
            
            # Convert the bar chart to HTML for rendering
            bar_chart = bar_fig.to_html(full_html=False, include_plotlyjs=False)
            
            # Create a new column 'total_streams_views' that sums the streams and views across platforms
            artist_df['total_streams_views'] = artist_df['Spotify Streams'] + artist_df['YouTube Views'] + artist_df['TikTok Views']
            
            # Generate the pie chart
            pie_fig = px.pie(
                artist_df,
                names='Track',  # Names of each track
                values='total_streams_views',  # The total streams/views for each track
                title=f'Distribution of Streams & Views by Track for {artist_name}',
                labels={'total_streams_views': 'Total Streams & Views'},
            )
            pie_fig.update_layout(title_x=0.5)
            
            # Convert the pie chart to HTML for rendering
            pie_chart = pie_fig.to_html(full_html=False, include_plotlyjs=False)
            
            # Scatter plot for tracks released over time
            scatter_data = artist_df.groupby('Release Date').count()['Track']
            scatter_fig_1 = px.scatter(
                x=scatter_data.index,
                y=scatter_data.values,
                title=f"Tracks Released Over Time for {artist_name}",
                labels={'x': 'Release Date', 'y': 'Number of Tracks'},
                hover_name=scatter_data.index
            )
            scatter_fig_1.update_layout(title_x=0.5)
            
            # Convert the scatter plot for release dates to HTML
            scatter_chart_1 = scatter_fig_1.to_html(full_html=False, include_plotlyjs=False)
            
            # Scatter plot showing the distribution of tracks with respect to total streams/views
            scatter_fig_2 = px.scatter(
                artist_df,
                x='Spotify Streams',
                y='YouTube Views',
                size='TikTok Views',  # Size of points based on TikTok Views
                color='Track',  # Color by track
                hover_name='Track',
                title=f"Track Comparison for {artist_name}",
                labels={'x': 'Spotify Streams', 'y': 'YouTube Views'}
            )
            scatter_fig_2.update_layout(title_x=0.5)
            
            # Convert the second scatter plot to HTML
            scatter_chart_2 = scatter_fig_2.to_html(full_html=False, include_plotlyjs=False)
            
            # Pass all charts and form to the template
            return render(request, 'app/customize_chart.html', {
                'form': form,
                'artist_name': artist_name,
                'bar_chart': bar_chart,
                'pie_chart': pie_chart,
                'scatter_chart_1': scatter_chart_1,  # Tracks Released Over Time
                'scatter_chart_2': scatter_chart_2   # Track Comparison (Spotify, YouTube, TikTok)
            })
    else:
        form = ArtistForm()
    
    return render(request, 'app/customize_chart.html', {'form': form})

