from curses import window
import random, time
from selenium.common.exceptions import NoSuchAttributeException, NoSuchElementException
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
from dbb import create_db_ifnot,add_data_with_view, get_views_per_day, send_final_mail
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import pickle


with open('proxies.txt', 'r') as file: lines = file.readlines()


def find_element(driver,xpath,locator=By.XPATH,timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        ele = wait.until(EC.presence_of_element_located((locator, xpath)))
        return ele
    except NoSuchElementException:
        pass
    except Exception as e:
        pass

def find_elements(driver, xpath, locator=By.XPATH, timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        elements = wait.until(EC.presence_of_all_elements_located((locator, xpath)))
        return elements
    except NoSuchElementException:
        pass
    except Exception as e:
        pass
    
def click_popup(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", element)
        time.sleep(1)
        element.click()
    except : ...
def click_element(driver,xpath,locator=By.XPATH,timeout=10):
    try:
        element = find_element(driver,xpath,locator,timeout)
        if element.is_displayed():
            element.click()
            return element
        else:
            print("Element is not displayed.")

    except NoSuchElementException:
        pass
    except Exception as e:
        pass
    
def connect_to_cyberghost_vpn(driver):
    country = ['United States','Romania', 'Germany', 'Netherlands' ]
    country = country[random.randint(0,3)]
    driver.get('chrome-extension://ffbkglfijbcbgblgflchnbphjdllaogb/index.html')
    time.sleep(5)
    # Disconnect if already connected
    connected_btn = driver.find_elements(By.CLASS_NAME, 'dark outer-circle connected')
    connected_btn[0].click() if connected_btn else None

    # Select country
    countries_drop_down_btn = driver.find_elements(By.TAG_NAME, 'mat-select-trigger')
    countries_drop_down_btn[0].click() if countries_drop_down_btn else None
    total_option_country = driver.find_elements(By.TAG_NAME, 'mat-option')
    for i in total_option_country:
        i_id = i.get_attribute('id')
        country_text_ele = i.find_element(By.XPATH, f"//*[@id='{i_id}']/span")
        country_text = country_text_ele.text
        if country == country_text:
            country_text_ele.click()
            break
    print(f"VPN connected to {country}")
    time.sleep(2)
    connect_btn = driver.find_elements(By.CLASS_NAME, 'disconnected')
    connect_btn[0].click() if connect_btn else None
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(ec.presence_of_element_located((By.XPATH, '//*[text()="Connected to:"]')))
    except Exception as e:
        print(f"Error: {e}")
    # Checking is the VPN connected or not
    connected_text = driver.find_elements(By.XPATH, '//*[text()="Connected to:"]')
    if connected_text:
        return True
    else:
        return False

def random_sleep(a=3,b=7):
    random_time = random.randint(a,b)
    print('time sleep randomly :',random_time)
    time.sleep(random_time)
def getvalue_byscript(driver,script = '',reason=''):
        """made for return value from ele or return ele"""
        if reason :print(f'Script execute for : {reason}')
        else:
            print(f'execute_script : {script}')
        value = driver.execute_script(f'return {script}')  
        return value
def connect_cyberghost_vpn(driver,vpn_country='Netherlands'):
    try :
        vpn_country_list = ['Romania','Netherlands','United States']
        vpn_country = random.choice(vpn_country_list)
        for  _ in range(3):
            driver.get('chrome-extension://ffbkglfijbcbgblgflchnbphjdllaogb/index.html')
            random_sleep()

            # Disconnect if already connected
            connected_btn = find_element('connected vpn circle','/html/body/app-root/main/app-home/div/div[2]/app-switch/div')
            if connected_btn :
                if not "disconnected" in connected_btn.get_attribute('class') : 
                    click_element('connected vpn circle','/html/body/app-root/main/app-home/div/div[2]/app-switch/div')
                    random_sleep()
                else: 
                    random_sleep(5,10)

            driver.execute_script('document.querySelector("body > app-root > main > app-home > div > div.servers.en > mat-form-field > div > div.mat-form-field-flex.ng-tns-c19-0 > div").click()')
            random_sleep(1,3)
            driver.execute_script(f'document.querySelector("#mat-option-{random.randint(0,3)}").click()')
            random_sleep(1,3)
            driver.execute_script(f'document.querySelector("body > app-root > main > app-home > div > div.spinner > app-switch > div").click()')
            random_sleep(4,10)
            

            # # selecting the country
            # total_option_country = driver.find_elements(By.TAG_NAME, 'mat-option')
            # for i in total_option_country:
            #     i_id = i.get_attribute('id')
            #     country_text_ele = i.find_element(By.XPATH, f"//*[@id='{i_id}']/span")
            #     country_text = country_text_ele.text

            #     # checking if the country is whether same or not and click on it
            #     if vpn_country in country_text:
            #         print('connected country is :',vpn_country)
            #         country_text_ele.click()
                    # break
            # time.sleep(1)
            # Checking is the VPN connected or not
            # connected_btn = getvalue_byscript('document.querySelector("body > app-root > main > app-home > div > div.spinner > app-switch > div").getAttribute("class")')
            # # document.querySelector("body > app-root > main > app-home > div > div.spinner > app-switch > div")
            # if connected_btn :
            #     if not "disconnected" in connected_btn.get_attribute('class') : 
            return
    except : ...
def connect_touchvpn(driver):
    try:
        driver.get('chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html')
        time.sleep(2)
        time.sleep(3)
        country = ['Singapore','Germany','United Kingdom','United States']
        country = random.choice(country)
        time.sleep(1)
        window_handles = driver.window_handles
        time.sleep(1)
        driver.switch_to.window(window_handles[0])
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@class="location"]').click()
        time.sleep(3)
        locations = driver.find_element(By.XPATH,'//*[@class="list"]')
        time.sleep(1)
        location = locations.find_elements(By.XPATH,'//*[@class="row"]')
        location[random.randint(0,7)].click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="ConnectionButton"]').click()
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(ec.presence_of_element_located((By.XPATH, '//*[text()="Stop"]')))
        except Exception as e:
            print(f"Error: {e}")
        connected = driver.find_element(By.XPATH,'//*[text()="Stop"]')
        if connected:
            return True
        else:
            return False
    except : ...
        
def connect_turbo(driver):    
    try :
        country = ['Singapore','Germany','United Kingdom','United States']
        country = country[random.randint(0,3)]
        time.sleep(1)
        window_handles = driver.window_handles
        time.sleep(1)
        driver.switch_to.window(window_handles[0])
        time.sleep(1)
        driver.get('chrome-extension://bnlofglpdlboacepdieejiecfbfpmhlb/popup/popup.html')
        time.sleep(2)
        location = driver.find_element(By.XPATH,'/html/body/div/div/div[4]/div[1]/div[3]')
        if location:
            location.click()
            time.sleep(5)
            searver_list = driver.find_element(By.XPATH,'/html/body/div/div/div[3]/div[1]/div[3]/div[2]/div')
            time.sleep(1)
            countrys = searver_list.find_elements(By.XPATH,'.//div')
            countrys[random.randint(0,3)].click()
                    
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(ec.presence_of_element_located((By.XPATH, '//*[text()="CONNECTED"]')))
        except Exception as e:
            driver.find_element(By.XPATH,'//*[@class="start-btn"]').click()
            wait.until(ec.presence_of_element_located((By.XPATH, '//*[text()="CONNECTED"]')))
            print(f"Error: {e}")
        connected = driver.find_element(By.XPATH,'//*[text()="CONNECTED"]')
        if connected:
            return True
        else:
            return False
    except :...
    
    
def connect_surf(driver):
    driver.get('chrome-extension://ailoabdmgclmfmhdagmlohpjlbpffblp/index.html')
    time.sleep(3)
    quick=driver.find_elements(By.XPATH, "//button[contains(text(), 'Quick-connect')]")
    disconnect_btn=driver.find_elements(By.XPATH, "//button[contains(text(), 'Disconnect')]")
    check=quick or disconnect_btn
    if check:
        driver.get('chrome-extension://ailoabdmgclmfmhdagmlohpjlbpffblp/index.html')
        time.sleep(4)
        continue_btn=driver.find_elements(By.XPATH, "//button[contains(text(), 'Continue')]")
        if continue_btn:continue_btn[0].click()
        time.sleep(4)
        disconnect_btn=driver.find_elements(By.XPATH, "//button[contains(text(), 'Disconnect')]")
        if disconnect_btn:disconnect_btn[0].click()
        time.sleep(4)
        all=driver.find_elements(By.CLASS_NAME,"SnNof")
        # breakpoint()
        if all:all[random.randint(0,len(all))].click()
        time.sleep(4)
    else:
        driver.get('https://my.surfshark.com/home/dashboard')
        with open('./surf.pkl', 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
        driver.get('chrome-extension://ailoabdmgclmfmhdagmlohpjlbpffblp/index.html')
        time.sleep(4)
        continue_btn=driver.find_elements(By.XPATH, "//button[contains(text(), 'Continue')]")
        if continue_btn:continue_btn[0].click()
        time.sleep(4)
        disconnect_btn=driver.find_elements(By.XPATH, "//button[contains(text(), 'Disconnect')]")
        if disconnect_btn:disconnect_btn[0].click()
        time.sleep(4)
        all=driver.find_elements(By.CLASS_NAME,"SnNof")
        # breakpoint()
        if all:all[random.randint(0,len(all))].click()
        time.sleep(4)  

def driver_get_xana(driver,link):
    driver.get('https://xana.net')
    add_data_with_view(datetime.now().strftime("%d/%m/%Y"), True)
    send_final_mail()
    
    windows = driver.window_handles
    for i in windows : 
        driver.switch_to.window(i)
        if 'xana.net' not in driver.current_url : driver.close()

def run_some_random_activity(driver,link,engagement=False):
    print('running some random activities')
    randomnumberrr = 1
    done_activity_nunber = 0
    while randomnumberrr != done_activity_nunber :
        driver.switch_to.window(driver.window_handles[-1])
        aa = driver.find_elements(By.TAG_NAME,'a')
        try :
            for _ in range(random.randint(1,4)):
                if engagement:
                    aa = driver.find_elements(By.TAG_NAME,'a')
                    random.shuffle(aa)
                    for a_ele in aa :
                        try:
                            a_ele.click()
                            break
                        except : ...
                    if not link in driver.current_url :
                        driver_get_xana(driver,link)
                random_sleep()
                actions = ActionChains(driver)
                element_to_scroll_to = driver.find_element(By.TAG_NAME,'footer')
                actions.move_to_element(element_to_scroll_to).perform()
                
                random_sleep(1,4)
                elements_to_scroll_to = driver.find_elements(By.TAG_NAME,'section')
                actions.move_to_element(random.choice(elements_to_scroll_to)).perform()
                
                
                random_sleep()
            done_activity_nunber += 1
            if done_activity_nunber %2 == 0 : 
                driver_get_xana(driver,link)
        except : ...
        random_sleep()

def connect_surf(driver):
    driver.get('chrome-extension://ailoabdmgclmfmhdagmlohpjlbpffblp/index.html')
    time.sleep(3)
    quick=driver.find_elements(By.XPATH, "//button[contains(text(), 'Quick-connect')]")
    disconnect_btn=driver.find_elements(By.XPATH, "//button[contains(text(), 'Disconnect')]")
    check=quick or disconnect_btn
    if check:
        driver.get('chrome-extension://ailoabdmgclmfmhdagmlohpjlbpffblp/index.html')
        time.sleep(4)
        continue_btn=driver.find_elements(By.XPATH, "//button[contains(text(), 'Continue')]")
        if continue_btn:continue_btn[0].click()
        time.sleep(4)
        disconnect_btn=driver.find_elements(By.XPATH, "//button[contains(text(), 'Disconnect')]")
        if disconnect_btn:disconnect_btn[0].click()
        time.sleep(4)
        all=driver.find_elements(By.CLASS_NAME,"SnNof")
        # breakpoint()
        if all:all[random.randint(0,len(all))].click()
        time.sleep(4)
    else:
        driver.get('https://my.surfshark.com/home/dashboard')
        with open('./surf.pkl', 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
        driver.get('chrome-extension://ailoabdmgclmfmhdagmlohpjlbpffblp/index.html')
        time.sleep(4)
        continue_btn=driver.find_elements(By.XPATH, "//button[contains(text(), 'Continue')]")
        if continue_btn:continue_btn[0].click()
        time.sleep(4)
        disconnect_btn=driver.find_elements(By.XPATH, "//button[contains(text(), 'Disconnect')]")
        if disconnect_btn:disconnect_btn[0].click()
        time.sleep(4)
        all=driver.find_elements(By.CLASS_NAME,"SnNof")
        # breakpoint()
        if all:all[random.randint(0,len(all))].click()
        time.sleep(4)  

def work(prx):
        try:
            logging.info('open selenium driver')
            from seleniumwire import webdriver
            proxy_options = {
                'proxy': {
                    'https': prx.replace('\n',''),
                }
            }
            chrome_options = webdriver.ChromeOptions()
            prefs = {"credentials_enable_service": True,
                'profile.default_content_setting_values.automatic_downloads': 1,
                "download.default_directory" : f"{check_Downloads_folder()}",
            'download.prompt_for_download': False, 
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True ,
            "profile.password_manager_enabled": True}
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument('--lang=en')  
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--mute-audio') 
            chrome_options.add_argument("--enable-webgl-draft-extensions")
            chrome_options.add_argument("--ignore-gpu-blocklist")
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--enable-javascript")
            chrome_options.add_argument("--enable-popup-blocking")
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_argument('--remote-debugging-pipe')
            chrome_options.add_argument('--disable-dev-shm-usage')
            # chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(seleniumwire_options=proxy_options, options=chrome_options)
            driver.get("https://xana.net/nftduel/en/")
            # element_to_scroll_to = driver.find_element(By.TAG_NAME,'footer')
            windows = driver.window_handles
            for i in windows : 
                driver.switch_to.window(i)
                if 'xana.net' not in driver.current_url : driver.close()
            
            run_some_random_activity(driver,link="xana.net/nftduel/en/")
            driver.get("https://xana.net/")
            run_some_random_activity(driver,link="xana.net",engagement=True)
        except Exception as e: print(e) 
        driver.quit()
    
# while True:
#     with ThreadPoolExecutor(max_workers=threads) as executor:
#         futures = [executor.submit(work) for _ in range(threads)]

def check_Downloads_folder():
    import os, shutil
    dwn_path = os.path.join(os.getcwd(),'Downloads')
    if not os.path.exists(dwn_path) :
        os.mkdir(dwn_path)
    else :
        shutil.rmtree(dwn_path)
        os.mkdir(dwn_path)
    return dwn_path

def get_random_prx():
    global lines
    if not lines : 
        with open('proxies.txt', 'r') as file: lines = file.readlines()
        
    if lines :
        return random.choice(lines)
    else :
        with open('proxies.txt', 'r') as file: lines = file.readlines()
        return random.choice(lines)


import concurrent.futures
create_db_ifnot()


num_threads = 1

def main():
    active_threads = set()

    def start_new_thread():
        while True:
            work(get_random_prx())
    
    # Start the initial threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            future = executor.submit(start_new_thread)
            active_threads.add(future)

        # Monitor and replace completed threads
        while True:
            completed = concurrent.futures.wait(active_threads, return_when=concurrent.futures.FIRST_COMPLETED).done
            for thread in completed:
                active_threads.remove(thread)
                new_thread = executor.submit(start_new_thread)
                active_threads.add(new_thread)

if __name__ == "__main__":
    from dbb import create_db_ifnot
    create_db_ifnot()
    main()
