# Spotify_Playlist_Exporter
A Python CLI tool to grab the songs of a Spotify playlist, then export them into a text file, or in my case, to YouTube.

# Requirements
Python 3.6 or above
Then 
pip install -r requirements.txt
## For exporting to YouTube
You must set up a google developer account with access to the YouTube v3 API. Then create a set of OAUTH2 and API access keys. 
Create a .env file, and put the following code in the file
~~```
YOUTUBE_API_KEY={YOUR_YOUTUBE_API_KEY_HERE}
```
Replace {YOUR_YOUTUBE_API_KEY_HERE} with your youtube api key
Then download the client_secret.apps.googleusercontent.com.json file from google and put it into the same dir as main.py


