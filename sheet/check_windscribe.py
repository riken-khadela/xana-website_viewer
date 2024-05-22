from utils import *

def get_vpn_status():
    try:
        result = subprocess.run(['windscribe','status'], capture_output=True, text=True, check=True)
        windscribe_status = result.stdout.strip()
        if windscribe_status:
            if "busy" in windscribe_status.lower() : 
                return "busy"
            
            if "DISCONNECTED" in windscribe_status :
                return "DISCONNECTED"
                
            elif ' -- ' in windscribe_status :
                country = windscribe_status.split(' -- ')[-1]
                return country
                
            return False
    except subprocess.CalledProcessError as e:
        return False
    
# get_vpn_status()