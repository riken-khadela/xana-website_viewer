import  pandas as pd, subprocess, gspread, datetime
from gs_dbb import get_views_per_day
from datetime import datetime, timedelta
from gspread_dataframe import set_with_dataframe
from utils import *
import datetime



def return_df_with_time(gs_df):
    """This function will return the dataframe of yesterday views and edited to the sheet"""
    pc_name = get_pc_name()
    if pc_name :
        new_data = {
                pc_name : datetime.datetime.now()
            }
        if pc_name not in gs_df.columns:
            gs_df[pc_name] = pd.NaT
            
        gs_df.at[0, pc_name] = new_data[pc_name]
        return gs_df, pc_name
    

# new_df = return_df_with_time()
# update_in_google_sheet(worksheet,new_df)

