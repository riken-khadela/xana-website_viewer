from check_windscribe import get_vpn_status, update_in_google_sheet
from ten_min_update_google_sheet import return_df_with_time
from utils import return_google_sheet_df
from views_count import yesterday_views, today_views

gs_df, worksheet = return_google_sheet_df(sheet_name='Website engagement views Sheet')

new_df, pc_name = return_df_with_time(gs_df)
vpn_status = get_vpn_status()


def main():
    if "busy" in  vpn_status:
        new_df.at[1, pc_name] = "VPN busy"
        new_df.at[2, pc_name] = "Not connected"
    elif "DISCONNECTED" in  vpn_status:
        new_df.at[1, pc_name] = "DISCONNECTED"
        new_df.at[2, pc_name] = "Not connected"
    elif vpn_status :
        new_df.at[1, pc_name] = "Connected"
        new_df.at[2, pc_name] = vpn_status
    else :
        new_df.at[1, pc_name] = "Not connected"
        new_df.at[2, pc_name] = "Not connected"
    
    return new_df

new_df = main()





update_in_google_sheet(worksheet,new_df)

