
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
![Alt text](https://github.com/tiagolvsantos/trading_tools/blob/main/pics/menu.jpg?raw=true)

- Charts
![Alt text](https://github.com/tiagolvsantos/trading_tools/blob/main/pics/chart_trend.jpg?raw=true)
![Alt text](https://github.com/tiagolvsantos/trading_tools/blob/main/pics/chart_mean_reversions.jpg?raw=true)
- Strategies
- Reports
![Alt text](https://github.com/tiagolvsantos/trading_tools/blob/main/pics/report_volume.jpg?raw=true)
- TradFi
- Crypto