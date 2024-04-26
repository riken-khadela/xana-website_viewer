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
            if "https://twitter.com/XANAMetaverse" ==  self.driver.current_url :
                continue
            else :
                self.driver.close()
                
        self.driver.switch_to.default_content()
        
    def open_random_post(self):
        all_posts_element = self.driver.find_elements(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/*')
        random_posts = random.choice(all_posts_element)
        self.hover_on_an_element(random_posts)
        random_posts.click()
        self.random_sleep()
        self.driver.back()
        all_posts_element = self.driver.find_elements(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/*')
        self.hover_on_an_element(all_posts_element[-1])
    
    def keep_old_site_open(self):
        for _ in range(3):
            if not self.last_driver_url == self.driver.current_url :
                self.driver.back()
            else : break
        else :
            self.driver.get(self.last_driver_url)
            
    def xana_twitter_activites(self):
        
        self.last_driver_url = self.driver.current_url
        def visit_setting():
            self.last_driver_url = self.driver.current_url
            settings_ele = self.driver.find_elements(By.XPATH,'//a[@href="/settings"]') 
            if settings_ele :
                settings_ele[0].click()
            self.keep_old_site_open()
                
        def hover_Atags_into_descriptions():
            self.last_driver_url = self.driver.current_url
            self.driver.execute_script(f"window.scrollTo(0, 0);")
            
            Descriptions = self.driver.find_elements(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[3]/div/div')
            if Descriptions :
                all_Atags = Descriptions[0].find_elements(By.TAG_NAME,'a')
                if all_Atags :
                    for __ in range(random.randint(0,len(all_Atags))):
                        try:
                            random_Atags = random.choice(all_Atags)
                            self.hover_on_an_element(random_Atags)
                            
                            random_Atags.click()
                            if 3 == random.randint(0,10):
                                random_Atags.click()
                        except : ...
                        self.random_sleep()
                    self.keep_old_site_open()
            self.keep_twitter_window_open()
                
        def visit_highlights(): 
            self.last_driver_url = self.driver.current_url
            self.click_element('High lights',"//a[@href='/XANAMetaverse/highlights']")
            self.click_element('High lights','//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[1]/div/div/article')
            try : self.driver.execute_script('document.querySelector("#react-root > div > div > div.css-175oi2r.r-1f2l425.r-13qz1uu.r-417010.r-18u37iz > main > div > div > div > div.css-175oi2r.r-14lw9ot.r-jxzhtn.r-13l2t4g.r-1ljd8xs.r-1phboty.r-16y2uox.r-184en5c.r-61z16t.r-11wrixw.r-1jgb5lz.r-13qz1uu.r-1ye8kvj > div > div:nth-child(3) > div > div > section > div > div > div:nth-child(1) > div > div > article").click()')
            except : ...
            self.random_sleep()
            self.keep_old_site_open()
            self.click_element('Posts',"//a[@href='/XANAMetaverse']")
                
        twitter_link_ = self.find_element('twitter link',"//a[@href='https://twitter.com/XANAMetaverse']")
        self.hover_on_an_element(twitter_link_)
        self.random_sleep()
        twitter_link_.click()
        self.random_sleep()
        self.keep_twitter_window_open()
        self.last_driver_url = self.driver.current_url
        
        visit_highlights()
        self.open_random_post()
        hover_Atags_into_descriptions()
        visit_setting()
        
        functions = [visit_highlights, self.open_random_post, hover_Atags_into_descriptions, visit_setting]
        for func in range(random.randint(0,5)):
            func = random.randint(0,len(functions))
            if func == len(functions) : continue
            functions[func]()
        
    def main(self):
        self.xana_twitter_activites()

def run_xana_twitter_activities():
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
        