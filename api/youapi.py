import asyncio
from youtubesearchpython.__future__ import VideosSearch, Video, Playlist, playlist_from_channel_id
import googleapiclient.discovery

from helpers.decorators import async_error_handler
from helpers.helper import Helper
import helpers.constants as constants

class YouApi:
    """
    This class interacts with YouTube Data API and youtubesearchpython library
    to fetch YouTube channel and video information.
    """
    def __init__(self):
        """
        Initializes the Google API client and sets up the YouTube Data API.
        """
        self.youtube = googleapiclient.discovery.build(
            constants.API_SERVICE_NAME, constants.API_VERSION, developerKey=constants.DEVELOPER_KEY)
    
    @async_error_handler
    async def add_channel_information(self, channel, channel_id, channels_db):
        """
        Adds additional channel information to the provided channel dictionary.
        
        Args:
            channel (dict): The channel dictionary to add information to.
            channel_id (str): The YouTube channel ID.
            channels_db (Cursor): MongoDB cursor to fetch channel information from the database.
        """
        for x in channels_db:
            if x["channelId"] == channel_id:
                del x["_id"]
                channel["information"] = x
                return
        
        request = self.youtube.channels().list(
            id=channel_id,
            part="snippet,statistics,contentDetails"
        )
        
        channel["information"] = Helper.parse_channel_information(request.execute())
        return
    
    @async_error_handler
    async def add_video_information(self, channel, video_id):
        """
        Adds additional video information to the provided channel dictionary.
        
        Args:
            channel (dict): The channel dictionary to add information to.
            video_id (str): The YouTube video ID.
        """
        response = await Video.getInfo(video_id)
        
        if Helper.is_video_filtered(response):
            return
        
        channel["videos"] = Helper.parse_video_information(response)
        return
    
    @async_error_handler
    async def video_search(self, videos_search):
        """
        Searches for videos on YouTube.
        
        Args:
            videos_search (VideosSearch): The VideosSearch instance to use for searching.
            
        Returns:
            list: A list of search results.
        """
        response = await videos_search.next()
        return response["result"]

    async def playlist_information(self, channel_id):
        """
        Fetches information about a YouTube playlist.
        
        Args:
            channel_id (str): The YouTube channel ID.
            
        Returns:
            list: A list of video information from the playlist.
        """
        tasks = []
        playlist = Playlist(playlist_from_channel_id(channel_id))
        
        await playlist.getNextVideos()
        videos = playlist.videos

        for video in videos:
            tasks.append(self.add_video_information({}, video["id"]))
        
        response = await asyncio.gather(*tasks)
        
        return response
