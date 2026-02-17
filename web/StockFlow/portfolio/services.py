import requests
import logging
import os
from datetime import date
import yfinance as yf
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

##############################################################
# 最新の値（１日前の終値を取得する）
##############################################################
def fetch_latest_price(asset_class, ticker):
    if asset_class in ("US_STOCK", "US_BOND"):
        return _fetch_latest_price_us(ticker)
    else:
        return _fetch_latest_price_jp(ticker)
    
##############################################################
# 米国株最新の値（１日前の終値を取得する）
##############################################################
def _fetch_latest_price_us(ticker):
    API_KEY = os.getenv("FINNHUB_API_KEY")
    url =  f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={API_KEY}"
    try:
        logger.info(f"[fetch_stock_price] ticker={ticker}")
        data = requests.get(url, timeout=5).json()
        if data is None:
            return None
        
        logger.info(f"[fetched_stock_price]")
        return data["c"]

    except Exception as e:
        logger.exception(f"[fetch_stock_price] ERROR ticker={ticker}")
        return None
    
##############################################################
# 日本株最新の値（１日前の終値を取得する）
##############################################################
def _fetch_latest_price_jp(ticker):
    url = f"https://finance.yahoo.co.jp/quote/{ticker}"
    logger.info(f"[fetch_latest_price_p] ticker={ticker}")
    html = requests.get(url).text
    logger.info(f"[fetched_fund_price]")
    soup = BeautifulSoup(html, "html.parser")

    # 基準価額のセレクタ（2025年時点）
    price_tag = soup.select_one("span._3rXWJKZF")
    if price_tag:
        return price_tag.text.replace(",", "")
    return None
##############################################################
# 最新のドル円レート（１日前の終値を取得する）
##############################################################
def fetch_usd_jpy():
    try:
        logger = logging.getLogger(__name__)
        url = "https://api.frankfurter.app/latest?base=USD&symbols=JPY"
        logger.info(f"[fetch_exchange_rate]")
        data = requests.get(url, timeout=5).json()
        if data is None:
            return None
    
        logger.info(f"[fetched_exchange_rate]")
        return data["rates"]["JPY"]

    except Exception as e:
        logger.exception(f"[fetch_exchange_rate] ERROR")
        return None

