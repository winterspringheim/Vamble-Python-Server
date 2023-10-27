import pytest
from youtubesearchpython.__future__ import VideosSearch
from services.youservice import YouService

@pytest.mark.asyncio
async def test_channel_list_lite_service():
    videos_search = VideosSearch('Test Query', limit=20)
    result = await YouService.channel_list_lite_service(videos_search)
    assert isinstance(result, dict)
    # Add more specific assertions based on your application's behavior

@pytest.mark.asyncio
async def test_channel_list_service():
    result = await YouService.channel_list_service('Test Query')
    assert isinstance(result, dict)
    # Add more specific assertions based on your application's behavior
