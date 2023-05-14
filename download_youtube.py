import os
import re
import argparse
from pytube import YouTube, Playlist

def sanitize_filename(filename):
    pattern = r'[\\/:\*\?"<>|]'
    sanitized_filename = re.sub(pattern, '-', filename)
    return sanitized_filename

def on_progress(chunk, file_handler, bytes_remaining, video, video_counter, total_videos):
    total_bytes = video.streams.get_highest_resolution().filesize
    bytes_downloaded = total_bytes - bytes_remaining
    percentage = (bytes_downloaded / total_bytes) * 100
    progress = f"Downloading: [{video_counter}/{total_videos}] {video.title[:70]}... ({percentage:.2f}%)"
    print(progress.ljust(100), end='\r')

def display_overall_progress(video_counter, total_videos):
    remaining_videos = total_videos - video_counter
    overall_percentage = (video_counter / total_videos) * 100
    overall_progress = f"Overall Progress: ({overall_percentage:.2f}%) {video_counter} of {total_videos} videos completed - {remaining_videos} Remaining"
    print(overall_progress)

def download_video(video_url, output_path):
    yt = YouTube(video_url)
    title = yt.title
    filename = f"{sanitize_filename(title)}.mp4"
    output_file = os.path.join(output_path, filename)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path=output_path, filename=filename)
    print("Download complete!")

def download_playlist(playlist_url, output_path):
    playlist = Playlist(playlist_url)
    playlist_name = playlist.title
    playlist_dir = os.path.join(output_path, playlist_name)
    os.makedirs(playlist_dir, exist_ok=True)
    video_counter = 1
    total_videos = len(playlist.videos)
    for video in playlist.videos:
        filename = f"{video_counter:03} - {video.title}.mp4"
        filename = sanitize_filename(filename)
        video_output_path = os.path.join(playlist_dir, filename)
        video.register_on_progress_callback(lambda chunk, file_handler, bytes_remaining: on_progress(chunk, file_handler, bytes_remaining, video, video_counter, total_videos))
        video.streams.get_highest_resolution().download(output_path=playlist_dir, filename=filename)
        video_counter += 1
        display_overall_progress(video_counter, total_videos)
    print("Download complete!")

def main():
    parser = argparse.ArgumentParser(description='Download YouTube videos or playlists.')
    parser.add_argument('link', nargs='?', help='YouTube video or playlist link')
    parser.add_argument('-d', '--directory', help='Output directory')
    parser.add_argument('-l', '--list', action='store_true', help='Flag to indicate a list of links')
    parser.add_argument('--csv', action='store_true', help='Flag to use comma-separated list')
    args = parser.parse_args()

    if not args.link:
        link = input("Enter YouTube link: ")
        if args.directory:
            download_video(link, args.directory)
        else:
            download_video(link, os.getcwd())
    elif args.list:
        links = args.link.split(',') if args.csv else args.link.splitlines()
        total_links = len(links)
        for index, link in enumerate(links, start=1):
            if args.directory:
                download_playlist(link, args.directory)
            else:
                download_playlist(link, os.getcwd())
            display_overall_progress(index, total_links)
    else:
        if args.directory:
            download_video(args.link, args.directory)
        else:
            download_video(args.link, os.getcwd())

if __name__ == '__main__':
    main()
