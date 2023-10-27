import pytest
from unittest.mock import AsyncMock, patch
from api.youapi import YouApi

@pytest.fixture
def mock_youtube_api():
    with patch('googleapiclient.discovery.build') as mock:
        yield mock

@pytest.mark.asyncio
async def test_add_channel_information(mock_youtube_api):
    you_api = YouApi()
    channel = {}
    channel_id = "test_channel_id"
    channels_db = [{"channelId": "test_channel_id", "some_data": "some_value"}]

    # Mock the YouTube API response
    mock_youtube_api.return_value.channels.return_value.list.return_value.execute.return_value = {
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
    
    await you_api.add_channel_information(channel, channel_id, channels_db)

    assert channel["information"]["title"] == "Test Channel"
    assert channel["information"]["viewCount"] == "12345"
    assert channel["information"]["country"] == "US"

@pytest.mark.asyncio
async def test_add_video_information(mock_youtube_api):
    you_api = YouApi()
    channel = {}
    video_id = "test_video_id"

    # Mock the Video.getInfo response
    with patch('youapi.Video.getInfo', new_callable=AsyncMock) as mock_get_info:
        mock_get_info.return_value = {
            "title": "Test Video",
            "viewCount": {"text": "1,234"},
            "thumbnails": [{"url": "http://example.com/image.jpg"}],
            "link": "http://example.com/video",
            "publishedTime": "1 day ago",
            "duration": "10:00",
            "channel": {"name": "Test Channel"}
        }
        
        await you_api.add_video_information(channel, video_id)

    assert channel["videos"]["title"] == "Test Video"
    assert channel["videos"]["viewCount"] == "1,234"
    assert channel["videos"]["imageLink"] == "http://example.com/image.jpg"
