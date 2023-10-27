import time
import asyncio
from youtubesearchpython.__future__ import VideosSearch
import pymongo

from api.youapi import YouApi
from helpers.helper import Helper
import helpers.constants as constants

class YouService:
    """
    A service class that handles the business logic for fetching and processing YouTube channel and video data.
    """
    @staticmethod
    async def channel_list_lite_service(videos_search):
        """
        Provides a lightweight list of YouTube channels based on a search query.
        
        Args:
            videos_search (VideosSearch): Instance of VideosSearch to use for searching videos.
            
        Returns:
            dict: A dictionary containing the list of channels.
        """
        you_api = YouApi()
        videos = await you_api.video_search(videos_search)
        channel_list = {}
        for video in videos:
            channel_id = video['channel']["id"]
            if channel_id not in channel_list:
                channel_list[channel_id] = {"information": {}, "videos": []}
            channel_list[channel_id]["videos"].append(Helper.parse_video_information(video))
        return channel_list
    
    @staticmethod
    async def channel_list_service(query):
        """
        Provides a detailed list of YouTube channels based on a search query.
        
        Args:
            query (str): The search query.
            
        Returns:
            dict: A dictionary containing the list of channels.
        """
        search_counter = 0
        videos_search = VideosSearch(query, limit=20)
        channel_list = {}
        you_api = YouApi()
        tasks = []        
        video_search_time = 0
        
        mongo_cluster = pymongo.MongoClient()   # Insert the client url inside MongoClient()
        db = mongo_cluster["myFirstDatabase"]
        channels_db = db["channels"].find()   
        
        while search_counter != constants.SEARCH_LIMIT:
            start_time = time.time()
            videos = await you_api.video_search(videos_search)
            video_search_time += time.time() - start_time

            for video in videos:
                channel_id = video['channel']["id"]
                if channel_id not in channel_list:
                    channel_list[channel_id] = {"information": {}, "videos": []}
                    task = asyncio.create_task(you_api.add_channel_information(channel_list[channel_id], channel_id, channels_db))
                    tasks.append(task)                   
                channel_list[channel_id]["videos"].append(Helper.parse_video_information(video))
            search_counter += 1
        
        await asyncio.gather(*tasks)
        channel_list["videoSearchTime"] = video_search_time
                
        return channel_list
    
    @staticmethod
    async def channel_details_service(channel_id, query):
        """
        Fetches detailed information about a specific YouTube channel.
        
        Args:
            channel_id (str): The YouTube channel ID.
            query (str): The search query (currently not used, can be removed or repurposed).
            
        Returns:
            dict: A dictionary containing detailed channel information.
        """
        # Implementation for fetching and returning channel details
        # This would likely involve making API calls and/or database queries
        pass
