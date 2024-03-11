from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,NoSuchElementException,WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver  
import json, random, time, os, shutil
import logging
from selenium import webdriver

class scrapping_bot():
    
    def __init__(self,brazzers_bot = False):
        
        
        self.driver = ''
        self.base_path = os.getcwd()

    def driver_arguments(self):
        ...
        # self.options.add_argument('--lang=en')  
        # self.options.add_argument('--mute-audio') 
        # self.options.add_argument("--enable-webgl-draft-extensions")
        # self.options.add_argument("--ignore-gpu-blocklist")
        # self.options.add_argument('--headless')

        # self.options.add_argument('--no-sandbox')
        # self.options.add_argument('--start-maximized')    
        # self.options.add_argument('--disable-dev-shm-usage')
        # self.options.add_argument("--ignore-certificate-errors")
        # self.options.add_argument("--enable-javascript")
        # self.options.add_argument("--enable-popup-blocking")

    
    def delete_cache_folder(self,folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print("Cache folder deleted successfully.")
        else:
            print("Cache folder not found.")

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
    
    def ScrollDown(self,px):
        self.driver.execute_script(f"window.scrollTo(0, {px})")
    
    def ensure_click(self, element, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))
            element.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", element)
    
    def new_tab(self):
        self.driver.find_element(By.XPATH,'/html/body').send_keys(Keys.CONTROL+'t')

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
    
        
    def click_popup(self, element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", element)
            time.sleep(1)
            element.click()
        except : ...
        
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
            print(f"Error: {e}")
        connected = self.driver.find_element(By.XPATH,'//*[text()="CONNECTED"]')
        if connected:
            return True
        else:
            return False
        
    
    def connect_touchvpn(self):
        self.driver.get('chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html')
        time.sleep(2)
        time.sleep(3)
        country = ['Singapore','Germany','United Kingdom','United States']
        country = random.choice(country)
        time.sleep(1)
        window_handles = self.driver.window_handles
        time.sleep(1)
        self.driver.switch_to.window(window_handles[0])
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//*[@class="location"]').click()
        time.sleep(3)
        locations = self.driver.find_element(By.XPATH,'//*[@class="list"]')
        time.sleep(1)
        location = locations.find_elements(By.XPATH,'//*[@class="row"]')
        location[random.randint(0,7)].click()
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
        
        
    def connect_cyberghost_vpn(self):
        vpn_country_list = ['Romania','Netherlands','United States']
        vpn_country = random.choice(vpn_country_list)
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get('chrome-extension://ffbkglfijbcbgblgflchnbphjdllaogb/index.html')
        time.sleep(3)

        # Disconnect if already connected
        connected_btn = self.driver.find_elements(By.CLASS_NAME, 'dark outer-circle connected')
        time.sleep(1)
        connected_btn[0].click() if connected_btn else None
        time.sleep(2)

        # Select country
        countries_drop_down_btn = self.driver.find_elements(By.TAG_NAME, 'mat-select-trigger')
        time.sleep(1)
        countries_drop_down_btn[0].click() if countries_drop_down_btn else None
        time.sleep(2)
        total_option_country = self.driver.find_elements(By.TAG_NAME, 'mat-option')
        for i in total_option_country:
            i_id = i.get_attribute('id')
            time.sleep(1)
            country_text_ele = i.find_element(By.XPATH, f"//*[@id='{i_id}']/span")
            
            country_text = country_text_ele.text
            time.sleep(1)
            # checking if the country is whether same or not and click on it
            if vpn_country == country_text:
                time.sleep(1)
                print('connected country is :',vpn_country)
                country_text_ele.click()
                break
        time.sleep(3)
        # Checking is the VPN connected or not
        connect_btn = self.driver.find_element(By.XPATH, '//div[@class="dark disconnected outer-circle"]')
        connect_btn.click()
        time.sleep(4)
      
      
    
    def run_some_random_activity(self):
        print('running some random activities')
        try: self.driver.execute_script('document.querySelector("body > div.fade.modal.show").click()')
        except : ...
        randomnumberrr = random.randint(2,7)
        done_activity_nunber = 0
        while randomnumberrr != done_activity_nunber :
            self.driver.switch_to.window(self.driver.window_handles[-1])
            aa = self.driver.find_elements(By.TAG_NAME,'a')
            try :
                for _ in range(random.randint(1,4)):
                    aa = self.driver.find_elements(By.TAG_NAME,'a')
                    random.shuffle(aa)
                    for a_ele in aa :
                        try:
                            a_ele.click()
                            break
                        except : ...
                    if not "xana" in self.driver.current_url :
                        self.driver.get('https://xana.net/app')
                    
                    self.random_sleep()
                        
                done_activity_nunber += 1
                self.random_sleep(20,30)
                if done_activity_nunber %2 == 0 : 
                    self.driver.get('https://xana.net/app')
            except : ...
            self.random_sleep()



    def work(self):
        self.options = webdriver.ChromeOptions()
        
        try:
            logging.info('open selenium driver')
            method = random.randint(1,3)
            method = 1
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--remote-debugging-port=9222")
            if method ==1:
                chrome_options.add_extension(r'./Touch-VPNSecure-and-unlimited-VPN-proxy.crx')
                self.driver = webdriver.Chrome(options=chrome_options)
                self.connect_touchvpn()
                
                self.driver.get('https://xana.net/app')

                
            elif method == 2:
                # chrome_options = webdriver.ChromeOptions()
                chrome_options.add_extension(r'./Turbo-VPNSecure-Free-VPN-Proxy.crx')
                self.driver = webdriver.Chrome(options=chrome_options)
                self.connect_turbo()
                self.driver.get('https://xana.net/app')
                
            elif method ==3:
                # chrome_options = webdriver.ChromeOptions()
                chrome_options.add_extension(r'./cyberghost.crx')
                self.driver = webdriver.Chrome(options=chrome_options)
                self.connect_cyberghost_vpn()
                self.driver.get('https://xana.net/app')
                # driver.get('xana.net')
                
            elif method == 4:
                return
                # self.driver = webdriver.Chrome()
                # driver.get('https://www.blockaway.net/')
                # text_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'url')))
                # text_box.send_keys('https://xana.net/app')
                # text_box.send_keys(Keys.RETURN)
                
            elif method ==5:
                return
                # self.driver = webdriver.Chrome()
                # driver.get('https://www.croxyproxy.net/')
                # text_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'url')))
                # text_box.send_keys('https://xana.net/app')
                # text_box.send_keys(Keys.RETURN)
            
            windows = self.driver.window_handles
            for i in windows : 
                self.driver.switch_to.window(i)
                if 'xana' not in self.driver.current_url : self.driver.close()
            
            for _ in range(random.randint(2,7)):
                self.run_some_random_activity()
        except Exception as e: print(e) 
        self.driver.quit()
        
        
    
num_threads = 10

import concurrent.futures

def main():
    active_threads = set()
    cll = scrapping_bot()
    def start_new_thread():
        while True:
            cll.work()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            future = executor.submit(start_new_thread)
            active_threads.add(future)

        while True:
            completed = concurrent.futures.wait(active_threads, return_when=concurrent.futures.FIRST_COMPLETED).done
            for thread in completed:
                active_threads.remove(thread)
                new_thread = executor.submit(start_new_thread)
                active_threads.add(new_thread)

if __name__ == "__main__":
    main()
