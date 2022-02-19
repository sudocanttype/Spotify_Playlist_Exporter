#!/usr/local/bin/python3
import os
import re
import time

import requests
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login(driver):

    driver.get("https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F")
    print("Please insert your credentials and login.")
    WebDriverWait(driver, 1000000).until(
        EC.url_matches("https://open.spotify.com/")
    )
    # getPlaylists(driver)
    #await the login or throw timeout error
    #and now you're logged in!

def getPlaylists(driver):
    #assumes you are already logged in
    driver.get("https://open.spotify.com/collection/playlists")
    print("Select a playlist from the screen")
    WebDriverWait(driver, 1000000).until(
        EC.url_contains("https://open.spotify.com/playlist/")
    )
    #and now you're on the playlist page
    time.sleep(1)

def getSongs(driver):
    #parse the html from the playlist page
    time.sleep(1)

    #set name of file
    name = driver.find_element_by_xpath("//h1").text
    #run it through to remove any interesting things
    rx = re.compile(r'\W+')
    name = rx.sub('_',name).strip()
    file = open(f"output/{name}.txt", "w")


    #sleep for a sec so that the page has time to load
    element = driver.find_element_by_xpath("//div[@data-testid='playlist-tracklist']")
    soup = bs(element.get_attribute('innerHTML'),'html.parser')
    #get the container holding all the songs
    container = soup.contents[1].contents[1]
    #the container holding all the songs is the 2nd child of the 2nd child of playlist tracklist


    #loading percentage
    p = 0
    deltap = int(100/len( container.find_all(recursive=False)))
    print("Beginning write to file")

    for song in container.children:
        for i in song.children:
            #need the second iterator to go one down on the heirarchy

            songdata = i.contents[1].contents[1].text
            link = getYoutubeVideoLink(songdata+" lyrics")
            file.write(link+"\n")
            p += deltap
            print(f'{p}% Completed.')
            #lazy workoutaround that might just work for now
    print("Done writing to file")
    file.close()


def getYoutubeVideoLink(search):
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






if __name__ == "__main__":
    current = os.getcwd()+"/dp"
    load_dotenv()

    os.environ['PATH'] += ':'+current
    #shitty nightmare way to make sure that selenium has its geckodriver
    runner = webdriver.Firefox()
    login(runner)
    getPlaylists(runner)
    getSongs(runner)
    #running out of variable names here...
