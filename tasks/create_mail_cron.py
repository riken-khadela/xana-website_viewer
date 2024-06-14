import os
from crontab import CronTab
import argparse

def create_reboot_cronjob(script_filename, delay_minutes=5):
    # Get the absolute path of the script file
    script_path = os.path.abspath(script_filename)

    # Initialize CronTab
    cron = CronTab(user=True)

    # Create a new cron job
    job = cron.new(command=f'sleep {delay_minutes * 60} && python3 {script_path}')

    # Set the job to run at reboot
    job.setall('@reboot')

    # Write the cron job to the user's crontab
    cron.write()

    print(f'Cron job created to run {script_filename} after {delay_minutes} minutes on reboot.')

# Example usage
if __name__ == "__main__":
    create_reboot_cronjob('mail.py', delay_minutes=5)
