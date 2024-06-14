import pandas as pd, os, datetime
from utils import get_this_pc_yesterday_view, get_this_pc_today_view

csv_path = os.path.join(os.getcwd(),'sheet','views.csv')
if not os.path.exists(csv_path) :
    
    json_data =  {
        "date" : datetime.datetime.today().strftime('%d/%m/%Y'),
        "updated" : datetime.datetime.now(),
        "views" : 0

    }
    df = pd.DataFrame([json_data])
    df.to_csv(csv_path,index=False)
    
# Function to check if the given date string is yesterday's date
def is_min_old_CONFIRMED(date_string, time_minutes, date_format='%d/%m/%Y'):
    from datetime import  timedelta
    
    try:
        # Parse the date string into a datetime object
        parsed_date = datetime.datetime.strptime(date_string, date_format).date()
        
        # Get yesterday's date
        yesterday = datetime.datetime.now().date() - timedelta(minutes=time_minutes)
        
        # Compare the parsed date with yesterday's date
        return parsed_date == yesterday
    
    except ValueError:
        
        # Return False if date_string is not a valid date
        return False


df = pd.read_csv(csv_path)
breakpoint()
df['updated'][0]
parsed_date = df['updated'][0]


# yesterday_views = get_this_pc_yesterday_view()
# today_views = get_this_pc_today_view()


