class Helper:
    """
    A collection of helper methods used across the application.
    """
    @staticmethod
    def parse_video_information(video):
        """
        Parses information from a video dictionary.
        
        Args:
            video (dict): The video dictionary to parse.
            
        Returns:
            dict: A dictionary containing parsed video information.
        """
        view_count = Helper.get_value(video, "viewCount")
        text = Helper.get_value(view_count, "text")
        image_link = Helper.get_value(video, "thumbnails")
        link = Helper.get_value(video, "link")
        published_time = Helper.get_value(video, "publishedTime")
        duration = Helper.get_value(video, "duration")
        
        return {
            "title": video["title"],
            "viewCount": text,
            "imageLink": image_link[-1]["url"] if image_link else None,
            "link": link,
            "publishedTime": published_time, 
            "duration": duration
        }
        
    @staticmethod
    def parse_channel_information(channel):
        """
        Parses information from a channel dictionary.
        
        Args:
            channel (dict): The channel dictionary to parse.
            
        Returns:
            dict: A dictionary containing parsed channel information.
        """
        item = channel["items"][0] if channel.get("items") else {}
        
        snippet = item.get("snippet", {})
        title = Helper.get_value(snippet, "title")
        description = Helper.get_value(snippet, "description")
        country = Helper.get_value(snippet, "country")
        
        statistics = item.get("statistics", {})
        view_count = Helper.get_value(statistics, "viewCount")
        subscriber_count = Helper.get_value(statistics, "subscriberCount")
        video_count = Helper.get_value(statistics, "videoCount")
        
        return {
            "title": title,
            "description": description,
            "country": country,
            "viewCount": view_count,
            "subscriberCount": subscriber_count,
            "videoCount": video_count
        }

    @staticmethod
    def is_video_filtered(received_video):
        """
        Checks if a video should be filtered out based on certain criteria.
        
        Args:
            received_video (dict): The video dictionary to check.
            
        Returns:
            bool: True if the video should be filtered out, False otherwise.
        """
        channel_name = received_video.get("channel", {}).get("name", "").lower()
        title = received_video.get("title", "").lower()
        
        if "123 go" in channel_name or "t-series" in channel_name: 
            return True
        elif "nursery rhymes" in title or "kids" in title:
            return True
        else:
            return False
        
    @staticmethod
    def get_value(dictionary, key):
        """
        Safely gets a value from a dictionary.
        
        Args:
            dictionary (dict): The dictionary to get the value from.
            key (str): The key of the value to get.
            
        Returns:
            The value associated with the key, or None if the key is not in the dictionary.
        """
        return dictionary.get(key)
