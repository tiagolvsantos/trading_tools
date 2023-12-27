from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=0) 

def get_keywords_trend(keywords_list: list):
    pytrends.build_payload(keywords_list, cat=0, timeframe='today 5-y')
    pytrends.
    df_data = pytrends.interest_over_time() 
    df_data = df_data.reset_index()
    return df_data