import yfinance as yf
from .models import Price
from datetime import date

def fetch_latest_price(symbol):
    # get ticker object
    ticker = yf.Ticker(symbol)
    # get stock price data for the most recent day
    data = ticker.history(period="1d")

    if data.empty:
        return None

    # close_price is "owari-ne" in Japanese
    # data is in Pandas DataFrame format. (like the table below)
        # Date           Open   High    Low   Close   Volume
        # 2024-01-10     150.0  152.0  149.5  151.2   1000000
        # 2024-01-11     151.0  153.0  150.0  152.5   1200000
        # 2024-01-12     152.0  154.0  151.0  153.8   1100000
    # iloc[-1] gets latest Close value.
    close_price = data["Close"].iloc[-1]

    # save to price model
    price = Price.objects.create(
            symbol = symbol,
            date = date.today(),
            close = close_price
            )

    return price

##############################################################
# 最新の値（１日前の終値を取得する）
##############################################################
def fetch_latest_price(ticker):
    data = yf.Ticker(ticker).history(period="1d")
    if data.empty:
        return None
    return data["Close"].iloc[-1]

