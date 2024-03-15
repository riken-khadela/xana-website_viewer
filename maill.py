import os
import signal
import smtplib
import subprocess
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.utils import formatdate
import pytz

SENDER_PASSWORD='hfac mvld ecjx clru'
receiver_mail="rikenkhadelamain@gmail.com"
sender_mail='rikenkhadela777@gmail.com'

class SendErrorMail:
    def __init__(self): ...

    def send_email(self, subject, system_no, body):
        add_line = ''
        if not system_no:
            try:
                result = subprocess.run(['whoami'], capture_output=True, text=True, check=True)
                pc_username = result.stdout.strip()
                if pc_username:
                    add_line += f"This is PC's username: {pc_username}\n"
            except subprocess.CalledProcessError as e:
                add_line += f"Failed to get username: {e}\n"

            anydesk_id = self.get_anydesk_id()
            if anydesk_id:
                add_line += f"This is AnyDesk ID: {anydesk_id}\nSYSTEM_NO not set in this PC.\n"

        sender_email = sender_mail
        sender_password = SENDER_PASSWORD
        receiver_email = receiver_mail

        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z%z')

        body = body + f"\n\n{add_line}\nCurrent IST Time: {current_time}----------------------"

        message = MIMEText(body)
        message["Subject"] = f'PC number: {system_no}, "{subject}"'
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Date"] = formatdate(localtime=True)

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
        except Exception as e:
            print(f"Failed to send email: {e}")
        else:
            print("Email sent successfully.")

    def get_anydesk_id(self):
        anydesk_id = ''
        try:
            anydesk_process = subprocess.Popen(['anydesk'])
            time.sleep(5)  # Adjust the sleep time as needed
            result = subprocess.run(['anydesk', '--get-id'], capture_output=True, text=True, check=True)
            anydesk_id = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Failed to get AnyDesk ID: {e}")
        finally:
            if anydesk_process:
                os.kill(anydesk_process.pid, signal.SIGTERM)
        return anydesk_id if anydesk_id and 'SERVICE_NOT_RUNNING' not in anydesk_id else None


# SendErrorMail(subject="test webview",body="this is a body of vebwiew")