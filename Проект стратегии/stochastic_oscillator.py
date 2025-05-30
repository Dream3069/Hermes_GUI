import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def calculate_stochastic_oscillator(data, k_period=14, d_period=3):
    data['low_min'] = data['Low'].rolling(window=k_period).min()
    data['high_max'] = data['High'].rolling(window=k_period).max()

    data['%K'] = 100 * ((data['Close'] - data['low_min']) / (data['high_max'] - data['low_min']))
    data['%D'] = data['%K'].rolling(window=d_period).mean()
    return data


df = yf.Ticker('BTC-USD').history(period='1d', interval='5m')[['Close', 'Open', 'High', 'Volume', 'Low']]
data = calculate_stochastic_oscillator(df)
df['%K'] = data[['%K']]
df['%D'] = data[['%D']]

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option("display.max_columns", None)
print(df)


def paint():
    # Avoid case-sensitive issues for accessing data.
    # Optional if using pandas_ta
    df.columns = [x.lower() for x in df.columns]
    # Create our primary chart
    # the rows/cols arguments tell plotly we want two figures
    fig = make_subplots(rows=2, cols=1)
    # Create our Candlestick chart with an overlaid price line
    fig.append_trace(
        go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            increasing_line_color='#ff9900',
            decreasing_line_color='black',
            showlegend=False
        ), row=1, col=1  # <------------ upper chart
    )
    # price Line
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['open'],
            line=dict(color='#ff9900', width=1),
            name='open',
        ), row=1, col=1  # <------------ upper chart
    )
    # Fast Signal (%k)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['%k'],
            line=dict(color='#ff9900', width=2),
            name='fast',
        ), row=2, col=1  #  <------------ lower chart
    )
    # Slow signal (%d)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['%d'],
            line=dict(color='#000000', width=2),
            name='slow'
        ), row=2, col=1 # <------------ lower chart
    )
    # Extend our y-axis a bit
    fig.update_yaxes(range=[-10, 110], row=2, col=1)
    # Add upper/lower bounds
    fig.add_hline(y=0, col=1, row=2, line_color="#666", line_width=2)
    fig.add_hline(y=100, col=1, row=2, line_color="#666", line_width=2)
    # Add overbought/oversold
    fig.add_hline(y=20, col=1, row=2, line_color='#336699', line_width=2, line_dash='dash')
    fig.add_hline(y=80, col=1, row=2, line_color='#336699', line_width=2, line_dash='dash')
    # Make it pretty
    layout = go.Layout(
        plot_bgcolor='#efefef',
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )
    fig.update_layout(layout)
    # View our chart in the system default HTML viewer (Chrome, Firefox, etc.)
    fig.show()


paint()

