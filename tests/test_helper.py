import pytest
from helper.py import Helper

def test_parse_video_information():
    video = {
        "title": "Test Video",
        "viewCount": {"text": "1,234"},
        "thumbnails": [{"url": "http://example.com/image.jpg"}],
        "link": "http://example.com/video",
        "publishedTime": "1 day ago",
        "duration": "10:00"
    }
    result = Helper.parse_video_information(video)
    assert result["title"] == "Test Video"
    assert result["viewCount"] == "1,234"
    assert result["imageLink"] == "http://example.com/image.jpg"
    assert result["link"] == "http://example.com/video"
    assert result["publishedTime"] == "1 day ago"
    assert result["duration"] == "10:00"

def test_parse_channel_information():
    channel = {
        "items": [
            {
                "snippet": {
                    "title": "Test Channel",
                    "description": "This is a test channel.",
                    "country": "US"
                },
                "statistics": {
                    "viewCount": "12345",
                    "subscriberCount": "6789",
                    "videoCount": "101"
                }
            }
        ]
    }
    result = Helper.parse_channel_information(channel)
    assert result["title"] == "Test Channel"
    assert result["description"] == "This is a test channel."
    assert result["country"] == "US"
    assert result["viewCount"] == "12345"
    assert result["subscriberCount"] == "6789"
    assert result["videoCount"] == "101"

def test_is_video_filtered():
    video = {"channel": {"name": "123 GO"}, "title": "Test Video"}
    assert Helper.is_video_filtered(video) == True

    video = {"channel": {"name": "T-Series"}, "title": "Test Video"}
    assert Helper.is_video_filtered(video) == True

    video = {"channel": {"name": "Test Channel"}, "title": "Nursery Rhymes"}
    assert Helper.is_video_filtered(video) == True
