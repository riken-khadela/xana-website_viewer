import random, time, os
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,NoSuchElementException,WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from dbb import add_data_with_view
from datetime import datetime





class driver_class():
    def __init__(self) -> None:
        
        self.time_running_on_sites = 0
    
    def driver_arguments(self):
        self.base_path = os.getcwd()
        self.download_path = os.path.join(os.getcwd(),'downloads')
        self.options.add_argument('--lang=en')  
        self.options.add_argument("--enable-webgl-draft-extensions")
        self.options.add_argument('--mute-audio')
        self.options.add_argument("--ignore-gpu-blocklist")
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--headless')

        prefs = {"credentials_enable_service": True,
                'profile.default_content_setting_values.automatic_downloads': 1,
                "download.default_directory": "/dev/null",
            'download.prompt_for_download': False, 
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True ,
            "profile.password_manager_enabled": True}
        self.options.add_experimental_option("prefs", prefs)
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')    
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--enable-javascript")
        self.options.add_argument("--enable-popup-blocking")
        self.options.add_argument(f"download.default_directory={self.base_path}/downloads")
        # self.options.add_extension(r'./Touch-VPNSecure-and-unlimited-VPN-proxy.crx')
        # self.options.add_extension(r'./Turbo-VPNSecure-Free-VPN-Proxy.crx')

    def get_driver(self,vpn = False):
        """Start webdriver and return state of it."""
        
        from selenium import webdriver
        for _ in range(30):
            self.options = webdriver.ChromeOptions()
            self.driver_arguments()
            try:
                self.driver = webdriver.Chrome(options=self.options)
                
                if vpn :
                    method = random.randint(1,2)
                    if method ==1:
                        if not self.connect_touchvpn() :
                            self.driver.quit()
                        else : 
                            break

                    elif method == 2:
                        if not self.connect_turbo() :
                            self.driver.quit()
                        else : 
                            break
                    
                break
            except Exception as e:
                print(e)
                
        add_data_with_view(datetime.now().strftime("%d/%m/%Y"), True)
        
        return self.driver

    def connect_touchvpn(self):
        """ Will select any counrty from the following 
            1. US
            2. Canada
            3. Russian Federation
            4. Germany
            5. Netherland (Removed and will not connect now)
            6. UK
        """
        time.sleep(1)
        window_handles = self.driver.window_handles
        time.sleep(1)
        self.driver.switch_to.window(window_handles[0])
        self.driver.get('chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html')
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//*[@class="location"]').click()
        time.sleep(3)
        locations = self.driver.find_element(By.XPATH,'//*[@class="list"]')
        time.sleep(1)
        location = locations.find_elements(By.XPATH,'//*[@class="row"]')
        location = [ i for i in location if not "Netherlands" == i.text]
        location[random.randint(1,7)].click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'//*[@id="ConnectionButton"]').click()
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Stop"]')))
        except Exception as e:
            print(f"Error: {e}")
        connected = self.driver.find_element(By.XPATH,'//*[text()="Stop"]')
        if connected:
            return True
        else:
            return False

    def connect_turbo(self):    
        
        country = ['Singapore','Germany','United Kingdom','United States']
        country = country[random.randint(0,3)]
        time.sleep(1)
        window_handles = self.driver.window_handles
        time.sleep(1)
        self.driver.switch_to.window(window_handles[0])
        time.sleep(1)
        self.driver.get('chrome-extension://bnlofglpdlboacepdieejiecfbfpmhlb/popup/popup.html')
        time.sleep(2)
        location = self.driver.find_element(By.XPATH,'/html/body/div/div/div[4]/div[1]/div[3]')
        if location:
            location.click()
            time.sleep(5)
            searver_list = self.driver.find_element(By.XPATH,'/html/body/div/div/div[3]/div[1]/div[3]/div[2]/div')
            time.sleep(1)
            countrys = searver_list.find_elements(By.XPATH,'.//div')
            countrys[random.randint(0,3)].click()
        
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="CONNECTED"]')))
        except Exception as e:
            self.driver.find_element(By.XPATH,'//*[@class="start-btn"]').click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="CONNECTED"]')))
        connected = self.driver.find_element(By.XPATH,'//*[text()="CONNECTED"]')
        if connected:
            return True
        else:
            return False
        
        
    def find_element(self, element, locator, locator_type=By.XPATH,
            page=None, timeout=10,
            condition_func=EC.presence_of_element_located,
            condition_other_args=tuple()):
        """Find an element, then return it or None.
        If timeout is less than or requal zero, then just find.
        If it is more than zero, then wait for the element present.
        """
        try:
            if timeout > 0:
                wait_obj = WebDriverWait(self.driver, timeout)
                ele = wait_obj.until(EC.presence_of_element_located((locator_type, locator)))
                # ele = wait_obj.until( condition_func((locator_type, locator),*condition_other_args))
            else:
                print(f'Timeout is less or equal zero: {timeout}')
                ele = self.driver.find_element(by=locator_type,
                        value=locator)
            if page:
                print(
                    f'Found the element "{element}" in the page "{page}"')
            else:
                print(f'Found the element: {element}')
            return ele
        except (NoSuchElementException, TimeoutException) as e:
            if page:
                print(f'Cannot find the element "{element}"'
                        f' in the page "{page}"')
            else:
                print(f'Cannot find the element: {element}')
                
    def click_element(self, element, locator, locator_type=By.XPATH,
            timeout=10):
        """Find an element, then click and return it, or return None"""
        ele = self.find_element(element, locator, locator_type, timeout=timeout)
        
        if ele:
            self.driver.execute_script('arguments[0].scrollIntoViewIfNeeded();',ele)
            self.ensure_click(ele)
            print(f'Clicked the element: {element}')
            return ele

    def input_text(self, text, element, locator, locator_type=By.XPATH,
            timeout=10, hide_keyboard=True):
        """Find an element, then input text and return it, or return None"""
        
        ele = self.find_element(element, locator, locator_type=locator_type,
                timeout=timeout)
        
        if ele:
            for i in range(3):
                try: 
                    ele.send_keys(text)
                    print(f'Inputed "{text}" for the element: {element}')
                    return ele    
                except ElementNotInteractableException :...
                
    def ensure_click(self, element, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))
            element.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", element)
            
    def swipe(self,pixel=0): 
        self.driver.execute_script(f"window.scrollTo(0, {pixel});")
            
    def random_sleep(self,a=3,b=7,reson = ""):
        random_time = random.randint(a,b)
        print('time sleep randomly :',random_time) if not reson else print('time sleep randomly :',random_time,f' for {reson}')
        time.sleep(random_time)
        
    def getvalue_byscript(self,script = '',reason=''):
        """made for return value from ele or return ele"""
        if reason :print(f'Script execute for : {reason}')
        else:
            print(f'execute_script : {script}')
        value = self.driver.execute_script(f'return {script}')  
        return value
    
    def CloseDriver(self):
        try: 
            self.driver.quit()
            print('Driver is closed !')
        except Exception as e: ...
        
    def create_or_check_path(self,file_path = '', folder = True):
        if not file_path : return 
        file_path = os.path.join(os.getcwd(),file_path)
        
        if os.path.exists(file_path) : return
        
        if folder :
            os.makedirs(file_path)  
            
            
    def define_action_driver(self):
        self.action = ActionChains(self.driver)
    
    def check_webdriver_element(self,element)    :
        if isinstance(element, WebDriver):
            return True
        return True
    
    def hover_on_an_element(self,element):
        self.define_action_driver()
        if self.check_webdriver_element(element):
            try:
                self.action.move_to_element(element).perform()
                print("Hovered over the element successfully.")
                return True
            except Exception as e:
                print(f"Failed to hover over the element: {e}")
                return False
        else:
            raise ValueError("Argument 'element' must be an instance of WebDriver.")

    
    
    def random_swipe_up(self,SCROLL_PAUSE_TIME=0.5, scroll_count = random.randint(3,7), random_scroll_hight = [400,580] ):
        """Random scrolling top to botton"""
        first_scroll = random.randint(500,780)
        driver = self.driver
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(scroll_count):
            scroll_hight=random.randint(random_scroll_hight[0],random_scroll_hight[1])
            scroll_hight = first_scroll if _ == 0 else scroll_hight
            # Scroll down to bottom
            driver.execute_script(f"window.scrollTo(0, {scroll_hight});")
            scroll_hight += random.randint(random_scroll_hight[0],random_scroll_hight[1])
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
    def random_swipe_down(self, SCROLL_PAUSE_TIME=0.5, scroll_count=random.randint(3, 7), random_scroll_height=[100, 180]):
        """Random scrolling bottom to top"""
        driver = self.driver
        scroll_count = random.randint(3, 7)
        current_height = driver.execute_script("return window.pageYOffset;")
        scroll_height = -random.randint(random_scroll_height[0], random_scroll_height[1])

        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for _ in range(scroll_count):
            scroll_height = last_height - random.randint(random_scroll_height[0], random_scroll_height[1])
            driver.execute_script(f"window.scrollTo(0, {scroll_height});")
            time.sleep(SCROLL_PAUSE_TIME)
            
            new_height = driver.execute_script("return window.pageYOffset;")
            if new_height == current_height:
                break
            current_height = new_height

            if new_height >= last_height:
                break
            last_height = new_height
            
            
            
    def keep_old_site_open(self):
        try :
            self.last_driver_url
            for _ in range(3):
                if not self.last_driver_url == self.driver.current_url :
                    self.driver.back()
                else : break
            else :
                self.driver.get(self.last_driver_url)
        except : ...
            
            
            
            
            
      
        

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' took {elapsed_time:.2f} seconds to execute.")
        return elapsed_time, result
    return wrapper

