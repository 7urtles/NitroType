from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui


import undetected_chromedriver as uc
from random import randint

import time

class Browser:
    def __init__(self, driver):       
        self.race_text = None
        self.driver = driver
        
    def login(self, username, password):
        self.driver.get("https://www.nitrotype.com/login")
        time.sleep(3)
        username_input_box = self.driver.find_element(By.NAME, "username")
        username_input_box.send_keys(username)

        password_input_box = self.driver.find_element(By.NAME, "password")
        password_input_box.send_keys(password)

        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

    def start_race(self):
        print("starting race")
        self.driver.get("https://www.nitrotype.com/race")

    def read_race_text(self):
        print("reading race text")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dash-letter'))
        )
        print("racing text found")
        elements = self.driver.find_elements(By.CLASS_NAME, 'dash-letter')
        text_generator = (element.text for element in elements)
        return text_generator

    def send_keystrokes(self, text_generator = None):
        print("entering keys")
        for letter in text_generator:
        # for letter in self.race_text:
            random_delay = randint(1,9)/60
            time.sleep(random_delay)
            actions = ActionChains(self.driver)
            actions.send_keys(letter).perform()
        else:
            return True
    
    def check_race_started(self):
        button_location = pyautogui.locateCenterOnScreen('start_race_indicator.png')
        if button_location:
            print("race started")
            return True
        else:
            print("waiting for start indicator")
            return False

    def run(self):
        self.login('ProbablyBanned', 'Earthday19!@22')
        time.sleep(2)
        self.start_race()
        input("Press enter to start race....")
        text = self.read_race_text()
        self.send_keystrokes(text)
        time.sleep(5)
        self.driver.quit()

if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.add_argument("--password-store=basic")
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )
    options.set_capability("pageLoadStrategy", "none")
    driver = uc.Chrome(options=options)
    browser = Browser(driver=driver)
    browser.run()