import threading
import time
from tkinter import *
import sys, subprocess, os
import urllib.parse
import json
try:
    import vlc
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'python-vlc'])
    import vlc

try:
    import pafy
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pafy'])
    import pafy

try:
    import requests
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])
    import requests

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

class YoutubeSearch:
    def __init__(self, search_terms: str, max_results=None):
        self.search_terms = search_terms
        self.max_results = max_results
        self.videos = self._search()

    def _search(self):
        encoded_search = urllib.parse.quote_plus(self.search_terms)
        BASE_URL = "https://youtube.com"
        url = f"{BASE_URL}/search?q={encoded_search}"
        response = requests.get(url).text
        while "ytInitialData" not in response:
            response = requests.get(url).text
        results = self._parse_html(response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[: self.max_results]
        return results

    def _parse_html(self, response):
        results = []
        start = (
            response.index("ytInitialData")
            + len("ytInitialData")
            + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"]

        for video in videos:
            res = {}
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})
                res["id"] = video_data.get("videoId", None)
                res["thumbnails"] = [thumb.get("url", None) for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}]) ]
                res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                res["long_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", None)
                res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0)
                res["publish_time"] = video_data.get("publishedTimeText", {}).get("simpleText", 0)
                res["url_suffix"] = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
                results.append(res)
        return results

    def to_dict(self, clear_cache=True):
        result = self.videos
        if clear_cache:
            self.videos = ""
        return result

    def to_json(self, clear_cache=True):
        result = json.dumps({"videos": self.videos})
        if clear_cache:
            self.videos = ""
        return result

def readpl(plname):
    playlistfile = open(plname)
    playlist = json.load(playlistfile)
    playlistfile.close()

    return playlist

def addtopl(playlist, plname):
    search = input("Search MultiFind: ")

    results = YoutubeSearch(search, max_results=10).to_dict()

    for i in range(len(results)):
        print(str(i) + " - " + results[i]["channel"] + ": " + results[i]["title"])

    whichres = int(input("Type here: "))

    url = "https://www.youtube.com" + results[whichres]["url_suffix"]

    print(str(len(list(playlist))))
    willbesong = {}
    willbesong['name'] = results[whichres]["title"]
    willbesong['author'] = results[whichres]["channel"]
    willbesong['url'] = url
    playlist[str(len(list(playlist)))] = willbesong

    print(playlist)

    playlistfile = open(plname, 'w+')
    json.dump(playlist, playlistfile, indent=3, ensure_ascii=False)
    playlistfile.close()


def playmusic(url, name, author):
    video = pafy.new(url)
    best = video.getbestaudio()
    playurl = best.url
    # playurl = url

    mediatoplay = vlc.MediaPlayer(playurl)
    mediatoplay.audio_set_volume(100)
    mediatoplay.play()
    time.sleep(0.5)
    length = mediatoplay.get_length() / 1000
    print(length)
    cls()
    print("Playing " + author + " - " + name)
    time.sleep(length)
    mediatoplay.stop()

playlist = readpl('play.list')
# addtopl(playlist, 'play.list')

for item in list(playlist):
    playmusic(playlist[item]['url'], playlist[item]['name'], playlist[item]['author'])

input()

