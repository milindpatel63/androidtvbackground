import os
import praw

# Metadata file to track uploaded images
metadata_file = "uploaded_wallpapers.txt"

# Load previously uploaded image filenames
if os.path.exists(metadata_file):
    with open(metadata_file, "r") as f:
        uploaded_images = set(f.read().splitlines())
else:
    uploaded_images = set()

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    refresh_token=os.getenv('REFRESH_TOKEN'),
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
                # Check if the image has already been uploaded
                if filename in uploaded_images:
                    print(f"Skipping {filename}, already uploaded.")
                    continue

                file_path = os.path.join(wallpapers_dir, filename)
                print(f"Uploading {filename} to subreddit...")

                # Submit the image to the subreddit
                try:
                    subreddit.submit_image(title=f"Wallpaper: {filename}", image_path=file_path)
                    print(f"Successfully uploaded {filename}.")
                    
                    # Add the image name to the metadata file
                    with open(metadata_file, "a") as f:
                        f.write(f"{filename}\n")

                    # Add to uploaded set to prevent processing during the current run
                    uploaded_images.add(filename)
                except Exception as e:
                    print(f"Failed to upload {filename}: {e}")