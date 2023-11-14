import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load data from CSV
# Assuming the CSV file has columns 'MovieName', 'MovieYear', and 'MovieRating'
df = pd.read_csv('top250_movies.csv')

# Sort data chronologically
df = df.sort_values(by=['MovieYear', 'MovieRating'], ascending=[True, False])

# Initialize the plot
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar([], [], color='blue')

# Set plot properties
ax.set_title('Top 10 Movies (Updated Yearly)')
ax.set_xlabel('Movie Ranking')
ax.set_ylabel('Movie Rating')
ax.set_xlim(0.5, 10.5)  # Adjust x-axis limits to match the movie ranking
ax.set_ylim(0, 10)

# Initialize variables for tracking top movies
top_movies = pd.DataFrame(columns=df.columns)

# Update function for animation
def update(frame):
    global top_movies
    
    plt.cla()  # Clear the previous plot
    
    # Get the top 10 movies of all time up to the current year
    top_movies = df[df['MovieYear'] <= (frame + 1950)].groupby('MovieName').apply(lambda x: x.nlargest(1, 'MovieRating')).reset_index(drop=True).nlargest(10, 'MovieRating')
    
    # Plot only the top 10 movies with movie names
    bars = ax.bar(range(1, 11), top_movies['MovieRating'], color='blue')
    for bar, movie_ranking, movie_rating, movie_name in zip(bars, range(1, 11), top_movies['MovieRating'], top_movies['MovieName']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{movie_name}\nRating: {movie_rating}",
                ha='center', va='bottom', rotation=45, fontsize=8)
    
    ax.set_title('Top 10 Movies (Updated Yearly)')
    ax.set_xlabel('Movie Ranking')
    ax.set_ylabel('Movie Rating')
    ax.set_xlim(0.5, 10.5)
    ax.set_ylim(0, 10)
    
    print(f"Processing year: {frame + 1950}, Top movies: {top_movies['MovieName'].tolist()}")

    # Check if the animation should stop
    if frame + 1950 >= 2023:
        animation.event_source.stop()
        print("Animation stopped at year 2023.")

# Create animation
animation = FuncAnimation(fig, update, frames=len(df['MovieYear'].unique()), repeat=False)

# Save the animation as a video using FFmpeg
animation.save('top_movies_animation.mp4', writer='ffmpeg', fps=2)

# Show the plot (optional)
plt.show()
