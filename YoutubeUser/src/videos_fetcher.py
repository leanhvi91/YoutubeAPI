import requests
import json
import time
from multiprocessing import Process


data_home = "/home/vila/Project/YoutubeUser/data"

url = "https://www.googleapis.com/youtube/v3/search"

querystring = {
    "channelId":"UCsooa4yRKGN_zEE8iknghZA",
    "part":"snippet",
    "key":"AIzaSyCVB2uxo0LC52PuOdb_yPKH_bMz1d3mPJU",
    "pageToken":"CAoQAA"
}

headers = {
    'cache-control': "no-cache",
    'postman-token': "a7befa87-43cd-82f5-4ad2-ddab7f986f16"
    }

# response = requests.request("GET", url, headers=headers, params=querystring)
#
# text = response.text
#
# print(response.json())



def get_channel_videos(items, querystring):
    """
    Get list of video info object of a channel
    :param channelId: Youtube Channel Id
    :param key: API key
    :param part: id/snippet
    :param maxResults: unsigned int: 0 - 50
    :return: List of all videos info of the input channel
    """
    url = "https://www.googleapis.com/youtube/v3/search"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "a7befa87-43cd-82f5-4ad2-ddab7f986f16"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if not response.ok:
        return items
    responseObject = response.json()
    totalItems = responseObject["pageInfo"]["totalResults"]
    fetchedItems = responseObject["items"]
    itemsCount = len(fetchedItems)
    items += fetchedItems
    print("SUCCESS\t%s/%s"%(itemsCount, totalItems))

    while "nextPageToken" in responseObject:
        querystring["nextPageToken"] = responseObject["nextPageToken"]
        response = requests.request("GET", url, headers=headers, params=querystring)
        if not response.ok:
            return items
        responseObject = response.json()
        fetchedItems = responseObject["items"]
        itemsCount += len(fetchedItems)
        items += fetchedItems
        print("SUCCESS\t%s/%s" % (itemsCount, totalItems))


def save_to_json_lines(items, filePath, nTrials = 10):
    count = 0
    with open(filePath, "w") as f:
        while True and count < nTrials:
            if items:
                item = items.pop()
                count = 0
            else:
                time.sleep(1)
                count += 1
                continue
            line = json.dumps(item)
            line = line.replace("\n", " ") + "\n"
            f.write(line)

if __name__=="__main__":

    items = []

    channelId = "UCsooa4yRKGN_zEE8iknghZA"
    key = "AIzaSyCVB2uxo0LC52PuOdb_yPKH_bMz1d3mPJU",
    querystring = {
        "channelId": channelId,
        "part": "snippet",
        "key": key,
        "type": "video",
        "maxResults": 50
    }



    pFetcher = Process(target=get_channel_videos, args=(items, querystring))
    pFetcher.start()

    filePath = ("%s/%s/videos.txt" % (data_home, channelId))
    pStorer = Process(target=save_to_json_lines, args=(items, filePath))
    pStorer.start()