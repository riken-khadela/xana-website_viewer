import threading
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from dbb import add_data_with_view
import datetime


import subprocess

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
# Function to perform random scrolling and clicking
def random_browsing():
    while True:
        add_data_with_view(datetime.datetime.now().strftime("%d/%m/%Y"), True)

        try:
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
            driver.get("https://xana.net/")
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
def start_threads():
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=random_browsing)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
        
# Main loop to repeat the process
while True:
    start_threads()
    time.sleep(1)  # Wait a short while before starting again