import requests
import xml.etree.ElementTree as ET
import html
from multiprocessing import Process
from queue import Queue
import time
import json

data_home = "/home/vila/Project/YoutubeAPI/YoutubeUser/data"

url = "https://www.youtube.com/api/timedtext"

querystring = {"v":"AQvTu1BKfxQ","lang":"en"}

def load_subtitle(videoId, lang):
    """

    :param videoId:
    :param lang:
    :return:
    """
    querystring = {
        "v": videoId,
        "lang": lang
    }
    headers = {
        'cache-control': "no-cache",
        'postman-token': "43b73caf-e525-0535-56cc-4490c4a7ac1c"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if not response.ok:
        print("%s\tSUBTITLE NOT FOUND" % videoId)
        return []
    if not response.text.strip():
        querystring["lang"] = "en"
        querystring["tlang"] = lang
        response = requests.request("GET", url, headers=headers, params=querystring)
    if not response.ok or not response.text.strip():
        print("%s\tSUBTITLE NOT FOUND" % videoId)
        return []
    lines = []
    root = ET.fromstring(response.text)
    for child in root:
        time = child.attrib
        text = child.text
        line = {}
        if "start" in time and "dur" in time:
            line["start"] = time["start"]
            line["dur"] = time["dur"]
            line["text"] = html.unescape(text)
            lines.append(line)
    print("%s\tSUCCESS DOWNLOAD" % videoId)
    return lines

def save_to_file(filePath, content):
    """

    :param filePath:
    :param content:
    :return:
    """
    with open(filePath, "w") as f:
        f.write(content)

def get_videos_id(channelId):
    """

    :param channelId:
    :return:
    """
    videos_file = ("%s/%s/videos.txt" % (data_home, channelId))
    ids = []
    with open(videos_file, "r") as f:
        for line in f:
            item = json.loads(line)
            if "id" in item:
                ids.append(item["id"]["videoId"])
    return ids


def multi_download_subtitles(channelId):
    """

    :param channelId:
    :return:
    """




if __name__=="__main__":

    channelId = "UCsZXuHKonP9utl5q2hFCkgA"
    ids = get_videos_id(channelId)

    print(ids)
    print(len(ids))