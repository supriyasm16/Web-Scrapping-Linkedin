from http import cookies
from msilib.schema import Component
from xmlrpc.client import boolean
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import random
import os

class post_grabber():
    def __init__(self, username, password):
        self.username = username
        self.password = password

        #This sets up the options for the Chrome website. The options are set to ignore
        #a few errors that make no difference to the code.
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        #Create the web driver page
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver)
        self.driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin') #Go to Signin page
        self.driver.find_element(By.ID, "username").send_keys(self.username) #Find username field and send username
        time.sleep(0.5)
        self.driver.find_element(By.ID, "password").send_keys(self.password) #Same as username but for password
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, '//*[@type="submit"]').click() #Click submit button

    def run(self, search):
        link_to_search = 'https://www.linkedin.com/search/results/content/?keywords={}&origin=SWITCH_SEARCH_VERTICAL&sid=ZNk'.format(re.sub(r' ', '%20', search))
        self.driver.get(link_to_search) #Do a search
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        not_done = True
        while(not_done):
            try:
                load_more = self.driver.find_element(By.XPATH, '//button[@class="artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button"]')
                load_more.click()
                time.sleep(1)
            except:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            time.sleep(2)
            new_height = self.driver.execute_script('return document.body.scrollHeight')
            
            #Checks if the previous scroll operation did anything. If the height is unchanged then break.
            if(new_height != last_height):
                not_done = False
            else:
                last_height = new_height

        #Click the load more comments button underneath each post
        button = False
        try:
            button = self.driver.find_element(By.XPATH, '//button[@class="comments-comments-list__load-more-comments-button artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"]')
        except:
            pass

        while button:
            self.actions.move_to_element(button).perform()
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="comments-comments-list__load-more-comments-button artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"]')))              
            try:
                button.click()
                time.sleep(random.randint(1, 2))
            except:
                pass

            try:
                button = self.driver.find_element(By.XPATH, '//button[@class="comments-comments-list__load-more-comments-button artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"]')
            except:
                break


        webpage = BeautifulSoup(self.driver.page_source, 'html.parser')

        components = webpage.find_all("h2", class_="visually-hidden") #Find all the div components with a certain property
        i = 0

        current_path = os.getcwd()
        folder = "posts"
        for element in components:
            with open(os.path.join(current_path, "Orcawise_project", folder, "{}.txt".format(i)), 'w', encoding="utf-8") as f:
                tmp = element.find_parent("div").find_parent("div")
                f.write(str(tmp))
                i += 1

    def exit(self):
        self.driver.quit()
