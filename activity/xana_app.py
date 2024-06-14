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
        pass
    
    
    def xana_app_random_activites(self):
        for _22 in range(10):
            if not self.find_element(By.XPATH,'//*[@id="__next"]/div[3]/div/div[1]/section/div[2]/div/div') : 
                self.driver.refresh()
                self.random_sleep()                
            else : break
<<<<<<< HEAD
            ...
            
        defualt_wind_handles = self.driver.window_handles[0]
        def random_clicks_cet(obj):
            ...
=======
            
        defualt_wind_handles = self.driver.window_handles[0]
        def random_clicks_cet(obj):
>>>>>>> 49bdd2c ( rm       breakpoint()
            for _ in range(random.randint(0,4)): 
                try:
                    self.driver.execute_script('document.querySelector("#__next > div:nth-child(6) > div > div:nth-child(2) > section > div.slick-slider.filter-Slider.hot-space-filters.home.slick-initialized > div > div > div:nth-child(54) > div > div").click()')
                except Exception as e:
                    ...
                obj[random.randint(0,len(obj))].find_element(By.XPATH,'./div/div').click()
                self.random_sleep()
                
        def login_activities_check():
            self.click_element('Login btn','walletConnectModal',By.ID)
            self.random_sleep()
            all_login_types = self.driver.find_elements(By.XPATH,'/html/body/div[4]/div/div/div/div/div[2]/form/*')
            all_login_types[random.randint(0, len(all_login_types))].click()
            self.random_sleep(5,9)
            
            self.driver.switch_to.default_content()
            for i in self.driver.window_handles :
                if i != defualt_wind_handles :
                    self.driver.switch_to.window(i)
                    self.driver.close()
                    
                self.driver.switch_to.default_content()

            self.random_sleep()
            try:
                self.driver.execute_script('document.querySelector("body > wcm-modal:nth-child(29)").shadowRoot.querySelector("#wcm-modal > div > wcm-modal-backcard").shadowRoot.querySelector("div.wcm-toolbar > button").click()')
            except Exception as e:
                ...
                
            self.click_element('Close login popup','/html/body/div[4]/div/div/div/div/span',timeout=3)

            self.ensure_click()
        
        def random_scroll_on_chat():
            chat_boy = self.find_element('chat body','chat-body',By.CLASS_NAME)
            
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", chat_boy)
        
        for __ in range(random.randint(2,5)):
            random_activites = random.randint(1,5)
            
            if random_activites == 1 :
                hotspace_category =[ i for i in self.driver.find_elements(By.XPATH,'//*[@id="__next"]/div[3]/div/div[1]/section/div[2]/div/div/*') if i.is_displayed()][:-3]
                hotspace_category = hotspace_category[:-3] if len(hotspace_category) > 3 else hotspace_category
                if hotspace_category : 
                    random_clicks_cet(hotspace_category)
                
                
            elif random_activites == 2 :
                hotgames_category =[ i for i in self.driver.find_elements(By.XPATH,'//*[@id="__next"]/div[3]/div/div[1]/section/div[2]/div/div/*') if i.is_displayed()][:-3]
                hotgames_category = hotgames_category[:-3] if len(hotgames_category) > 3 else hotgames_category
                if hotgames_category : 
                    random_clicks_cet(hotgames_category)
                
            elif random_activites == 3:
                self.random_swipe_up()
                
            elif random_activites == 4:
                for _ in range(random.randint(2,5)):
                    header_eles = self.driver.find_elements(By.XPATH,'//*[@id="navbar"]/div/nav/div/*')[:6]
                    self.hover_on_an_element(random.choice(header_eles))
                    self.action.move_to_element(random.choice(header_eles)).perform()
                    # self.random_sleep()
            elif random_activites == 5:
                login_activities_check()
            
            return
         
    def main(self):
        self.driver.get(views_links[0])
        self.random_sleep()
        self.driver.refresh()
        self.random_sleep()
        self.xana_app_random_activites()
        ...
    
# if __name__ == '__main__':

def run_xana_app_activities(driver):
    bt = xana_net(driver)

    @measure_time
    def Xana_app_activities():
        bt.main()
    total_time_elsped = 0
    recommanded_timer = random.randint(15,80)
    print('recommanded timer :',recommanded_timer)
    while total_time_elsped < recommanded_timer:
        time_elsped, fun_result = Xana_app_activities()
        total_time_elsped += time_elsped
        print(total_time_elsped)
        
# run_xana_app_activities()