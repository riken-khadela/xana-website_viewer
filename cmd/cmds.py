import pandas as pd
from utils import *



gs_df, worksheet = return_google_sheet_df("xana sheet commands")
pcname = get_pc_name()

def check_cmds_pcname():
    if pcname not in gs_df.columns :
        gs_df[pcname] = pd.NaT
    update_in_google_sheet(worksheet,gs_df)
check_cmds_pcname()

gs_df, worksheet = return_google_sheet_df("xana sheet commands")


create_sh_file(gs_df[pcname].to_list())
print(run_sh_file())
values_to_remove = gs_df[pcname].to_list()
gs_df = gs_df[~gs_df[pcname].isin(values_to_remove)]
update_in_google_sheet(worksheet,gs_df)

