
# trading_tools

  

This is a mix of unreliable and unpredictable tools for trading the markets.

  

The code was created without testing and was crafted during sleepless nights and mid-day coffee breaks.

  

Use at your own peril.

  
  

I have a plan to move this forward and keep adding features, but please be aware that this is not the best tool in the world.

  

For this, I agree with the principle 'It works on my machine'. Don't hesitate to use it or send pull requests.

  
  

# how to run

- install packages on the requirements.txt

    - pip install -r requirements.txt
    - pip install  "openbb[all]==3.2.4" --no-cache-dir
    
- Copy the configs_template file and rename it to configs, paste the keys:
	- Quandl / Nasdaq Datalink : https://www.nasdaq.com/nasdaq-data-link
	- Finnhub: https://finnhub.io/
	- financialmodelingprep : https://site.financialmodelingprep.com/developer/docs
	- FRED : https://fred.stlouisfed.org/docs/api/fred/
	- ALPHAVANTAGE : https://www.alphavantage.co/support/
	- EIA : https://www.eia.gov/opendata/


  
- Run the main.py file 


# Features
Menu
![Alt text](pics\menu.jpg)

- Charts
![Alt text](pics\chart_trend.jpg)
![Alt text](pics\chart_mean_reversions.jpg)
- Strategies
- Reports
![Alt text](pics\report_volume.jpg)
- TradFi
- Crypto