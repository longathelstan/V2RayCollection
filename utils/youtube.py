import requests
import os

class Youtube:
    def get_vids_in_channel(id_channel: str):
        API_KEY = os.getenv("GOOGLE_API_KEY")
        r = requests.get(f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={id_channel}&part=snippet,id&order=date&maxResults=20")
        return r.json()["items"]
    
    def get_first_comment(id_video: str):
        API_KEY = os.getenv("GOOGLE_API_KEY")
        r = requests.get(f"https://www.googleapis.com/youtube/v3/commentThreads?key={API_KEY}&textFormat=plainText&part=snippet&videoId={id_video}&maxResults=50")
        return r.json()["items"][0]["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
    
    def get_comments(id_video: str):
        API_KEY = os.getenv("GOOGLE_API_KEY")
        r = requests.get(f"https://www.googleapis.com/youtube/v3/commentThreads?key={API_KEY}&textFormat=plainText&part=snippet&videoId={id_video}&maxResults=50")
        return r.json()["items"]