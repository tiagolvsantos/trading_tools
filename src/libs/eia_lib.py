import pandas as pd
import os
from configs import EIA


# load key to environment
os.environ['EIA_KEY'] = EIA
from dotenv import load_dotenv
load_dotenv()


# import eia package
from eiapy import Series
from eiapy import Category

# https://www.eia.gov/petroleum/supply/weekly/
# https://pypi.org/project/eiapy/

def get_spr():
    df_data = pd.read_excel("https://www.eia.gov/dnav/pet/xls/PET_SUM_SNDW_A_EPC0_SAS_MBBL_W.xls", sheet_name="Data 1", skiprows=2)
    return df_data if len(df_data) >0 else pd.pd.DataFrame()


def us_pretroleum_balance_sheet():
    df_data = pd.read_excel("https://ir.eia.gov/wpsr/psw01.xls", sheet_name="Data 1", skiprows=2)
    return df_data if len(df_data) >0 else pd.pd.DataFrame()




#cal_to_mex = Series('EBA.CISO-CFE.ID.H')

#gulf_category = Category(296728).get_info()