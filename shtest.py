import selenium, datetime

# # Append-adds at last
# print('fffffffff')
# file1 = open("myfile.txt", "a")  # append mode
# file1.write(f"Today : {datetime.datetime.now()} \n")
# file1.close()

import time
import subprocess

# The time you want to run the script (12:30 AM)
desired_time = "10:45"

while True:
    current_time = time.strftime("%H:%M")
    breakpoint()
    # if current_time == desired_time:
    subprocess.call(["/home/dell/workspace2/website_viewer/env/bin/python3", "/home/dell/workspace2/website_viewer/shtest2.py"])
    
    # Sleep for a while to avoid excessive checking
    print(1111)
    # time.sleep(30)
