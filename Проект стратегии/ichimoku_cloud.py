import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Read BTC/USD data
df = yf.Ticker('BTC-USD').history(period='1y')[['Close', 'Open', 'High', 'Volume', 'Low']]
d = df['Close'].ewm(span=26, adjust=False, min_periods=26).mean()

# Define length of Tenkan Sen or Conversion Line
cl_period = 20

# Define length of Kijun Sen or Base Line
bl_period = 60

# Define length of Senkou Sen B or Leading Span B
lead_span_b_period = 120

# Define length of Chikou Span or Lagging Span
lag_span_period = 30

# Calculate conversion line
high_20 = df['High'].rolling(cl_period).max()
low_20 = df['Low'].rolling(cl_period).min()
df['conversion_line'] = (high_20 + low_20) / 2

# Calculate based line
high_60 = df['High'].rolling(bl_period).max()
low_60 = df['Low'].rolling(bl_period).min()
df['base_line'] = (high_60 + low_60) / 2

# Calculate leading span A
df['lead_span_A'] = ((df.conversion_line + df.base_line) / 2).shift(lag_span_period)

# Calculate leading span B
high_120 = df['High'].rolling(120).max()
low_120 = df['High'].rolling(120).min()
df['lead_span_B'] = ((high_120 + low_120) / 2).shift(lead_span_b_period)

# Calculate lagging span
df['lagging_span'] = df['Close'].shift(-lag_span_period)

# Drop NA values from Dataframe
# df.dropna(inplace=True)

# Add figure and axis objects
fig, ax = plt.subplots(1, 1, sharex=True, figsize=(20, 10))
ax.plot(d)

ax.plot(df['Close'])
ax.plot(df['lead_span_A'])
ax.plot(df['lead_span_B'])

# Use the fill_between of ax object to specify where to fill
ax.fill_between(df.index, df['lead_span_A'], df['lead_span_B'],
                where=df['lead_span_A'] >= df['lead_span_B'], color='lightgreen')

ax.fill_between(df.index, df['lead_span_A'], df['lead_span_B'],
                where=df['lead_span_A'] < df['lead_span_B'], color='lightcoral')
plt.legend()
plt.grid()
plt.show()
