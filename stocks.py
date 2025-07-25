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
    'AAPL', 'VOO', 'FBTC', 'LMT', 'VXUS'
]

app.layout = html.Div([
    html.Div(children='Stocks'),
    html.Hr(),
    dcc.RadioItems(options=portfolio, value='AAPL', id='controls-and-radio'),
    dcc.Graph(figure={}, id='controls-and-graph',style={'height': '900px'}
    )   
])

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio', component_property='value')
)
def update_graph(selection):
    days_back = 100
    ticker_df = pd.DataFrame(
        client.list_aggs(
            selection,
            1,
            "day",
            (date.today() - timedelta(days=days_back)).strftime("%Y-%m-%d"),
            date.today().strftime("%Y-%m-%d"),
            adjusted="true",
            sort="asc",
            limit=120
        )
    )
    ticker_df['timestamp'] = pd.to_datetime(ticker_df['timestamp'], unit='ms')
    ticker_df.set_index('timestamp', inplace=True)

    ticker_df['MA50'] = ticker_df['close'].rolling(window=50).mean()

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.8, 0.4],
        vertical_spacing=0.1,
        subplot_titles=(f"{selection} Price", "Volume")
    )

    x_dates = ticker_df.index.strftime('%Y-%m-%d')

    fig.add_trace(
        go.Candlestick(
            x=x_dates,
            open=ticker_df['open'],
            high=ticker_df['high'],
            low=ticker_df['low'],
            close=ticker_df['close'],
            name='Candlestick'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=x_dates,
            y=ticker_df['MA50'],
            mode='lines',
            line=dict(color='blue', width=2),
            name='50-day MA'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(
            x=x_dates,
            y=ticker_df['volume'],
            name='Volume',
            marker_color='rgba(0, 0, 255, 0.5)'
        ),
        row=2, col=1
    )

    fig.update_xaxes(
        row=1, col=1,
        type='category',
        rangebreaks=[dict(bounds=["sat", "mon"])]
    )
    fig.update_xaxes(
        row=2, col=1,
        type='category',
        rangebreaks=[dict(bounds=["sat", "mon"])]
    )
    # print(datetime.fromtimestamp(ticker_df.iloc[-1].timestamp / 1000))

    return fig

if __name__ == '__main__':
    app.run(debug=True)