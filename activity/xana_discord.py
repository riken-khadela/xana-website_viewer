from lib2to3.pgen2 import driver
import random, time
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,NoSuchElementException,WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.service import Service
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor, wait
import logging
from webdriver_manager.chrome import ChromeDriverManager
# from ..others.dbb import create_db_ifnot,add_data_with_view, get_views_per_day, get_today_views
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import pickle
import argparse, subprocess
from pathlib import Path
import logging, os, inspect, subprocess
from logging import handlers
from driver import driver_class, measure_time


views_links = [
    "https://xana.net/app",
    "https://xana.net/",
    ]


class xana_net(driver_class):
    def __init__(self) -> None:
        self.driver = driver
        self.random_sleep()
        pass
    
    def keep_twitter_window_open(self):
        for wind in self.driver.window_handles:
            self.driver.switch_to.window(wind)
            if "https://discord.com/invite/Xana" ==  self.driver.current_url :
                continue
            else :
                self.driver.close()
                
        self.driver.switch_to.default_content()
        
    def xana_discord_activites(self):
        
        self.last_driver_url = self.driver.current_url
        discord_link_ = self.click_element('Discord link',"//a[@href='https://discord.com/invite/Xana']")
        self.random_sleep()
    
        
    def main(self):
        self.xana_discord_activites()

def run_xana_discord_activities():
    bt = xana_net()

    @measure_time
    def Xana_app_activities():
        bt.main()
    total_time_elsped = 0
    recommanded_timer = random.randint(420,480)
    while total_time_elsped < recommanded_timer:
    
        time_elsped, fun_result = Xana_app_activities()
        total_time_elsped += time_elsped
        print(total_time_elsped)
        