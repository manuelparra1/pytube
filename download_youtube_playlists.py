#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pytube import Playlist


# In[2]:


def on_progress(stream, chunk, bytes_remaining):
    total_bytes = stream.filesize
    bytes_downloaded = total_bytes - bytes_remaining
    percentage = (bytes_downloaded / total_bytes) * 100
    print(f"Downloading: [{video_counter}/{total_videos}] {stream.default_filename} ({percentage:.2f}%)")


# ## URL

# In[4]:


playlist_url = "https://youtube.com/playlist?list=PLTR5ZfYubz5Up1SQiaJmB29kgRNNUsClM"


# ## Variables

# In[5]:


# Setup Variables
# ---------------
playlist = Playlist(playlist_url)
output_path = "Downloads/"

# Create subdirectory using the playlist name
playlist_name = playlist.title
playlist_dir = os.path.join(output_path, playlist_name)
os.makedirs(playlist_dir, exist_ok=True)

video_counter = 1  # Initialize the counter
total_videos = len(playlist.videos)  # Get the total number of videos in the playlist


# ## Downloading

# In[ ]:


# Downloading
# -----------
for video in playlist.videos:
    video.register_on_progress_callback(on_progress)

    # Assign the formatted counter value to the file name
    filename = f"{video_counter:03} - {video.title}.mp4"

    # Set the output path to the playlist subdirectory
    video_output_path = os.path.join(playlist_dir, filename)

    video.streams.get_highest_resolution().download(output_path=video_output_path)

    video_counter += 1  # Increment the counter for the next video

    remaining_videos = total_videos - video_counter + 1
    overall_percentage = (video_counter / total_videos) * 100
    overall_progress = f"Overall Progress: ({overall_percentage:.2f}%) {video_counter} of {total_videos} videos completed - {remaining_videos} Remaining"
    print(overall_progress)

print("Download complete!")

