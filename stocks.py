# stocks.py

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


# apple = yf.Ticker("AAPL")
# print(apple.info)  # General information about Apple Inc.

# Hold list of ticker symbols
portfolio = [
    # 'AAPL'
    'VOO', 
    'FBTC', 
    'LMT',
    'VXUS'
]

# Function collects data for each portfoio item and plots it
def candle(symbols, days_back):
    # Provide ticker symbols and most recent period using -(days)
    for ticker in symbols:
        ticker_data = yf.Ticker(ticker)
        ticker_df = ticker_data.history(period="max")

        ticker_df['MA50'] = ticker_df['Close'].rolling(window=50).mean()

        if days_back > 0:
            ticker_df = ticker_df.iloc[-days_back:]

        fig = go.Figure(data=[
            go.Candlestick(
                x=ticker_df.index,
                open=ticker_df['Open'],
                high=ticker_df['High'],
                low=ticker_df['Low'],
                close=ticker_df['Close']
            ),
            go.Scatter(
                x=ticker_df.index,
                y=ticker_df['MA50'],
                mode='lines',
                line=dict(color='blue', width=2),
                name='50-day MA'
            )
        ])

        fig.update_layout(
            title=ticker
        )

        fig.show()
    
    return

candle(portfolio, 100) # negative plots most recent data

