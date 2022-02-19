#!/usr/local/bin/python3
import os
import re
import time

from bs4 import BeautifulSoup as bs
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
    rx = re.compile('\W+')
    name = rx.sub('_',name).strip()
    file = open(f"output/{name}.txt", "w")


    #sleep for a sec so that the page has time to load
    element = driver.find_element_by_xpath("//div[@data-testid='playlist-tracklist']")
    soup = bs(element.get_attribute('innerHTML'),'html.parser')
    #get the container holding all the songs
    container = soup.contents[1].contents[1]
    #the container holding all the songs is the 2nd child of the 2nd child of playlist tracklist

    songDict = {}

    for song in container.children:
        for i in song.children:
            #need the second iterator to go one down on the heirarchy

            songdata = i.contents[1].contents[1].text
            file.write(songdata+"\n")
            #lazy workoutaround that might just work for now






if __name__ == "__main__":
    current = os.getcwd()+"/dp"

    os.environ['PATH'] += ':'+current
    #shitty nightmare way to make sure that selenium has its geckodriver
    runner = webdriver.Firefox()
    login(runner)
    getPlaylists(runner)
    getSongs(runner)
    #running out of variable names here...
