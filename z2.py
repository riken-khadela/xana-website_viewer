import time
import subprocess

# The time you want to run the script (12:30 AM)
desired_time = "00:30"

while True:
    current_time = time.strftime("%H:%M")
    
    if current_time == desired_time:
        subprocess.call(["/home/dell/workspace2/website_viewer/env/bin/python3", "/home/dell/workspace2/website_viewer/shtest.py"])
    
    # Sleep for a while to avoid excessive checking
    time.sleep(60)
