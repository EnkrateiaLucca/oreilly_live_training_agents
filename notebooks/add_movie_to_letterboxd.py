from playwright.sync_api import sync_playwright
from pynput import mouse
import pyautogui
import time
import os
import sys
import time
import pyautogui

def add_movie_to_letterboxd_watchlist(username, password, movie_to_add_to_watchlist,consent_location):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Go to the login page
        page.goto('https://letterboxd.com/')
        
        time.sleep(2)
        # trying clicking on the following coordinates:
        pyautogui.click(x=consent_location[0], y=consent_location[1])
        time.sleep(1)
        # Click on the consent button
        page.click('text=Sign in')
        page.wait_for_load_state()
        # Fill in the username and password fields
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)

        # Click the login button and wait for navigation
        # press tab twice and then enter
        page.keyboard.press('Tab')
        page.keyboard.press('Tab')
        page.keyboard.press('Enter')
        
        time.sleep(1)
        
        # click in the search bar and type in a movie (input in this function)
        # click in search bar by looking at xpath
        page.click('//*[@id="header"]/section/div[1]/div/nav/ul/li[7]/a')
        page.fill('input[name="q"]', movie_to_add_to_watchlist)
        # click enter
        page.keyboard.press('Enter')
        
        # click on this xpath
        page.click('//*[@id="content"]/div/div/section/ul/li[1]/div[2]/h2/span')
        
        page.wait_for_load_state()
        
        page.click('//*[@id="userpanel"]/ul/li[1]/span[4]')
        
        time.sleep(3)
        # Close the browser
        context.close()
        browser.close()

def record_click_position():
    click_position = None  # Variable to store the click position

    def on_click(x, y, button, pressed):
        nonlocal click_position  # Refer to the non-local variable
        if pressed:
            click_position = pyautogui.position()
            return False  # Stop the listener

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    return click_position

def reset_consent_location():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Go to the login page
        page.goto('https://letterboxd.com/')
        consent_location = record_click_position()
    
    return consent_location


if __name__ == '__main__':
    letterboxd_user = os.environ["LETTERBOXD_USER"]
    letterboxd_pwd = os.environ["LETTERBOXD_PWD"]
    movie = sys.argv[1]
    try:
        add_movie_to_letterboxd_watchlist(letterboxd_user, letterboxd_pwd, movie, consent_location=(776, 673))
    except Exception as e:
        print("You had this error: ", e)
        reset_loc = input("Would you like to reset the consent location? (y/n)")
        if reset_loc == "y":
            consent_location = reset_consent_location()
            print("Your new consent button location is: ")
            print(consent_location)
            run_again = input("Would you like to run the script again? (y/n)")
            if run_again == "y":
                add_movie_to_letterboxd_watchlist(letterboxd_user, letterboxd_pwd, movie, consent_location=consent_location)
            else:
                print("Ok, bye!")