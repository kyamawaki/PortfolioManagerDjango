import requests
import logging
import os
from datetime import date
import yfinance as yf
from bs4 import BeautifulSoup
from portfolio.models import Asset

logger = logging.getLogger(__name__)

##############################################################
# 最新の値
##############################################################
def fetch_latest_price(asset):
    if asset.is_usstock_asset:
        return fetch_latest_price_us(asset)
    elif asset.is_usbnd_asset:
        return fetch_latest_price_usbnd(asset)
    elif asset.is_usmmf_asset:
        return fetch_latest_price_usmmf(asset)
    elif asset.is_uscash_asset:
        return fetch_latest_price_uscash(asset)
    elif asset.is_jpstock_asset:
        return fetch_latest_price_jp(asset)
    else:
        return fetch_latest_price_jp_fund(asset)
    
##############################################################
# 米国株最新の値（１日前の終値を取得する）
##############################################################
def fetch_latest_price_us(asset):
    ticker = asset.ticker
    API_KEY = os.getenv("FINNHUB_API_KEY")
    url =  f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={API_KEY}"
    try:
        logger.info(f"[fetch_stock_price] ticker={ticker}")
        data = requests.get(url, timeout=5).json()
        logger.info(f"[fetched_stock_price]")
        if data is None:
            return None
        
        price = data["c"]
        logger.info(f"ticker={ticker} price={price}")
        return price

    except Exception as e:
        logger.exception(f"[fetch_stock_price] ERROR ticker={ticker}")
        return None
    
##############################################################
# 米国債権の値
##############################################################
def fetch_latest_price_usbnd(asset):
    return asset.quantity
    
##############################################################
# 米国MMFの値
##############################################################
def fetch_latest_price_usmmf(asset):
    return fetch_usd_jpy()
    
##############################################################
# 米国CASHの値
##############################################################
def fetch_latest_price_uscash(asset):
    return fetch_usd_jpy()
    
##############################################################
# 日本株最新の値
##############################################################
def fetch_latest_price_jp(asset):
    ticker = asset.ticker
    url = f"https://finance.yahoo.co.jp/quote/{ticker}"
    logger.info(f"[fetch_latest_price_jp] ticker={ticker}")
    html = requests.get(url).text
    logger.info(f"[fetched_latest_price_jp]")
    soup = BeautifulSoup(html, "html.parser")

    # 基準価額のセレクタ
    price_tag = soup.select_one("span.StyledNumber__value__3rXW")
    #price_tag = soup.select_one("span._3rXWJKZF")
    if price_tag:
        price = price_tag.text.replace(",", "")
        logger.info(f"ticker={ticker} price={price}")
        return price
    
    return None

##############################################################
# 投資信託最新の値
##############################################################
def fetch_latest_price_jp_fund(asset):
    return fetch_latest_price_jp(asset)

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

