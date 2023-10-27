
# Vamble: YouTube Channel Explorer

## Overview

Vamble is an innovative application designed to offer users an immersive experience in exploring YouTube channels, providing extensive details, subscriber counts, video content, and user ratings on channels. This repository contains the Python backend server component of Vamble, responsible for interfacing with YouTube's data, performing web scraping, storing results in MongoDB, and serving processed data to the client application.

## Features

- **Channel Search**: Users can search for YouTube channels by entering text in the search bar.
- **Channel Details**: Retrieve detailed information about a YouTube channel, including subscriber count, description, and video content.
- **Channel Ratings**: Users can rate YouTube channels, and view the average ratings given by other users.
- **Performance Monitoring**: Performance of key endpoints is monitored and logged, ensuring efficient service delivery.
- **Error Handling**: Comprehensive error handling and retry mechanisms in place for robustness.

## Getting Started

### Prerequisites

- Python 3.6+
- Flask
- MongoDB
- Google Cloud Account (for deploying to Google Cloud Run)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/reigon/Vamble-Python.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Vamble-Python
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   - Copy the `.env.example` file to a new file named `.env`.
   - Fill in your MongoDB connection string, Google API key, and any other necessary configurations.

### Running Locally

1. Start the Flask application:
   ```bash
   python main.py
   ```

2. The server will start, and you can interact with it via `http://127.0.0.1:5000` or the configured port.

### Deploying to Google Cloud Run

1. Follow Google's official [Cloud Run Deployment Guide](https://cloud.google.com/run/docs/deploying) to deploy the application to Google Cloud Run.

## Usage

The server exposes several endpoints to interact with YouTube data:

- `GET /channel/list`: Search for YouTube channels.
- `GET /channel/list/lite`: Retrieve a lightweight list of YouTube channels.
- `GET /channel/details`: Get detailed information about a specific YouTube channel.

## Testing

The project includes a suite of tests to ensure functionality and reliability. To run the tests:

```bash
pytest tests/
```

## Acknowledgements

- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Flask](https://flask.palletsprojects.com/)
- [PyMongo](https://pymongo.readthedocs.io/)
- [Google Cloud Run](https://cloud.google.com/run)

