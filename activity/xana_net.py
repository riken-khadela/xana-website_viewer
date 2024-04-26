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
    
    
    def xana_net_random_activites(self):
        
        def open_random_blog_points():
            for _1 in range(random.randint(2,5)):
                self.click_element('content 3 dot','fix_tocbtn',By.ID)
                if self.find_element('Index of table','index_modal',By.ID) :
                    Ol_ele = self.find_element('Index of table','index_modal',By.ID).find_elements(By.TAG_NAME,'ol')
                    if Ol_ele:
                        a_tags_table_content = Ol_ele[0].find_elements(By.TAG_NAME,'a')
                        if a_tags_table_content :
                            random.choice(a_tags_table_content).click()
                self.random_sleep()
        
        def open_random_blogs():
                all_blogs_a_tag = self.driver.find_elements(By.XPATH,"//a[contains(@href, 'https://xana.net/blog/')]")
                for _ in range(len(all_blogs_a_tag)):
                    try :
                        random_choosed_tag = random.choice(all_blogs_a_tag)
                        self.hover_on_an_element(random_choosed_tag)
                        self.random_sleep()
                        random_choosed_tag.click()
                        time.sleep(2)
                        break
                    except Exception as e:...


                
                if not "https://xana.net/blog" in self.driver.current_url:
                    self.random_sleep()
                
                self.click_element('Searchbtn','//*[@id="gnav"]/ul/li[3]/button')
                self.random_sleep()
                self.click_element('Searchbtn','//*[@id="gnav"]/ul/li[3]/button')
                

                categories_blogs = self.driver.find_elements(By.XPATH,'//*[@id="block-6"]/div/div/ul/*')
                if categories_blogs:
                    categories_blogs_choosen_blog = random.choice(categories_blogs)
                    self.hover_on_an_element(categories_blogs_choosen_blog)
                    categories_blogs_choosen_blog.find_element(By.TAG_NAME,'a').click()
                    self.random_sleep()
                
                side_bar_blogs = self.driver.find_elements(By.XPATH,'//*[@id="swell_new_posts-3"]/ul/*')
                if side_bar_blogs :
                    side_bar_blogs_choosen_blog = random.choice(side_bar_blogs)
                    self.hover_on_an_element(side_bar_blogs_choosen_blog)
                    self.random_sleep()
                    side_bar_blogs_choosen_blog.click()
                    self.random_sleep()
        
        for __ in range(random.randint(2,4)):
            random_activities = random.randint(0,5)    
            random_activities = 3
            # hover on header options
            if random_activities == 0:
                for _ in range(random.randint(2,5)):
                    header_eles = self.driver.find_elements(By.XPATH,'//*[@id="nav-bar"]/div/div[2]/*')[:6]
                    self.hover_on_an_element(random.choice(header_eles))
                    
            if random_activities == 1:
                # try to read some blogs
                all_blogs_a_tag = self.driver.find_elements(By.XPATH,"//a[contains(@href, 'https://xana.net/blog/')]")
                random_choosed_tag = random.choice(all_blogs_a_tag)
                self.hover_on_an_element(random_choosed_tag)
                self.random_sleep()
                try:
                    for i in range(3):
                        random_choosed_tag.click()
                        time.sleep(2)
                except Exception as e:...
                
                
                if not "https://xana.net/blog" in self.driver.current_url:
                    self.random_sleep()
                    continue
                
                self.click_element('Searchbtn','//*[@id="gnav"]/ul/li[3]/button')
                self.random_sleep()
                self.click_element('Searchbtn','//*[@id="gnav"]/ul/li[3]/button')
                
                self.random_sleep()

                categories_blogs = self.driver.find_elements(By.XPATH,'//*[@id="block-6"]/div/div/ul/*')
                if categories_blogs:
                    categories_blogs_choosen_blog = random.choice(categories_blogs)
                    self.hover_on_an_element(side_bar_blogs_choosen_blog)
                    categories_blogs_choosen_blog.find_element(By.TAG_NAME,'a').click()
                    self.random_sleep()
                
                side_bar_blogs = self.driver.find_elements(By.XPATH,'//*[@id="swell_new_posts-3"]/ul/*')
                if side_bar_blogs :
                    side_bar_blogs_choosen_blog = random.choice(side_bar_blogs)
                    self.hover_on_an_element(side_bar_blogs_choosen_blog)
                    self.random_sleep()
                    side_bar_blogs_choosen_blog.click()
                    self.random_sleep()
                
                
            if random_activities == 2 :
                # Random hove on footer 
                
                row_footer_xpaths = [ 
                    '//*[@id="w-node-_2c4cb8f7-7bb0-4268-c510-64705bfa9987-df63d195"]',
                    '//*[@id="w-node-_2c4cb8f7-7bb0-4268-c510-64705bfa9953-df63d195"]',
                    '/html/body/footer[1]/div[2]/div/div[3]/div[1]/div[3]',
                    '//*[@id="w-node-_2c4cb8f7-7bb0-4268-c510-64705bfa99e5-df63d195"]',
                    '/html/body/footer[1]/div[2]/div/div[3]/div[1]/div[5]',
                ]
                for _ in range(0,3):
                    self.random_sleep()
                    try :
                        selected_footer = self.driver.find_element(By.XPATH,random.choice(row_footer_xpaths))
                        selected_footer_eles = selected_footer.find_elements(By.TAG_NAME,'a')
                        for ___ in range(0,4):
                            self.hover_on_an_element(random.choice(selected_footer_eles))
                            self.random_sleep()
                    except : ...
            
            if random_activities == 3:
                open_random_blogs()
                self.random_swipe_up()
                self.random_swipe_up()
                open_random_blog_points()
        
                
    
         
    def main(self):
        
        self.xana_net_random_activites()
        ...
    
# if __name__ == '__main__':

def run_xana_net_activities(driver):
    bt = xana_net(driver)

    @measure_time
    def Xana_app_activities():
        bt.main()
    total_time_elsped = 0
    
    recommanded_timer = random.randint(420,480)
    while total_time_elsped < recommanded_timer:
        time_elsped, fun_result = Xana_app_activities()
        total_time_elsped += time_elsped
        print(total_time_elsped)
        