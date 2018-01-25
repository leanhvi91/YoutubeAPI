import requests
import json

data_home = "/home/levi/projects/YoutubeAPI/YoutubeUser/data"

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



def get_channel_videos(querystring, filePath):
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
        return
    responseObject = response.json()
    totalItems = responseObject["pageInfo"]["totalResults"]
    items = responseObject["items"]
    itemsCount = len(items)
    save_to_json_lines(items, filePath)
    print("SUCCESS\t%s/%s"%(itemsCount, totalItems))

    while "nextPageToken" in responseObject:
        querystring["pageToken"] = responseObject["nextPageToken"]
        response = requests.request("GET", url, headers=headers, params=querystring)
        if not response.ok:
            return
        responseObject = response.json()
        items = responseObject["items"]
        itemsCount += len(items)
        save_to_json_lines(items, filePath)
        print("SUCCESS\t%s/%s" % (itemsCount, totalItems))


def save_to_json_lines(items, filePath):
    with open(filePath, "a") as f:
        for item in items:
            line = json.dumps(item)
            line = line.replace("\n", " ") + "\n"
            f.write(line)


def get_channel_info(ids=[]):
    """

    :return:
    """
    if not ids:
        return {}
    _ids = ",".join(ids)
    url = "https://www.googleapis.com/youtube/v3/channels"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "a7befa87-43cd-82f5-4ad2-ddab7f986f16"
    }

    querystring = {
        "id": _ids,
        "part": "snippet",
        "key": "AIzaSyCVB2uxo0LC52PuOdb_yPKH_bMz1d3mPJU"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if not response.ok:
        return
    responseObject = response.json()
    totalItems = responseObject["pageInfo"]["totalResults"]
    items = responseObject["items"]
    return items


def get_video_info(ids=[]):
    """

    :param ids:
    :return:
    """
    if not ids:
        return {}
    _ids = ",".join(ids)
    url = "https://www.googleapis.com/youtube/v3/videos"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "a7befa87-43cd-82f5-4ad2-ddab7f986f16"
    }

    querystring = {
        "id": _ids,
        "part": "snippet",
        "key": "AIzaSyCVB2uxo0LC52PuOdb_yPKH_bMz1d3mPJU"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if not response.ok:
        return
    responseObject = response.json()
    totalItems = responseObject["pageInfo"]["totalResults"]
    items = responseObject["items"]
    return items

if __name__=="__main__":

    # items = []
    #
    # channelId = "UCzR-rom72PHN9Zg7RML9EbA"
    #
    # key = "AIzaSyCVB2uxo0LC52PuOdb_yPKH_bMz1d3mPJU"
    #
    # querystring = {
    #     "channelId": channelId,
    #     "part": "snippet",
    #     "key": key,
    #     "type": "video",
    #     "maxResults": 50
    # }
    #
    # filePath = ("%s/%s/videos.txt" % (data_home, channelId))
    #
    # get_channel_videos(querystring, filePath)

    ids = ["UC6E2mP01ZLH_kbAyeazCNdg", "UC08wrceRCWhajGG4udhETww", "UCd_vju15XYyTXgL-S3_2HtA",
           "UCd_vju15XYyTXgL-S3_2HtA", "UCJsSEDFFnMFvW9JWU6XUn0Q", "UCkEBDbzLyH-LbB2FgMoSMaQ",
           "UCvJiYiBUbw4tmpRSZT2r1Hw", "UCwmZiChSryoWQCZMIQezgTg", "UCzR-rom72PHN9Zg7RML9EbA",
           "UCzWQYUVCpZqtN93H8RR44Qw"]

    items = get_channel_info(ids=ids)
    filePath = "/home/vila/projects/YoutubeAPI/YoutubeUser/data/channels.txt"
    save_to_json_lines(items=items, filePath=filePath)

    print(items)