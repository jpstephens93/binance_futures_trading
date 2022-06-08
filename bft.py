from binance.client import Client
import pandas as pd

user_key = "****************************"
secret_key = "****************************"

binance_client = Client(user_key, secret_key)

# MARKET DATA
# current futures price
binance_client.futures_symbol_ticker()

# OHLCV historical
df = pd.DataFrame(binance_client.futures_historical_klines(
    symbol='BTCUSDT',
    interval='1d',  # can play with this e.g. '1h', '4h', '1w', etc.
    start_str='2021-01-01',
    end_str='2021-06-01'
))

# crop unnecessary columns
df = df.iloc[:, :6]

# ascribe names to columns
df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

# convert timestamp to date format and ensure ohlcv are all numeric
df['date'] = pd.to_datetime(df['date'], unit='ms')
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col])

print(df)

# TRADING
# test order
binance_client.create_test_order(
    symbol='BTCUSDT',
    type='MARKET',
    side='BUY',
    quantity=0.001
)

# order book - into a pandas DataFrame for neater output
df = pd.DataFrame(
    binance_client.futures_order_book(symbol='BTCUSDT')
)
print(df[['bids', 'asks']].head())

# set leverage - IMPORTANT
binance_client.futures_change_leverage(symbol='BTCUSDT', leverage=1)

# limit order
binance_client.futures_create_order(
    symbol='BTCUSDT',
    type='LIMIT',
    timeInForce='GTC',  # Can be changed - see link to API doc below
    price=30000,  # The price at which you wish to buy/sell, float
    side='BUY',  # Direction ('BUY' / 'SELL'), string
    quantity=0.001  # Number of coins you wish to buy / sell, float
)

# market order
binance_client.futures_create_order(
    symbol='BTCUSDT',
    type='MARKET',
    timeInForce='GTC',
    side='BUY',
    quantity=0.001
)

# view outstanding orders
binance_client.futures_get_open_orders(symbol='BTCUSDT')
