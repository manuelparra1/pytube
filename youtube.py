#!/usr/bin/env python
# coding: utf-8

# In[4]:


from pytube import YouTube


# ### Create `pytube` `YouTube` object

# In[5]:


# Create YouTube object with video_url variable
video_url = "https://youtu.be/TK2l-Dv4M2M"
yt = YouTube(video_url)


# In[ ]:


#yt = YouTube(
#        'http://youtube.com/watch?v=2lAe1cqCOXo',
#        on_progress_callback=progress_func,
#        on_complete_callback=complete_func,
#        proxies=my_proxies,
#        use_oauth=False,
#        allow_oauth_cache=True
#    )


# ### Streams

# In[6]:


# Retrieve all available streams
for stream in yt.streams:
    # Print the available quality choices
    print(f"Resolution: {stream.resolution}, Format: {stream.mime_type}")


# ### 1080p MP4

# In[7]:


for i in yt.streams:
    print(i)


# In[8]:


mp4_1080p = yt.streams.get_highest_resolution()


# In[ ]:


#print(mp4_1080p)


# In[9]:


mp4_1080p.download(output_path = "pytube/YouTube-Videos/")


# In[ ]:


# Filter and select 1080p resolution stream with mp4 file type
#mp4_1080p = yt.streams.filter(file_extension='mp4', resolution='1080p').first()

# Download Selected Quality to Directory
#mp4_1080p.download(output_path = "pytube/YouTube-Videos/")


# ### 1080p WEBM

# In[ ]:





# In[ ]:





# In[ ]:


# Filter and select 1080p resolution stream with webm file type
#best_webm = yt.streams.filter(file_extension='webm', resolution='1080p').first()

# Download Selected Quality to Directory
#best_webm.download(output_path = "pytube/YouTube-Videos/")


# # Playlists

# In[3]:


from pytube import Playlist

def on_progress(stream, chunk, bytes_remaining):
    total_bytes = stream.filesize
    bytes_downloaded = total_bytes - bytes_remaining
    percentage = (bytes_downloaded / total_bytes) * 100
    print(f"Downloaded: {percentage:.2f}%")

playlist_url = "https://youtube.com/playlist?list=PLhoH5vyxr6Qq41NFL4GvhFp-WLd5xzIzZ"
playlist = Playlist(playlist_url)

output_path = "pytube/YouTube-Videos/"

for video in playlist.videos:
    video.register_on_progress_callback(on_progress)
    video.streams.get_highest_resolution().download(output_path=output_path)


# In[ ]:


from pytube import Playlist

def on_progress(stream, chunk, bytes_remaining):
    total_bytes = stream.filesize
    bytes_downloaded = total_bytes - bytes_remaining
    percentage = (bytes_downloaded / total_bytes) * 100
    print(f"Downloading: [{video_counter}/{total_videos}] {stream.default_filename} ({percentage:.2f}%)")

playlist_url = "https://www.youtube.com/playlist?list=PLAYLIST_ID"
playlist = Playlist(playlist_url)

output_path = "pytube/YouTube-Videos/"

video_counter = 1  # Initialize the counter
total_videos = len(playlist.videos)  # Get the total number of videos in the playlist

for video in playlist.videos:
    video.register_on_progress_callback(on_progress)

    # Assign the formatted counter value to the file name
    filename = f"{video_counter:03} - {video.title}.mp4"

    video.streams.get_highest_resolution().download(output_path=output_path, filename=filename)

    video_counter += 1  # Increment the counter for the next video

    remaining_videos = total_videos - video_counter + 1
    overall_percentage = (remaining_videos / total_videos) * 100
    print(f"Overall Progress: {remaining_videos}/{total_videos} videos remaining ({overall_percentage:.2f}%)\n")

