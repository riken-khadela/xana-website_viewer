import random, time
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.service import Service
from selenium import webdriver


def connect_to_cyberghost_vpn(driver):
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    # countrys = ['United States','Romania', 'Germany', 'Netherlands' ]
    countrys = ['United States','Romania', 'Netherlands' ]
    country = countrys[random.randint(0,3)]
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
    error = find_element(driver,'//*[text()="connectPage.error"]')
    if error:
        return False
    # while error:
    #     country = countrys[random.randint(0,3)]
    #     countries_drop_down_btn = driver.find_elements(By.TAG_NAME, 'mat-select-trigger')
    #     countries_drop_down_btn[0].click() if countries_drop_down_btn else None
    #     total_option_country = driver.find_elements(By.TAG_NAME, 'mat-option')
    #     for i in total_option_country:
    #         i_id = i.get_attribute('id')
    #         country_text_ele = i.find_element(By.XPATH, f"//*[@id='{i_id}']/span")
    #         country_text = country_text_ele.text
    #         if country == country_text:
    #             country_text_ele.click()
    #     time.sleep(2)
    #     connect_btn = driver.find_elements(By.CLASS_NAME, 'disconnected')
    #     connect_btn[0].click() if connect_btn else None
    #     error = find_element(driver,'//*[text()="connectPage.error"]')
        
    connected_text = driver.find_elements(By.XPATH, '//*[text()="Connected to:"]')
    if connected_text:
        time.sleep(30)
        disconnect = find_element(driver,'//*[@class="dark outer-circle connected"]')
        disconnect.click()
        return True

    
def connect_touchvpn(driver):
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    driver.get('chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html')
    time.sleep(2)
    time.sleep(3)
    country = ['Singapore','Germany','United Kingdom','United States']
    country = random.choice(country)
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@class="location"]').click()
    time.sleep(3)
    locations = find_element(driver,'//*[@class="list"]')
    time.sleep(1)
    location = find_elements(locations,'//*[@class="row"]')
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
        time.sleep(20)
        connected.click()
        return True
    else:
        return False
        
def connect_turbo(driver):  
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])  
    country = ['Singapore','Germany','United Kingdom','United States']
    country = country[random.randint(0,3)]
    # time.sleep(1)
    # window_handles = driver.window_handles
    # time.sleep(1)
    # driver.switch_to.window(window_handles[0])
    time.sleep(1)
    driver.get('chrome-extension://bnlofglpdlboacepdieejiecfbfpmhlb/popup/popup.html')
    time.sleep(2)
    location = find_element(driver,'/html/body/div/div/div[4]/div[1]/div[3]')
    if location:
        location.click()
        time.sleep(5)
        searver_list = find_element(driver,'/html/body/div/div/div[3]/div[1]/div[3]/div[2]/div')
        time.sleep(1)
        countrys = find_elements(searver_list,'.//div')
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
    driver.execute_script(
        "arguments[0].scrollIntoViewIfNeeded();", element)
    time.sleep(1)
    element.click()

def play_all_frame(driver):
    iframes = find_elements(driver,'iframe', By.TAG_NAME)
    for i in iframes:
        driver.switch_to.frame(i)
        try:
            driver.find_element(By.CSS_SELECTOR, '[title^="Pause (k)"]')
        except WebDriverException:
            try:
                driver.find_element(
                    By.CSS_SELECTOR, 'button.ytp-large-play-button.ytp-button').send_keys(Keys.ENTER)
            except WebDriverException:
                try:
                    driver.find_element(
                        By.CSS_SELECTOR, '[title^="Play (k)"]').click()
                except WebDriverException:
                    try:
                        driver.execute_script(
                            "document.querySelector('button.ytp-play-button.ytp-button').click()")
                    except WebDriverException:
                        pass
        driver.switch_to.default_content()
        time.sleep(2)

options = webdriver.ChromeOptions()
options.add_argument('--mute-audio')
options.add_extension(r'./Touch-VPNSecure-and-unlimited-VPN-proxy.crx')
options.add_extension(r'./Turbo-VPNSecure-Free-VPN-Proxy.crx')
options.add_extension(r'./cyberghost.crx')
driver = webdriver.Chrome(options=options)
driver.get('https://youtube-views.ytpremium35.repl.co/')
text_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'urlvideo')))
text_box.clear()
text_box.send_keys('https://www.youtube.com/watch?v=g4FUGtd1piY&ab_channel=armordriller')
views = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'nbrvideo')))
views.clear()
views.send_keys('5')
play_btn =  find_element(driver,'//button[@onclick="play();"]')
play_btn.click()
time.sleep(10)
play_all_frame(driver)
while True:
    for i in range(2):
        if i == 0:
            connect_to_cyberghost_vpn(driver)
        elif i ==1:
            connect_touchvpn(driver)
        else:
            connect_turbo(driver)
        time.sleep(30)
            
breakpoint()


