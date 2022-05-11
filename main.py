#!/usr/local/bin/python3
import os
import re
import time

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login_to_spotify(driver):

    driver.get("https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F")
    #this link ensures you end up on web client
    print("Please insert your credentials and login.")
    WebDriverWait(driver, 1000000).until(
        #await spotify homepage
        EC.url_matches("https://open.spotify.com/")
    )
    get_playlists_from_spotify(driver)

def get_playlists_from_spotify(driver):
    #assumes you are already logged in
    driver.get("https://open.spotify.com/collection/playlists")
    print("Select a playlist from the screen")
    WebDriverWait(driver, 1000000).until(
        EC.url_contains("https://open.spotify.com/playlist/")
    )
    #and now you're on the playlist page
    time.sleep(1)

def parse_songs_from_spotify(driver):
    #parse the html from selenium html, returns a list of all the songs
    time.sleep(1)
    #sleep for a sec so that the page has time to load
    songs = []

    element = driver.find_element_by_xpath("//div[@data-testid='playlist-tracklist']")
    soup = bs(element.get_attribute('innerHTML'),'html.parser')
    #get the container holding all the songs
    container = soup.contents[1].contents[1]
    #the container holding all the songs is the 2nd child of the 2nd child of playlist tracklist

    #loading percentage
    p = 0
    deltap = int(100/len( container.find_all(recursive=False)))
    print("Retrieving songs:")

    for song in container.children:
        for i in song.children:
            #need the second iterator to go one down on the heirarchy

            songdata = i.contents[1].contents[1].text
            songs.append(songdata)
            p += deltap
            print(f'{p}% Completed.')
            #lazy workoutaround that might just work for now
    print("Songs retrieved.")

    return songs

def write_songs_to_file(driver, song_list):
    #set name of file
    name = driver.find_element_by_xpath("//h1").text
    #run it through to remove any interesting things
    rx = re.compile(r'\W+')
    name = rx.sub('_',name).strip()

    file = open(f"output/{name}.txt", "w")
    print("Beginning write to file")

    for i in song_list:
        file.write(link+"\n")

    file.close()

def google_oauth_login():
    #should prob implement a way to set the client_secrets_file
    client_secrets_file = "client_secret.apps.googleusercontent.com.json"

    #apparently i should remove this in prod?
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    #should prob implement a way to set and change scopes
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()

    return credentials

def get_youtube_link(search):
    #https://youtube.googleapis.com/youtube/v3/search?maxResults=1&q=Space%20Oddity%20-%202015%20RemasterDavid%20Bowie%20lyrics&key=[API_KEY_HERE]
    key = os.getenv("YOUTUBE_API_KEY")
    maxResults=1
    link = f"https://youtube.googleapis.com/youtube/v3/search?maxResults={maxResults}&key={key}&q={search}"
    r = requests.get(link)
    #standard requests stuff
    assert(r.status_code == 200), "Could not connect to Youtube API"
    #ensure that we can actually use this search

    print("Connected Successfully")
    videoid = r.json()['items'][0]['id']["videoId"]
    #calling api returns a json dict that i have to manipulate
    link = "https://www.youtube.com/watch?v="+videoid

    return link

def addSongToYoutubePlaylist(songLink, playlistid, credentials):
    #pass in the link of the song, the playlist id, and credentials
    videoId = songLink[32:]
    print(videoId)

    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    #idk what this really does, copied from dev google

    request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": playlistid,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": videoId
            }
          }
        }
    )
    response = request.execute()
    print(response)
    # part snippet-> playlistid, resourceid-> kind,videoid

def create_youtube_playlist(name, credentials):
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    request = youtube.playlists().insert(
        part="snippet",
        body={
          "snippet": {
            "title": name
          }
        }
    )
    request.execute()

    print(f'Successfully created playlist {name}')

def export_file_to_playlist(playlistFileName, playlistid, credentials):
    failures = []
    with open('output/'+playlistFileName) as lmao:
        for line in lmao:
            line = line[0:len(line)-1]
            #uhhhhh i dont know why this works but okay we take those
            try:
                addSongToYoutubePlaylist(line, playlistid, credentials)
            except:
                failures.append(line)
            print(f'added {line} to playlist')
    print(failures)










if __name__ == "__main__":
    current = os.getcwd()+"/dp"
    load_dotenv()

    # creds = google_oauth_login()
    # name = str(input("Name a new playlist:"))
    # createYoutubePlaylist(name, creds)

    os.environ['PATH'] += ':'+current
    #shitty nightmare way to make sure that selenium has its geckodriver
    runner = webdriver.Firefox()
    login_to_spotify(runner)
    get_playlists_from_spotify(runner)
    parse_songs_from_spotify(runner)

    #running out of variable names here...

    # createYoutubePlaylist(str(input("Name your new playlist:")), creds)
