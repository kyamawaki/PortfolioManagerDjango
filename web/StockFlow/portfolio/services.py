import requests
import logging
import os
from datetime import date

logger = logging.getLogger(__name__)

##############################################################
# 最新の値（１日前の終値を取得する）
##############################################################
def fetch_latest_price(ticker):
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
