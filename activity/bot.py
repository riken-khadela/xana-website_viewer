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
    
    def switch_to_tab(self, window_name:str):
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
            if direction == "down":
                self.driver.execute_script("window.scrollBy(0, window.innerHeight/4);")
            else:
                self.driver.execute_script("window.scrollBy(0, -window.innerHeight/4);")
            time.sleep(random.uniform(0.5, 1.5))  # Random sleep to mimic human behavior
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
        
        

def get_cmd_output(command : str = ''):
    try:
        output = subprocess.check_output(
            f'''google-chrome --version''',
            shell=True
        ).decode()
        
        return output.replace('\n','').strip()
                    
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")
    return None
    

def get_google_chrome_version():
    output = get_cmd_output(f'''google-chrome --version''')
    return output.replace('Google Chrome ','').split('.')[0]
    

# Function to check if GA tracking code is present
def check_ga_loaded(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//script[contains(@src, 'googletagmanager.com/gtag/js') or contains(@src, 'google-analytics.com/analytics.js')]"))
        )
        print("GA tracking code found.")
        return True
    except TimeoutException:
        print("GA tracking code not found.")
        return False
    
    

def find_on_google():
    driver.get('https://www.google.com/')
    
    

    
def find_on_insta():
    old_windows = driver.window_handles
    
    driver.get('https://www.instagram.com/xanametaverse/')
    time.sleep(10)
    a_tag = driver.find_elements(By.XPATH,"//*[contains(text(), 'linktr.ee/xanametaverse')]")
    if a_tag :
        suppoter.ensure_click(a_tag[0])
    else : return
    
    new_windows = driver.window_handles
    for new_win in new_windows : 
        if new_win  in old_windows :
            driver.switch_to.window(new_win)
            driver.close()

    
    driver.switch_to.window(driver.window_handles[-1])
    website_tag = driver.find_elements(By.XPATH,"//a[contains(@href, 'https://xana.net/?utm_source=linktree')]")
    suppoter.scroll_smoothly(max_scroll=2)
    if not website_tag  : return
    
    website_tag = website_tag[-1]
    time.sleep(random.uniform(0.5, 1.5))
    suppoter.ensure_click(website_tag)
    

def nevigate_to_website():
    
    
    
    ...

    
    
def click_on_stite():
    find_on_insta()

    
# Function to perform random scrolling and clicking
def random_browsing():
    while True:

        try:
            global driver
            global suppoter
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
            
            driver = uc.Chrome(options=options, version_main=int(get_google_chrome_version()))
            suppoter = WebDriverUtility(driver=driver)
            click_on_stite()
            driver.get("https://xana.net/")
            add_data_with_view(datetime.datetime.now().strftime("%d/%m/%Y"), True)
            
            # Ensure the page is fully loaded
            time.sleep(5)
            if not check_ga_loaded(driver):
                driver.quit()
                break
            end_time = time.time() + 1 * 60  # 1 minute from now
            while time.time() < end_time:
                # Random scroll
                scroll_height = driver.execute_script("return document.body.scrollHeight")
                random_scroll = random.randint(0, scroll_height)
                driver.execute_script(f"window.scrollTo(0, {random_scroll});")
                # Random click
                elements = driver.find_elements(By.XPATH, "//*")
                if elements:
                    element_to_click = random.choice(elements)
                    try:
                        ActionChains(driver).move_to_element(element_to_click).click().perform()
                    except WebDriverException:
                        pass
                # Wait for a short random interval
                time.sleep(random.uniform(0.5, 2))
            driver.quit()
            break  # Exit the loop if browsing completes successfully
        except (TimeoutException, WebDriverException) as e:
            print(f"An error occurred: {e}. Retrying...")
            if 'driver' in locals():
                driver.quit()
# Function to run browsing in threads

num_threads = 1


def start_threads():
    active_threads = set()

    from concurrent import futures
    with futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            future = executor.submit(random_browsing)
            active_threads.add(future)
            

# while True:
#     start_threads()
#     time.sleep(1)  # Wait a short while before starting again
    
    
    
class xana_viewer(WebDriverUtility):
    
    def __init__(self) -> None:
        ...
    
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

    
    def get_google_chrome_version(self):
        output = get_cmd_output(f'''google-chrome --version''')
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

    
    def by_insta(self):
        self.get_driver()
        self.navigate_to('https://www.instagram.com/xanametaverse/')
        old_windows = self.driver.current_window_handle
        self.random_sleep()
        a_tag = driver.find_elements(By.XPATH,"//*[contains(text(), 'linktr.ee/xanametaverse')]")
        if a_tag :
            self.ensure_click(a_tag[0])
        else : return
        
        self.switch_to_tab(old_windows)
        self.driver.close()
        
        self.switch_to_tab(self.driver.window_handles[-1])
        website_tag = driver.find_elements(By.XPATH,"//a[contains(@href, 'https://xana.net/?utm_source=linktree')]")
        self.scroll_smoothly(max_scroll=2)
        if not website_tag  : return
        
        website_tag = website_tag[-1]
        time.sleep(random.uniform(0.5, 1.5))
        self.ensure_click(website_tag)
        add_data_with_view(datetime.datetime.now().strftime("%d/%m/%Y"), True)
        
        
        if not self.check_ga_loaded():
            driver.quit()
            return
        
        self.random_activity()
        self.close_driver()
        
    def by_google(self):
        
        
        ...