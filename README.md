
# trading_tools

This is a mix of unreliable and unpredictable tools for trading the markets.

The code was created without testing and was crafted during sleepless nights and mid-day coffee breaks.
Use at your own peril.

I have a plan to move this forward and keep adding features, but please be aware that this is not the best tool in the world.
For this, I agree with the principle 'It works on my machine'. Don't hesitate to use it or send pull requests.

### Prerequisites

You need to install the packages listed in the `requirements.txt` file. Run the following commands:

```bash
pip install -r requirements.txt
pip install "openbb[all]==3.2.4" --no-cache-dir
```
  

### Configuration
Copy the configs_template file and rename it to configs. Then, paste your API keys for the following services:

- Quandl / Nasdaq Datalink: Get your API key here
- Finnhub: Get your API key here
- Financialmodelingprep: Get your API key here
- FRED: Get your API key here
- ALPHAVANTAGE: Get your API key here
- EIA: Get your API key here
  
- Run the main.py file 


### Features

#### Menu Option 1: Charts
This feature allows you to generate various types of charts for trading analysis. You can create trend charts, mean reversion charts, and more.

#### Menu Option 2: Strategies
This feature provides various trading strategies for you to explore. You can analyze the performance of each strategy and choose the one that suits your trading style.

#### Menu Option 3: Reports
This feature generates detailed reports on trading volume, performance, and other key metrics. You can use these reports to make informed trading decisions.

#### Menu Option 4: TradFi
This feature provides tools and analysis for traditional finance (TradFi). You can analyze stocks, bonds, and other traditional financial instruments.

#### Menu Option 5: Crypto
This feature provides tools and analysis for cryptocurrencies. You can analyze the price, volume, and market cap of various cryptocurrencies.


### Images

![Alt text](https://github.com/tiagolvsantos/trading_tools/blob/main/assets/menu.jpg?raw=true)
![Alt text](https://github.com/tiagolvsantos/trading_tools/blob/main/assets/chart_mean_reversions.jpg?raw=true)
![Alt text](https://github.com/tiagolvsantos/trading_tools/blob/main/assets/chart_trend.jpg?raw=true)
![Alt text](https://github.com/tiagolvsantos/trading_tools/blob/main/assets/report_volume.jpg?raw=true)