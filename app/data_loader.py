import yfinance as yf
import pandas as pd

def load_stock_data(ticker: str, period: str = "1y"):
    df = yf.download(ticker, period=period, group_by="ticker")
    df = df[ticker]
    df.reset_index(inplace=True)
    return df
