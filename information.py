import requests
import pandas_datareader.data as web
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def get_datas(codes):
    stcodes = ['{}.JP'.format(code) for code in codes[:10]]
    print(stcodes)
    datas = web.DataReader(stcodes, 'stooq')
    print(datas)
    return web.DataReader(stcodes, 'stooq')["Close"][-200:]

def get_moving_average(data):
    # 25日平均線
    series1 = data["Close"].rolling(window=25).mean().values
    # 75日平均線
    series2 = data["Close"].rolling(window=75).mean().values
    # 200日平均線
    series3 = data["Close"].rolling(window=200).mean().values
    return series1, series2, series3

def golden_crossover(series1: pd.Series, series2: pd.Series, series3: pd.Series) -> bool:
    """
    ゴールデンクロスが起きたらTrueを返す
    """
    if(series1.size < 2):
        return False
    try:
        return (series1[0] < series2[0] and series1[1] > series2[1]) or \
                    (series2[0] < series3[0] and series2[1] > series3[1]) or \
                        (series1[0] < series3[0] and series1[1] > series3[1])
    except IndexError:
        return False

def dead_crossover(series1: pd.Series, series2: pd.Series, series3: pd.Series) -> bool:
    """
    デッドクロスが起きたらTrueを返す
    """
    if(series1.size < 2):
        return False
    try:
        return (series1[0] > series2[0] and series1[1] < series2[1]) or \
                    (series2[0] > series3[0] and series2[1] < series3[1]) or \
                        (series1[0] > series3[0] and series1[1] < series3[1])
    except IndexError:
        return False

def get_fundametals(code):
    """
    Get Market capitalization, PER, PBR, ROE
    """
    load_url = "https://stocks.finance.yahoo.co.jp/stocks/detail/?code={}".format(code)
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")
    company_name = soup.find(class_="symbol").text
    return company_name, [element.text for element in soup.find_all(class_="tseDtl")][3:-1]