import yfinance as yf
from datetime import date

##############################################################
# 最新の値（１日前の終値を取得する）
##############################################################
def fetch_latest_price(ticker):
    data = yf.Ticker(ticker).history(period="1d")
    if data.empty:
        return None
    return data["Close"].iloc[-1]

##############################################################
# 最新のドル円レート（１日前の終値を取得する）
##############################################################
def fetch_usd_jpy():
    data = yf.Ticker("USDJPY=X").history(period="1d")
    if data.empty:
        return None
    return data["Close"].iloc[-1]
