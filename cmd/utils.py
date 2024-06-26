from gspread_dataframe import set_with_dataframe
from datetime import datetime, timedelta
import  pandas as pd, subprocess, gspread, datetime, os


def return_google_sheet_df(sheet_name : str,sheet_index : int = 0):
    """
    sheet_name = 'here will be the name of google sheet like title',
    sheet_index = 'will return the index number of google sheet
    """

    if not sheet_name : 
        raise "please provide a proper sheet"
    
    global sa, sh, worksheet, df
    sa = gspread.service_account()
    sh = sa.open(sheet_name)
    worksheet = sh.get_worksheet(sheet_index)
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df, worksheet

def get_pc_name():
    try:
        result = subprocess.run(['whoami'], capture_output=True, text=True, check=True)
        pc_username = result.stdout.strip()
        if pc_username:
            return pc_username
    except subprocess.CalledProcessError as e:
        return None

        
def create_sh_file(cmd_li : list = []):
    if not cmd_li : return False
    
    sh_path = os.path.join(os.getcwd(),'cmd','cmds.sh')
    # if not os.path.exists(sh_path):
    
    with open(sh_path, 'w') as file: 
        for command in cmd_li: 
            file.write(f"{command}\n")
    
def run_sh_file(sh_path =  os.path.join(os.getcwd(),'cmd','cmds.sh')):
    try:
        result = subprocess.run(['sh', sh_path], check=True, text=True, capture_output=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr
    except FileNotFoundError as e:
        return str(e), None
    
    
    
def create_or_overwrite_sh_file(script_path, commands):
    # Create or overwrite the shell script file
    with open(script_path, 'w') as file:
        # Write the shebang line at the beginning of the file
        file.write("#!/bin/bash\n\n")
        # Write each command in the list to the file
        for command in commands: file.write(f"{command}\n")
    
    # Make the script executable
    os.chmod(script_path, 0o755)

    print(f"Script has been created/recreated at {script_path}")

        
    

# Function to check if the given date string is yesterday's date
def is_date_CONFIRMED(date_string, time_dayss, date_format='%d/%m/%Y'):
    try:
        # Parse the date string into a datetime object
        parsed_date = datetime.datetime.strptime(date_string, date_format).date()
        
        # Get yesterday's date
        yesterday = datetime.datetime.now().date() - timedelta(days=time_dayss)
        
        # Compare the parsed date with yesterday's date
        return parsed_date == yesterday
    except ValueError:
        # Return False if date_string is not a valid date
        return False
    
# # Function to check if the given date string is yesterday's date
# def is_min_old_CONFIRMED(date_string, time_dayss, date_format='%d/%m/%Y'):
#     try:
#         # Parse the date string into a datetime object
#         parsed_date = datetime.datetime.strptime(date_string, date_format).date()
        
#         # Get yesterday's date
#         yesterday = datetime.datetime.now().date() - timedelta(minutes==time_dayss)
        
#         # Compare the parsed date with yesterday's date
#         return parsed_date == yesterday
#     except ValueError:
#         # Return False if date_string is not a valid date
#         return False
    

# def get_this_pc_yesterday_view():
#     """Will return the number of views of yesterday and the name of PCs"""
#     data = get_views_per_day() 
#     for keys, value in data.items() : 
#         if is_date_CONFIRMED(keys, time_dayss = 1) :
#             return value
#     else :
#         return False
    
# def get_this_pc_today_view():
#     """Will return the number of views of yesterday and the name of PCs"""
#     data = get_views_per_day() 
#     for keys, value in data.items() : 
#         if is_date_CONFIRMED(keys,time_dayss = 0) :
#             return value
#     else :
#         return False
    
def update_in_google_sheet(worksheet,gs_df):
    set_with_dataframe(worksheet, gs_df)
    
    
    