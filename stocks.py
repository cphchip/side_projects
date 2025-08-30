# stocks.py
# This script uses the Polygon API to fetch stock data and visualize it using Dash and Plotly.
from polygon import RESTClient
from datetime import date, timedelta, datetime
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, Input, Output, callback, dcc, html


client = RESTClient("AgmVIXjnEAmbTzQc6wDT5n4xVoahcn7Z")
app = Dash()

# Hold list of ticker symbols
portfolio = [
    'VXUS', 'VOO', 'AAPL', 'VTWO', 'FBTC' 
]
timespan = [
    50, 100, 200
]


def get_ticker_data(tickers):
    """
    Fetches stock data for the given tickers from the Polygon API.
    Returns a list of DataFrames with the stock data.
    """
    ticker_data_dict = {}
    for item in tickers:
        DAYS_BACK = 750
        ticker_df = pd.DataFrame(
            client.list_aggs(
                ticker=item,
                multiplier=1,
                timespan="day",
                from_=(date.today() - timedelta(days=DAYS_BACK)).strftime("%Y-%m-%d"),
                to=date.today().strftime("%Y-%m-%d"),
                adjusted="true",
                sort="asc",
                # limit=750
            )
        )
        ticker_df['timestamp'] = pd.to_datetime(ticker_df['timestamp'], unit='ms')
        ticker_df['date'] = ticker_df['timestamp'].dt.date
        ticker_df.set_index('date', inplace=True)

        # Calcuate Simple Moving Averages (SMA)
        ticker_df['SMA50'] = ticker_df['close'].rolling(window=50).mean()
        ticker_df['SMA200'] = ticker_df['close'].rolling(window=200).mean()

        # Add the DataFrame to the dictionary with the ticker as the key
        ticker_data_dict.update({item: ticker_df})

    return ticker_data_dict

ticker_data = get_ticker_data(portfolio)

# Setup the Dash app layout
app.layout = html.Div([
    html.Div(children='Stocks'),
    html.Hr(),
    html.Div([
        html.Div([
            html.H3('Ticker'),
            dcc.RadioItems(options=sorted(portfolio), value='AAPL', id='controls-and-radio'),
        ], style={'margin-right': '40px', 'flex': '1'}),
        html.Div([
            html.H3('Timeframe'),
            dcc.RadioItems(options=timespan, value=200, id='timeframe-radio'),
        ], style={'flex': '1'}),
    ], style={'display': 'flex', 'flex-direction': 'row', 'margin-bottom': '30px'}),
    dcc.Graph(figure={}, id='controls-and-graph', style={'height': '900px'}),
])
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio', component_property='value'),
    Input(component_id='timeframe-radio', component_property='value')
)
def update_graph(selection, timespan):
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.8, 0.4],
        vertical_spacing=.2,
        subplot_titles=(f"{selection} Price", "Volume")
    )

    candle_data = ticker_data[selection].iloc[-timespan:] # just plot the last n selected records
    x_dates = candle_data.index

    # Create the candlestick and volume traces
    fig.add_trace(
        go.Candlestick(
            x=x_dates,
            open=candle_data['open'],
            high=candle_data['high'],
            low=candle_data['low'],
            close=candle_data['close'],
            name=f'{selection} OHLC'
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=x_dates,
            y=candle_data['SMA50'],
            mode='lines',
            line=dict(color='blue', width=2),
            name='50-day MA'
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=x_dates,
            y=candle_data['SMA200'],
            mode='lines',
            line=dict(color='orange', width=2),
            name='200-day MA'
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(
            x=x_dates,
            y=candle_data['volume'],
            name='Volume',
            marker_color='rgba(0, 0, 255, 0.5)'
        ),
        row=2, col=1
    )

    # Use date axis and skip weekends (no gaps for non-trading days)
    fig.update_xaxes(
        row=1, col=1,
        rangebreaks=[dict(bounds=["sat", "mon"])]
    )
    fig.update_xaxes(
        row=2, col=1,
        rangebreaks=[dict(bounds=["sat", "mon"])]
    )
    return fig


if __name__ == '__main__':
    app.run(debug=False)