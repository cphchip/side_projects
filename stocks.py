# stocks.py

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

app = Dash()

# Hold list of ticker symbols
portfolio = [
    'AAPL',
    'VOO', 
    'FBTC', 
    'LMT',
    'VXUS'
]

app.layout = html.Div([
    html.Div(children='Stocks'),
    html.Hr(),
    dcc.RadioItems(options=portfolio, value='AAPL', id='controls-and-radio'),
    dcc.Graph(figure={}, id='controls-and-graph')
])


# apple = yf.Ticker("AAPL")
# print(apple.info)  # General information about Apple Inc.

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio', component_property='value')
)
def update_graph(selection):
    days_back = 100
    ticker_data = yf.Ticker(selection)
    ticker_df = ticker_data.history(period="max")  

    if days_back > 0:
        ticker_df = ticker_df.iloc[-days_back:]

    ticker_df['MA50'] = ticker_df['Close'].rolling(window=50).mean()

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
        title=selection
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)



# # Function collects data for each portfoio item and plots it
# def candle(symbols, days_back):
#     # Provide ticker symbols and most recent period using -(days)
#     for ticker in symbols:
#         ticker_data = yf.Ticker(ticker)
#         ticker_df = ticker_data.history(period="max")

#         ticker_df['MA50'] = ticker_df['Close'].rolling(window=50).mean()

#         if days_back > 0:
#             ticker_df = ticker_df.iloc[-days_back:]

#         fig = go.Figure(data=[
#             go.Candlestick(
#                 x=ticker_df.index,
#                 open=ticker_df['Open'],
#                 high=ticker_df['High'],
#                 low=ticker_df['Low'],
#                 close=ticker_df['Close']
#             ),
#             go.Scatter(
#                 x=ticker_df.index,
#                 y=ticker_df['MA50'],
#                 mode='lines',
#                 line=dict(color='blue', width=2),
#                 name='50-day MA'
#             )
#         ])

#         fig.update_layout(
#             title=ticker
#         )

#         fig.show()
    
#     return

# candle(portfolio, 100) # negative plots most recent data

