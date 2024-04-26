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
    
    def keep_twitter_window_open(self):
        for wind in self.driver.window_handles:
            self.driver.switch_to.window(wind)
            if "https://discord.com/invite/Xana" ==  self.driver.current_url :
                continue
            else :
                self.driver.close()
                
        self.driver.switch_to.default_content()
        
    def switch_yt_window(self):
        for wind in self.driver.window_handles:
            self.driver.switch_to.window(wind)
            if "https://www.youtube.com" in  self.driver.current_url :
                return True
        return False
    
    
    def random_yt_video_activity(self):
        random_videos = random.choice(self.videos_ele_li)
        random_videos.click()
        for _ in range(random.randint(0,3)):
            self.random_swipe_up()
            self.random_sleep()
        self.driver.back()
        self.driver.refresh()
        
    def collect_all_video(self):
        
        videos_ele_li = []
        
        for o_r in range(1,5): 
            for i_r in range(1,5) :
                try:
                    inner_grid_loop_range = self.driver.find_elements(By.XPATH,f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{o_r}]/div/ytd-rich-item-renderer[{i_r}]/div')
                    if inner_grid_loop_range:
                        videos_ele_li.append(inner_grid_loop_range[0])
                except : ...
                    
        self.videos_ele_li = videos_ele_li
        len(self.videos_ele_li)
        len(videos_ele_li)
    
    
    
    def xana_youtube_activites(self):
        self.videos_ele_li = []
        self.click_element('youtbube link',"//a[@href='https://www.youtube.com/c/XANAMetaverse?reload=9']")
        self.random_sleep()
        if not self.switch_yt_window() : 
            self.CloseDriver()
            self.__init__()
            self.xana_youtube_activites()
             
        self.driver.refresh()
        if self.click_element('videos btn','//*[@id="tabsContent"]/yt-tab-group-shape/div[1]/yt-tab-shape[2]'):
            self.old_current_driver_url = self.driver.current_url
            self.random_sleep()
            self.collect_all_video()
        
        for s__ in range(random.randint(0,5)):
            try:
                if self.videos_ele_li :
                    for __ in range(random.randint(0,5)):
                        self.random_yt_video_activity()
            except : ...
            self.videos_ele_li = []
            self.collect_all_video()
            
    def main(self):
        self.xana_youtube_activites()

def run_xana_youtube_activities():
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
        