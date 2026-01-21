import yfinance as yf
from .models import Price
from datetime import date

def fetch_latest_price(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")

    if data.empty:
        return None

    close_price = data["Close"].iloc[-1]

    # save to price model
    price = Price.objects.create(
            symbol = symbol,
            date = date.today(),
            close = close_price
            )

    return price
