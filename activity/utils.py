
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
    