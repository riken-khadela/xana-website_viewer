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
    def __init__(self,driver) -> None:
        self.driver = driver
        self.driver.get(views_links[-1])
        self.random_sleep()
        pass
    
       
    def switch_yt_window(self):
        for wind in self.driver.window_handles:
            self.driver.switch_to.window(wind)
            if "https://www.instagram.com" in  self.driver.current_url :
                return True
        return False
    

    def view_some_post(self):
        
        ...
    
    def random_scrolling(self):
        for __ in range(random.randint(0,9)):
            self.self.random_swipe_up()
    
    def scroll_high_light(self):
        for _ in range(random.randint(0,5)):
            self.click_element('scroll highlight right side','/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/section/main/div/div[1]/div/div/button')
            self.random_sleep()
    
    def collect_reel_a(self):
        self.reels_ele_li = []
        self.driver.current_url
        for o_r in range(1,5): 
            for i_r in range(1,4) :
                try:
                    inner_grid_loop_range = self.driver.find_elements(By.XPATH,f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/section/main/div/div[3]/div/div/div/div[{o_r}]/div[{i_r}]/div/a")
                    if inner_grid_loop_range:
                        self.reels_ele_li.append(inner_grid_loop_range[0])
                except : ...
    
    def insta_reel_activity(self):
        
        self.find_element('Instagram reel btn',"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/section/main/div/div[3]/div/div/div/div[1]/div[4]/div/a")
        if self.find_element('Instagram reel btn',"//a[@href='/xanametaverse/reels/']"):
            self.hover_on_an_element(self.find_element('Instagram reel btn',"//a[@href='/xanametaverse/reels/']"))
            self.random_sleep()
            self.click_element('Instagram reel btn',"//a[@href='/xanametaverse/reels/']")
            self.random_sleep()
            self.collect_reel_a()
            if self.reels_ele_li : random.choice(self.reels_ele_li).click()
            self.random_sleep(5,10)
            self.click_element('Insta login close','/html/body/div[8]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div')
            self.random_sleep()
            self.click_element('close reel','/html/body/div[7]/div[1]/div/div[2]/div')
            self.random_swipe_up()
            # /html/body/div[7]/div[1]/div/div[2]/div
            
        
    
    def xana_youtube_activites(self):
<<<<<<< HEAD
        ...
=======
>>>>>>> 49bdd2c ( rm       breakpoint()
        self.videos_ele_li = []
        if self.find_element('Instagram link',"//a[@href='https://www.instagram.com/xanametaverse/']"):
            self.hover_on_an_element(self.find_element('Instagram link',"//a[@href='https://www.instagram.com/xanametaverse/']"))
            self.random_sleep()
            self.click_element('Instagram link',"//a[@href='https://www.instagram.com/xanametaverse/']")
        self.random_sleep()
        if not self.switch_yt_window() : 
            self.CloseDriver()
            self.__init__()
            self.xana_youtube_activites()
            
        for _ in range(random.randint(3,8)):
            random.choice([self.insta_reel_activity, self.scroll_high_light])()
            
    def main(self):
        self.xana_youtube_activites()

def run_xana_insta_activities():
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
        