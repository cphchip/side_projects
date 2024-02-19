import yfinance as yf
import pandas as pd
# import matplotlib.pyplot as plt
import mplfinance as mpf

# Hold list of ticker symbols
portfolio = [
    'VOO', 
    'ARKK', 
    'EZBC', 
    'LMT'
]

# Function collects data for each portfoio item and plots it
def candle(symbols, period):
    for ticker in symbols:
        ticker_data = yf.Ticker(ticker)
        ticker_df = ticker_data.history(period="max")
        mpf.plot(
            ticker_df[period:],
            volume=True,
            style='yahoo',
            type='candle',
            title=ticker,
            mav=(25),
            figratio=(18,10)
        )
    
    return


candle(portfolio, -100) # negative plots most recent data