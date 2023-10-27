from youtubesearchpython.__future__ import VideosSearch
import os
import asyncio
from flask import Flask, jsonify, request

from helpers.decorators import performance_tester
from services.youservice import YouService

app = Flask(__name__)

# Global variable to store the current VideosSearch instance
videos_search_instance = None

@app.route("/channel/list", methods=['GET'])
@performance_tester
def channel_list():
    """
    Get a list of YouTube channels based on a search query.
    
    Returns:
        JSON response with a list of channels.
    """
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required."}), 400
    
    response = asyncio.run(YouService.channel_list_service(query=query))
    return jsonify(response), 200
    
@app.route("/channel/list/lite", methods=['GET'])
@performance_tester
def channel_list_lite():
    """
    Get a lightweight list of YouTube channels based on a search query.
    This endpoint is optimized for faster response times.
    
    Returns:
        JSON response with a list of channels.
    """
    global videos_search_instance
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required."}), 400
    
    new_search = request.args.get('new') == "1"
    if new_search or videos_search_instance is None:
        videos_search_instance = VideosSearch(query, limit=20)
        response = asyncio.run(YouService.channel_list_lite_service(videos_search_instance))
    else:
        response = asyncio.run(YouService.channel_list_lite_service(videos_search_instance))
    return jsonify(response), 200

@app.route("/channel/details", methods=['GET'])
def channel_details():
    """
    Get detailed information about a specific YouTube channel.
    
    Returns:
        JSON response with detailed channel information.
    """
    query = request.args.get('q')
    channel_id = request.args.get('id')
    if not channel_id:
        return jsonify({"error": "Query parameter 'id' is required."}), 400
    
    response = asyncio.run(YouService.channel_details_service(query=query, channel_id=channel_id))
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
