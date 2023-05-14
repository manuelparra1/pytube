#!/usr/bin/env python
# coding: utf-8

# ## Libraries

# In[ ]:


import os
import re
from pytube import Playlist


# ## Functions

# In[ ]:


def sanitize_filename(filename):
    # Define the pattern for invalid characters
    pattern = r'[\\/:\*\?"<>|]'

    # Replace invalid characters with a hyphen
    sanitized_filename = re.sub(pattern, '-', filename)
    return sanitized_filename


# In[ ]:


def on_progress(chunk, file_handler, bytes_remaining, video, video_counter, total_videos):
    total_bytes = video.streams.get_highest_resolution().filesize
    bytes_downloaded = total_bytes - bytes_remaining
    percentage = (bytes_downloaded / total_bytes) * 100
    progress = f"Downloading: [{video_counter}/{total_videos}] {video.title[:70]}... ({percentage:.2f}%)"
    print(progress.ljust(100), end='\r')


# In[ ]:


def display_overall_progress(video_counter, total_videos):
    remaining_videos = total_videos - video_counter
    overall_percentage = (video_counter / total_videos) * 100
    overall_progress = f"Overall Progress: ({overall_percentage:.2f}%) {video_counter} of {total_videos} videos completed - {remaining_videos} Remaining"
    print(overall_progress)


# In[ ]:


def download_playlist(playlist_url, output_path):
    playlist = Playlist(playlist_url)

    # Create subdirectory using the playlist name
    playlist_name = playlist.title
    playlist_dir = os.path.join(output_path, playlist_name)
    os.makedirs(playlist_dir, exist_ok=True)

    video_counter = 1  # Initialize the counter
    total_videos = len(playlist.videos)  # Get the total number of videos in the playlist

    for video in playlist.videos:
        # Assign the formatted counter value to the file name
        filename = f"{video_counter:03} - {video.title}.mp4"

        # Sanitize the filename
        filename = sanitize_filename(filename)

        # Set the output path to the playlist subdirectory
        video_output_path = os.path.join(playlist_dir, filename)

        # Register the progress callback function with the video object and the counter
        video.register_on_progress_callback(lambda chunk, file_handler, bytes_remaining: on_progress(chunk, file_handler, bytes_remaining, video, video_counter, total_videos))

        # Download the highest resolution stream to the playlist directory
        video.streams.get_highest_resolution().download(output_path=playlist_dir, filename=filename)

        video_counter += 1  # Increment the counter for the next video

        display_overall_progress(video_counter, total_videos)

    print("Download complete!")


# ## Main

# In[2]:


playlist_url = "https://youtube.com/playlist?list=PLTR5ZfYubz5Up1SQiaJmB29kgRNNUsClM"
output_path = "Downloads/"
download_playlist(playlist_url, output_path)


# In[ ]:




