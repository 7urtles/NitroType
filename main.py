import sys
import time
import psutil
import argparse
import pyautogui
import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC






from random import randint

class Browser:
    def __init__(self, driver):       
        self.race_text = None
        self.driver = driver
        self.process = psutil.Process(driver.service.process.pid)
        
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
        self.driver.get("https://www.nitrotype.com/race")


    def read_race_text(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'dash-letter')
        text_generator = (element.text for element in elements)
        return text_generator

    def send_keystrokes(self, text_generator, typing_speed):
        print("entering keys")
        for letter in text_generator:
            sys.stdout.write(letter)
            sys.stdout.flush()
            random_delay = randint(1,9)/(typing_speed*10)
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

    def run(self, username, password, typing_speed):
        self.login(username, password)
        time.sleep(2)
        print("Loading New Race...")
        self.start_race()
        
        for i in range(15):
            print(f"Starting in:  {15-i}")
            time.sleep(1)
        print("GO!!!")
        text = self.read_race_text()
        self.send_keystrokes(text, typing_speed)
        time.sleep(6)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('username', type=str, help='username')
    parser.add_argument('password', type=str, help='password')
    parser.add_argument('background', type=bool, help='checkbox value')
    parser.add_argument('typing_speed', type=str, help='bot typing speed')

    args = parser.parse_args()

    print(args.username)
    print(args.password)
    print(args.background)
    print(args.typing_speed)

    try:
        options = uc.ChromeOptions()
        options.add_argument("--password-store=basic")
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--no-sandbox")
        
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            },
        )
        options.set_capability("pageLoadStrategy", "none")

        driver = uc.Chrome(options=options)
        if args.background == True:
            driver.set_window_size(int(1920/1.5), int(1080/1.5))
        else:
            options.add_argument('headless')

        browser = Browser(driver=driver)
        browser.run(username = args.username, password = args.password, typing_speed = int(args.typing_speed))
        
    except ModuleNotFoundError as e:
        # print(e)
        browser.process.terminate()
    except OSError as e:
        # print(e)
        browser.process.terminate()