from playwright.sync_api import sync_playwright
from pynput import mouse
import pyautogui
import time
import os
import sys
import time
import pyautogui

def login_to_letterboxd(page, username, pwd, consent_box_location):
    """Log in to a letterboxd account."""
    # Go to the login page
    page.goto('https://letterboxd.com/')

    time.sleep(2)
    # trying clicking on the following coordinates:
    pyautogui.click(x=consent_box_location[0], y=consent_box_location[1])
    time.sleep(1)
    # Click on the consent button
    page.click('text=Sign in')
    page.wait_for_load_state()
    # Fill in the username and password fields
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', pwd)

    # Click the login button and wait for navigation
    # press tab twice and then enter
    page.keyboard.press('Tab')
    page.keyboard.press('Tab')
    page.keyboard.press('Enter')

    time.sleep(1)

    return page

def search_movie_or_keyword(page, movie_title: str, movie=True):
    # click in the search bar and type in a movie (input in this function)
    # click in search bar by looking at xpath
    page.click('//*[@id="header"]/section/div[1]/div/nav/ul/li[7]/a')
    page.fill('input[name="q"]', movie_title)
    # click enter
    page.keyboard.press('Enter')
    
    # click on this xpath
    if movie:
        page.click('//*[@id="content"]/div/div/section/ul/li[1]/div[2]/h2/span')
    else:
        page.click('//*[@id="content"]/div/div/section/ul/li[1]/section/a')
    
    page.wait_for_load_state()
    return page

def search_movie_lists(page):
    # Select all elements that match the criteria
    elements = page.query_selector_all('li.poster-container.film-watched')
    movies_list = []
    # Iterate over the elements to do something with each
    for element in elements:
        # For example, get the inner text of each element
        text = element.text_content()
        movies_list.append(text)
        print(text)
    
    return movies_list


def test_browsing_feature(function, *args, **kwargs):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page = function(page, *args, **kwargs)



letterboxd_user = os.environ["LETTERBOXD_USER"]
letterboxd_pwd = os.environ["LETTERBOXD_PWD"]
consent_box_location = (776, 693)

# test_browsing_feature(login_to_letterboxd,letterboxd_user, letterboxd_pwd, consent_box_location)
movie_kw = "dark comedy"
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page = login_to_letterboxd(page, letterboxd_user, letterboxd_pwd, consent_box_location)
    page = search_movie_or_keyword(page, movie_kw, movie=False)
    movie_list = search_movie_lists(page)
    print("finished")
    time.sleep(1)
    context.close()
    browser.close()