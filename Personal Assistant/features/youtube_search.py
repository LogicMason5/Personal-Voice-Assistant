import webbrowser
import urllib.parse
import urllib.request
import re

def play_youtube_song(song_name: str):
    # URL-encode the search query
    query_string = urllib.parse.urlencode({"search_query": song_name})
    url = "https://www.youtube.com/results?" + query_string

    # Fetch the search results page
    response = urllib.request.urlopen(url)
    html = response.read().decode()

    # Regex to extract video IDs (11 characters)
    video_ids = re.findall(r"watch\?v=(\S{11})", html)

    if not video_ids:
        print("No results found.")
        return

    # Use the first video
    video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
    print(f"Opening: {video_url}")

    # Open in browser
    webbrowser.open_new(video_url)


if __name__ == "__main__":
    song = input("Enter the song name: ")
    play_youtube_song(song)
