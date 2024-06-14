import pytz, time, os, signal
from datetime import datetime
import subprocess
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib

sender_email = SENDER_MAIL='rikenkhadela777@gmail.com'
sender_password = SENDER_PASSWORD='mced jhzv vxoj xixm'
receiver_email = RECEIVER_MAIL="rikenkhadela22@gmail.com"
system_no = SYSTEM_NO='RK'

def restart_anydesk_id():
    import subprocess

    # Command to restart AnyDesk with sudo
    command = ""
    # Ask for the sudo password
    password = "1234"
    # Execute the command with sudo and provide the password
    completed_process = subprocess.run(
        command,
        input=password,
        shell=True,
        text=True,
        check=True,
        capture_output=True
    )
    # Check the output for any errors
    if completed_process.returncode == 0:
        print("AnyDesk restarted successfully.")
    else:
        password = "0000"
    # Execute the command with sudo and provide the password
        completed_process = subprocess.run(
            command,
            input=password,
            shell=True,
            text=True,
            check=True,
            capture_output=True
        )
        if completed_process.returncode == 0:
            print("AnyDesk restarted successfully.")
        else :
            print("Error:", completed_process.stderr)

def get_anydesk_id():
        restart_anydesk_id()
        anydesk_id = ''
        try:
            anydesk_process = subprocess.Popen(['anydesk'])
            time.sleep(5)  # Adjust the sleep time as needed
            # subprocess.run(["sudo","-S", "systemctl","restart", "anydesk"], input="0000",capture_output=True, text=True, check=True)
            result = subprocess.run(['anydesk', '--get-id'], capture_output=True, text=True, check=True)
            anydesk_id = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Failed to get AnyDesk ID: {e}")
        finally:
            if anydesk_process:
                os.kill(anydesk_process.pid, signal.SIGTERM)
        return anydesk_id if anydesk_id and 'SERVICE_NOT_RUNNING' not in anydesk_id else None
    
body = ''
add_line = ''
if not system_no:
    try:
        result = subprocess.run(['whoami'], capture_output=True, text=True, check=True)
        pc_username = result.stdout.strip()
        if pc_username:
            add_line += f"This is PC's username: {pc_username}\n"
    except subprocess.CalledProcessError as e:
        add_line += f"Failed to get username: {e}\n"


ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z%z')

body = body + f"\n\n{add_line}\nCurrent IST Time: {current_time}"
subject = "test emails"
anydesk_id = ''
try :
    anydesk_id = get_anydesk_id()
except : ...
print(anydesk_id,'-------------')

try:
    result = subprocess.run(['whoami'], capture_output=True, text=True, check=True)
    pc_username = result.stdout.strip()
    if pc_username:
        body += f"\nThis is PC's username: {pc_username}\n"
except subprocess.CalledProcessError as e:
    body += f"\nFailed to get username: {e}\n"
    
if anydesk_id:
    if not pc_username :
        body += f"\n\n\nThis is AnyDesk ID: {anydesk_id}\nSYSTEM_NO not set in this PC.\n"
    else :
        body += f"\n\n\nThis is AnyDesk ID: {anydesk_id}\nSYSTEM_NO not set in this PC.\n"
        
    
message = MIMEText(body)
message["Subject"] = f'PC number: {system_no} {subject} from xana web views'
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