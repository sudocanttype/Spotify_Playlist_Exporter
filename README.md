# Spotify_Playlist_Exporter
A Python CLI tool to scrape the songs of a Spotify playlist, then export them into a text file, or to YouTube. 

## Requirements
- Linux
- Python 3.6 or above
- PIP3
- git

## Installation and Prerequisites
*THIS GUIDE ONLY APPLIES TO LINUX/GNU OPERATING SYSTEMS*
<br>
To download, run `git clone https://github.com/sudocanttype/Spotify_Playlist_Exporter.git && cd Spotify_Playlist_Exporter`
<br>
Then, install the necessary libraries by running `pip3 install -r requirements.txt`.
### YouTube Compatibility
In order to be able to export playlists to YouTube, you must set up a google developer account with access to the YouTube v3 API. Instructions on how can be found [here](https://developers.google.com/youtube/v3/getting-started#before-you-start). Then, follow the instructions to set up OAUTH2, and generate an API key in the Google Developers Console. 
<br>
In the Spotify_Playlist_Exporter folder, run `touch .env` to create a .env file, and put the following code in the file
```
YOUTUBE_API_KEY={YOUR_YOUTUBE_API_KEY_HERE}
```
Replace {YOUR_YOUTUBE_API_KEY_HERE} with your YouTube API Key.
<br>
Finally, go the the Credentials page from the Google Developers Console, and click on the name of your newly created OAUTH2 Client ID. Download the JSON file with the button labelled "DOWNLOAD JSON", and rename it to `client_secret.apps.googleusercontent.com.json`. Move this JSON file into the Spotify_Playlist_Exporter folder, and finally, Spotify_Playlist_Exporter is ready to run. 

## Running
While in the folder Spotify_Playlist_Exporter, simply run `python3 main.py`.


