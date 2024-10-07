import os
import praw

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    username=os.getenv('USERNAME'),
    password=os.getenv('PASSWORD'),
    user_agent='Wallpaper Posting Bot v1.0'
)

# Subreddit you want to post to
subreddit = reddit.subreddit(os.getenv('SUBREDDIT'))

# Directories where wallpapers are stored
wallpapers_dirs = ["plex_backgrounds", "tmdb_backgrounds"]

# Iterate over each directory and each file in the directory
for wallpapers_dir in wallpapers_dirs:
    if os.path.exists(wallpapers_dir):
        for filename in os.listdir(wallpapers_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(wallpapers_dir, filename)
                print(f"Uploading {filename} to subreddit...")

                # Submit the image to the subreddit
                try:
                    subreddit.submit_image(title=f"Wallpaper: {filename}", image_path=file_path)
                    print(f"Successfully uploaded {filename}.")
                except Exception as e:
                    print(f"Failed to upload {filename}: {e}")
