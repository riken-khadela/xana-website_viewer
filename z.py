import concurrent.futures
import random
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

# Function to perform actions within a browser window
def perform_actions(driver, thread_id):
    print(f"Thread {thread_id} is starting.")
    
    try:
        if random.choice([True, False]):
            driver.get('https://www.google.com')


            time.sleep(200)
            # Add your actions here

        # Example: Click an element
        # element = find_element(driver, 'your_xpath')
        # if element:
        #     element.click()
        
        # Add more actions as needed

    except NoSuchElementException as e:
        print(f"Thread {thread_id}: Element not found - {e}")
    except TimeoutException as e:
        print(f"Thread {thread_id}: Timeout waiting for element - {e}")
    except Exception as e:
        print(f"Thread {thread_id}: An error occurred - {e}")

    print(f"Thread {thread_id} is completed.")
    driver.quit()

# Function to find an element with a timeout
def find_element(driver, xpath, timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(lambda d: d.find_element(By.XPATH, xpath))
        return element
    except TimeoutException:
        return None

# Number of threads to run concurrently
num_threads = 10

# Create a thread pool executor
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    for thread_id in range(1, num_threads + 1):
        # You can use different WebDriver options here if needed
        driver_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=driver_options)
        executor.submit(perform_actions, driver, thread_id)
