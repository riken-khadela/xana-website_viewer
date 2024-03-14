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

def driver_get_xana(driver):
    driver.get('https://xana.net')
    add_data_with_view(datetime.now().strftime("%d/%m/%Y"), True)
    send_final_mail()

def run_some_random_activity(driver):
    print('running some random activities')
    randomnumberrr = 2
    done_activity_nunber = 0
    while randomnumberrr != done_activity_nunber :
        driver.switch_to.window(driver.window_handles[-1])
        aa = driver.find_elements(By.TAG_NAME,'a')
        try :
            for _ in range(random.randint(1,4)):
                aa = driver.find_elements(By.TAG_NAME,'a')
                random.shuffle(aa)
                for a_ele in aa :
                    try:
                        a_ele.click()
                        break
                    except : ...
                if not "xana.net" in driver.current_url :
                    driver.get('https://xana.net')
                
                    
                random_sleep()
            done_activity_nunber += 1
            if done_activity_nunber %2 == 0 : 
                driver.get('https://xana.net/app')
        except : ...
        random_sleep()

def work():
        try:
            logging.info('open selenium driver')
            method = random.randint(1,3)
            # method = 1
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument("--remote-debugging-port=9222")
            if method ==1:
                chrome_options.add_extension(r'./Touch-VPNSecure-and-unlimited-VPN-proxy.crx')
                driver = webdriver.Chrome( options=chrome_options)
                connect_touchvpn(driver)
                driver.get('https://xana.net')

            elif method == 2:
                # chrome_options = webdriver.ChromeOptions()
                chrome_options.add_extension(r'./Turbo-VPNSecure-Free-VPN-Proxy.crx')
                driver = webdriver.Chrome(options=chrome_options)
                connect_turbo(driver)
                driver.get('https://xana.net')
                
            elif method ==3:
                # chrome_options = webdriver.ChromeOptions()
                chrome_options.add_extension(r'./cyberghost.crx')
                driver = webdriver.Chrome(options=chrome_options)
                connect_cyberghost_vpn(driver)
                driver.get('https://xana.net')
                
            elif method == 4:
                """Not working"""
                ...
                # return
                # driver = webdriver.Chrome(options=chrome_options,)
                # driver.get('https://www.blockaway.net/')
                # text_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'url')))
                # text_box.send_keys('https://xana.net/app')
                # text_box.send_keys(Keys.RETURN)
                
            elif method ==5:
                # return
                driver = webdriver.Chrome(options=chrome_options,)
                driver.get('https://www.croxyproxy.net/')
                text_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'url')))
                text_box.send_keys('https://xana.net/app')
                text_box.send_keys(Keys.RETURN)
            
            # driver.execute_script(f"window.open('{random.choice(urls)}')")
            # driver.switch_to.window(driver.window_handles[-1])
            
            windows = driver.window_handles
            for i in windows : 
                driver.switch_to.window(i)
                if 'xana.net' not in driver.current_url : driver.close()
            
            run_some_random_activity(driver)
        except Exception as e: print(e) 
        driver.quit()
    
num_threads = 10
# while True:
#     with ThreadPoolExecutor(max_workers=threads) as executor:
#         futures = [executor.submit(work) for _ in range(threads)]

import concurrent.futures
create_db_ifnot()

def main():
    active_threads = set()

    def start_new_thread():
        while True:
            work()
    
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
