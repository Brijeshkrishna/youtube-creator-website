from flask import Flask, render_template
import numpy as np
from pytube import Channel, YouTube
import os
import requests
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# # local
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__, template_folder="./src/template", static_folder="./src/static")

global VIDEO_LIST
global VIDEOCOUNT
global CHANNEL_URL
global SOCIAL

VIDEO_LIST = np.array([], dtype=dict)
VIDEOCOUNT = int(os.environ["VIDEOCOUNT"])
CHANNEL_URL = os.environ["CHANNEL_URL"]
FAVICON_URL = os.environ["FAVICON_URL"]
BANNER_VIDEO_URL = os.environ["BANNER_VIDEO_URL"]
BANNER_VIDEO_LENGTH = int(os.environ["BANNER_VIDEO_LENGTH"])


def setVidFav(video_url, fav_url, video_len=10, res="360"):
    print("Downloading video")
    video_path = os.path.abspath("src/static/video/temp.mp4")
    with open(video_path, "wb") as f:
        if "https://www.youtube.com" in video_url:
            r = YouTube(video_url).streams.get_by_resolution(res + "p").url
        else:
            r = video_url
            print("Video url:" + r)
        f.write(requests.get(r).content)

    print("Loading video")
    ffmpeg_extract_subclip(
        video_path,
        0,
        video_len,
        targetname="src/static/video/intro.mp4",
    )
    if not fav_url is None:
        with open("./src/static/img/favicon.ico", "wb") as f:
            f.write(requests.get(fav_url).content)


setVidFav(BANNER_VIDEO_URL, FAVICON_URL, BANNER_VIDEO_LENGTH)

SOCIAL = {
    "CHANNEL_NAME": os.environ["CHANNEL_NAME"],
    "CHANNEL_URL": CHANNEL_URL,
}
try:
    SOCIAL["INSTAGRAM_URL"] = os.environ["INSTAGRAM_URL"]
except:
    SOCIAL["INSTAGRAM_URL"] = "https://www.instagram.com/"
try:
    SOCIAL["TWITTER_URL"] = os.environ["TWITTER_URL"]
except:
    SOCIAL["TWITTER_URL"] = "https://twitter.com/"

channel_root = Channel(CHANNEL_URL)
j = 0
for i in channel_root.video_urls:
    VIDEO_LIST = np.append(
        VIDEO_LIST, {"videoId": i.split("=")[1], "title": YouTube(i).title}
    )
    j += 1
    if j == VIDEOCOUNT:
        break

print("Server started..")
@app.route("/")
def response():
    global VIDEO_LIST
    global VIDEOCOUNT
    global CHANNEL_URL
    global SOCIAL

    channel_root = Channel(CHANNEL_URL)
    subcriber = channel_root.about_html.split("subscribers")[1][18:]

    for i in range(0, VIDEOCOUNT):
        if i < VIDEO_LIST.__len__():
            if channel_root.video_urls[i].split("=")[1] == VIDEO_LIST[i]["videoId"]:
                break
        VIDEO_LIST = np.insert(
            VIDEO_LIST,
            0,
            {
                "videoUrl": channel_root.video_urls[i],
                "videoId": channel_root.video_urls[i].split("=")[1],
                "title": YouTube(i).title,
            },
        )

    return render_template(
        "index.html", html_data=list(VIDEO_LIST), subcriber=subcriber, social=SOCIAL
    )