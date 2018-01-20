import json
import time, datetime
import dynamo_crud as dynamo


def get_time_stamp(timeLabel):
    """
    Convert time string into linux time stamp
    :param timeString: time label (string)
    :return: time stamp (integer)
    """
    if "000Z" in timeLabel:
        t = time.mktime(datetime.datetime.strptime(timeLabel, "%Y-%m-%dT%H:%M:%S.000Z").timetuple())
        return int(t)
    else:
        return 0


def load_video_list(filePath):
    """

    :param filePath: json lines file store video information
    :return: List of videos information
    """
    items = []
    with open(filePath) as fp:
        for line in fp:
            item = extract_item(line)
            if item:
                items.append(item)
    return items


def extract_item(line):
    """
    Extract item from a json line string
    :param line: json line
    :return: item object, empty object if extraction error
    """
    raw_item = json.loads(line)
    try:
        item = {}
        item["VideoId"] = raw_item["id"]["videoId"]
        item["ChannelId"] = raw_item["snippet"]["channelId"]
        time_label = raw_item["snippet"]["publishedAt"]
        item["PublishedAtLabel"] = time_label
        item["PublishedAt"] = get_time_stamp(time_label)
        item["Title"] = raw_item["snippet"]["title"]
        item["ChannelTitle"] = raw_item["snippet"]["channelTitle"]
        item["Status"] = 0
        return item
    except:
        return {}


if __name__ == "__main__":
    filePath = "/home/levi/projects/YoutubeAPI/YoutubeUser/data/UCzWQYUVCpZqtN93H8RR44Qw/videos.txt"
    items = load_video_list(filePath=filePath)

    _items = json.dumps(items, indent=2)
    #
    # dynamo.batch_put_items(items, "Videos")
    print(items)
    print(len(items))
