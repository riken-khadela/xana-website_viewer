import threading
import time
import random
import undetected_chromedriver as uc
import time
import random, json
from typing import Union
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException, WebDriverException
from dbb import add_data_with_view
import datetime

driver = ''
import subprocess



    

import time
import random, json
from typing import Union


class WebDriverUtility:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.options = None  # Now defining options here, although it might still be better set in each subclass if different options are needed per use case.

    def drivers_options(self):
        pass


    def close_driver(self):
        self.driver.quit()

    def navigate_to(self, url):
        self.driver.get(url)

    def safe_send_keys(self, locator, text, by=By.XPATH, timeout=10):
        element = self.find_element(locator, by, timeout)
        if element:
            element.send_keys(text)


    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def wait_for_element_visible(self, locator, by=By.XPATH, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
        except TimeoutException:
            print(f"Element with locator {locator} not visible within {timeout} seconds")
            return None

    def wait_for_element_invisible(self, locator, by=By.XPATH, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, locator))
            )
        except TimeoutException:
            print(f"Element with locator {locator} still visible after {timeout} seconds")
            return False

    def get_text(self, locator, by=By.XPATH, default=""):
        element = self.find_element(locator, by)
        return element.text if element else default

    def find_element(self, locator, by=By.XPATH, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            return element
        except TimeoutException:
            print(f"Timeout while trying to find element with locator: {locator}")
            return None
    
    def find_elements(self, locator, by=By.XPATH, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, locator))
            )
            return elements
        except TimeoutException:
            print(f"Timeout while trying to find elements with locator: {locator}")
            return []

    def click_element(self, locator, by=By.XPATH, timeout=10):
        element = self.find_element(locator, by, timeout)
        if element:
            self.ensure_click(element)

    def ensure_click(self, element, attempts=3):
        successful = False
        current_attempt = 0
        while not successful and current_attempt < attempts:
            try:
                actions = ActionChains(self.driver)
                # Move to the element (hover over it) to make the action seem more human-like
                actions.move_to_element(element)
                # Introduce a slight pause before clicking to mimic human behavior
                time.sleep(random.uniform(0.5, 1.5))
                # Perform the click action
                actions.click().perform()
                successful = True
            except ElementClickInterceptedException:
                print("Element is not clickable, attempting to scroll and retry.")
                self.scroll_to_element(element)
            except StaleElementReferenceException:
                print("Stale element reference, re-fetching the element.")
                element = self.refresh_element(element)
            except Exception as e:
                print(f"Unexpected error clicking element: {str(e)}")
            finally:
                current_attempt += 1

        if not successful:
            print("Attempting final click using JavaScript.")
            self.click_with_javascript(element)
            

    def simulate_human_movement(self):
        print('start human movement')
        action = ActionChains(self.driver)
        
        random_x = random.randint(200, 1200)  # random x point
        random_y = random.randint(200, 1200)  # random y point

        action.move_by_offset(random_x, random_y).perform()

        time.sleep(random.uniform(0.5, 1.5))  # random delay between 0.5 to 1.5 sec


    def refresh_element(self, element):
        # Re-find the element in the DOM to avoid StaleElementReferenceException
        locator = element.get_attribute('xpath')
        return self.find_element(locator)

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def click_with_javascript(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def capture_screenshot(self, file_path):
        self.driver.save_screenshot(file_path)

    def get_all_tabs(self):
        return self.driver.window_handles
    
    def switch_to_tab(self, window_name):
        if isinstance(window_name, int):
            self.driver.switch_to.window(self.driver.window_handles[window_name])
        else:
            self.driver.switch_to.window(window_name)

    def switch_to_iframe(self, frame_reference: Union[str, int, WebElement]):
        self.driver.switch_to.frame(frame_reference)
    
    def getvalue_byscript(self,script = ''):
        value = self.driver.execute_script(f'return {script}')  
        return value
    
    def new_tab(self, url=None):
        self.driver.tab_new(url)
    
    def random_sleep(self,a=3,b=7,reson = ""):
        random_time = random.randint(a,b)
        print('time sleep randomly :',random_time) if not reson else print('time sleep randomly :',random_time,f' for {reson}')
        time.sleep(random_time)

    def scroll_smoothly(self, direction="down", max_scroll=3):
        """ Scroll smoothly in the specified direction.
        
        :param direction: 'up' or 'down'
        :param max_scroll: maximum number of scroll actions
        """
        scroll_count = 0
        while scroll_count < max_scroll:
            try:
                if direction == "down":
                    self.driver.execute_script("window.scrollBy(0, window.innerHeight/4);")
                else:
                    self.driver.execute_script("window.scrollBy(0, -window.innerHeight/4);")
                time.sleep(random.uniform(0.5, 1.5))  # Random sleep to mimic human behavior
            except:pass
            scroll_count += 1
            
    def load_cookies(self, load_path):
        """ Load cookies from a file and add them to the current session. """
        with open(load_path, 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
    
    def get_cookies(self, save_path):
        """ Save all cookies to a file. """
        cookies = self.driver.get_cookies()
        with open(save_path, 'w') as file:
            json.dump(cookies, file)

    def refresh_driver(self):
        self.driver.refresh()
        
        
        
        



# while True:
#     start_threads()
#     time.sleep(1)  # Wait a short while before starting again
    
    
    
class xana_viewer(WebDriverUtility):
    
    def __init__(self) -> None:
        self.referers = ['https://search.yahoo.com/', 'https://duckduckgo.com/', 'https://www.google.com/',
            'https://www.bing.com/', 'https://t.co/', 'https://www.instagram.com/xanametaverse/']

    
    def get_driver(self):
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--incognito")
        options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT {random.randint(6, 10)}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.{random.randint(3000, 4000)}.87 Safari/537.36")
        prefs = {
            "download.prompt_for_download": True,  # Always ask for download location
            "download.default_directory": "",  # Disable default directory for downloads
            "download_restrictions": 3  # Block all downloads
        }
        options.add_experimental_option("prefs", prefs)
        
        self.driver = uc.Chrome(options=options, version_main=int(self.get_google_chrome_version()))
            
    def get_cmd_output(self, command : str = ''):
        try:
            output = subprocess.check_output(
                command,
                shell=True
            ).decode()
            
            return output.replace('\n','').strip()
                        
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.output}")
        return None
    
    def get_google_chrome_version(self):
        output = self.get_cmd_output(f'''google-chrome --version''')
        return output.replace('Google Chrome ','').split('.')[0]
    
    def check_ga_loaded(self,):
        track = self.find_element("//script[contains(@src, 'googletagmanager.com/gtag/js') or contains(@src, 'google-analytics.com/analytics.js')]", timeout=30)
        if track:
            return True
        return False
        
    def random_activity(self):
        end_time = time.time() + 1 * 60  # 1 minute from now
        while time.time() < end_time:
            # Random scroll
            self.scroll_smoothly(max_scroll=random.randint(2,4))
            elements = self.find_elements('//*')
            if elements:
                element_to_click = random.choice(elements)
                self.ensure_click(element_to_click)
            # Wait for a short random interval
            time.sleep(random.uniform(0.5, 2))
    
    def randomly_scroll(self):
        print('start random scroll')
        self.scroll_smoothly(random.choice(['up', 'down']))

    def play_random_video(self):
        video_tag = self.find_elements('video', By.TAG_NAME)
        self.scroll_to_element(random.choice(video_tag))
        self.random_sleep(30, 50)  
        
    def xana_nft_randomly_action(self ):
        random_ele = ['style_collection-card__znXis', 'style_collection-card__PGcs0', 'style_nft-card__ZBQK6']
        self.randomly_click_on_multiple_element(random_ele)

    def xana_nftduel_randomly_action(self):
        random_ele = ['card-2']
        self.randomly_click_on_multiple_element(random_ele)

    def xana_app_randomly_action(self):
        random_ele = ['slick-slider']
        self.randomly_click_on_multiple_element(random_ele,number= 4)

    def xana_blog_randomly_action(self):
        random_ele = ['c-tabList__button']
        self.randomly_click_on_multiple_element(random_ele)
        ul_tags = self.find_elements('//*[contains(@id, "post_list_tab")]')
        for ul in ul_tags:
            if ul.is_displayed():
                li_tags = ul.find_elements(By.TAG_NAME, 'li')
                self.ensure_click(random.choice(li_tags))
                break
        self.switch_to_tab(-1)
        self.scroll_smoothly(max_scroll=random.randint(6,10))

    def randomly_click_on_multiple_element(self, element_list=[], selector=By.CLASS_NAME, number=1):
        number = len(element_list) if len(element_list) < number else number
        for i in range(number):
            class_name = random.choice(element_list)
            lanchpad = self.find_elements(class_name, selector)
            self.ensure_click(random.choice(lanchpad))
            self.random_sleep(7,10) 

        
    def set_referer(self, url:str='' ):
        urls = ['https://xana.net/app', 'https://xana.net/blog/', 'https://xana.net/nft', 'https://xana.net/nftduel/en/', 'https://xana.net/XANASUMMIT/']
        if not url: url = random.choice(urls)
        referer = random.choice(self.referers)
        if referer:
            # if 'search.yahoo.com' in referer:
            #     self.navigate_to(referer)
            #     self.random_sleep()
            #     self.navigate_to('https://duckduckgo.com/')
            #     self.random_sleep()
            #     breakpoint()
            #     self.driver.execute_script('''window.history.pushState({urlPath: arguments[0]}, '', arguments[0]);''', referer)
            # else:
            self.navigate_to(referer)
            self.random_sleep()
            self.driver.execute_script(
                "window.location.href = '{}';".format(url))
        else:
            self.navigate_to(url)

    def activity_for_xana_nft(self):
        self.set_referer('https://xana.net/nft')
        actions = [
            # self.simulate_human_movement,
            self.randomly_scroll,
            self.xana_nft_randomly_action
        ]

        # Randomly choose an action and execute it
        random.shuffle(actions)
        for i in actions:
            i()

    def activity_for_xana_summit(self):
        self.set_referer('https://xana.net/XANASUMMIT/')
        actions = [
            # self.simulate_human_movement,
            self.randomly_scroll,
            self.play_random_video
        ]

        # Randomly choose an action and execute it
        random.shuffle(actions)
        for i in actions:
            i()

    def activity_for_xana_nftduel(self):
        self.set_referer('https://xana.net/nftduel/en/')
        actions = [
            # self.simulate_human_movement,
            self.randomly_scroll,
            self.xana_nftduel_randomly_action,
            self.play_random_video
        ]

        # Randomly choose an action and execute it
        random.shuffle(actions)
        for i in actions:
            i()

    def activity_for_xana_app(self):
        self.set_referer('https://xana.net/app')
        actions = [
            # self.simulate_human_movement,
            self.randomly_scroll,
            self.xana_app_randomly_action,
            self.play_random_video
        ]

        # Randomly choose an action and execute it
        random.shuffle(actions)
        for i in actions:
            i()
        
    def activity_for_xana_blog(self):
        self.set_referer('https://xana.net/blog/')
        actions = [
            # self.simulate_human_movement,
            self.randomly_scroll,
            self.xana_blog_randomly_action,
        ]

        # Randomly choose an action and execute it
        random.shuffle(actions)
        for i in actions:
            self.random_sleep()
            i()
    
    def work(self):
        self.get_driver()
        self.activity_for_xana_app()
        self.close_driver()
        
        
def run_script():
    xana = xana_viewer()
    xana.work()

num_threads = 3


def start_threads():
    active_threads = set()

    from concurrent import futures
    with futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            future = executor.submit(run_script)
            active_threads.add(future)

start_threads()