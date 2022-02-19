#!/usr/local/bin/python3
import os

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
    #await the login or throw timeout error
    #and now you're logged in!

def getPlaylists(driver):
    driver.get("https://open.spotify.com/collection/playlists")
    print()


if __name__ == "__main__":
    current = os.getcwd()+"/dp"

    os.environ['PATH'] += ':'+current
    #shitty nightmare way to make sure that selenium has its geckodriver
    runner = webdriver.Firefox()
    #running out of variable names here...
