#!/usr/local/bin/python3
import os
import time

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
    element = driver.find_element_by_xpath("//div[@data-testid='playlist-tracklist']")
    print(element.get_attribute('innerHTML'))



if __name__ == "__main__":
    current = os.getcwd()+"/dp"

    os.environ['PATH'] += ':'+current
    #shitty nightmare way to make sure that selenium has its geckodriver
    runner = webdriver.Firefox()
    login(runner)
    getPlaylists(runner)
    #running out of variable names here...
