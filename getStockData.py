import requests
from bs4 import BeautifulSoup
import traceback
import pandas as pd
import datetime

#basic정보페이지를 파싱
def parse_page(code, page):
    try:
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'.format(code=code, page=page)
        res = requests.get(url)
        _soap = BeautifulSoup(res.text, 'lxml')
        _df = pd.read_html(str(_soap.find("table")), header=0)[0] #리스트에 [0]붙여서 dataframe 만들기
        _df = _df.dropna() #NaN값 제거
        return _df
    except Exception as e:
        traceback.print_exc()
    return None

#foregin정보페이지를 파싱
def parse_pageForeign(code, page):
    try:
        url = 'https://finance.naver.com/item/frgn.nhn?code={code}&page={page}'.format(code=code, page=page)
        res = requests.get(url)
        _soap = BeautifulSoup(res.text, 'lxml')
        _df = pd.read_html(str(_soap.find("table", summary="외국인 기관 순매매 거래량에 관한표이며 날짜별로 정보를 제공합니다.")), header=0)[0] #리스트에 [0]붙여서 dataframe 만들기
        _df = _df.dropna() #NaN값 제거
        return _df
    except Exception as e:
        traceback.print_exc()
    return None

#basic정보 크롤링
def getBasicData(code, startYear, startMonth, startDay):
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    res = requests.get(url)
    res.encoding = 'utf-8'

    soap = BeautifulSoup(res.tex,'lxml')

    # page_navigation 마지막 번호(pg_last)
    el_table_navi = soap.find("table", class_="Nnavi")
    el_td_last = el_table_navi.find("td", class_="pgRR")
    pg_last = el_td_last.a.get('href').rsplit('&')[1]
    pg_last = pg_last.split('=')[1]
    pg_last = int(pg_last)

    str_datefrom = datetime.datetime.strftime(datetime.datetime(year=startYear, month=startMonth, day=startDay), '%Y.%m.%d')
    str_dateto = datetime.datetime.strftime(datetime.datetime.today(), '%Y.%m.%d')

    df = None

    for page in range(1, pg_last + 1):
        _df = parse_page(code, page)
        _df_filtered = _df[_df['날짜'] > str_datefrom]

        if df is None:
            df = _df_filtered
        else:
            df = pd.concat([df, _df_filtered])
        if len(_df) > len(_df_filtered):
            break

    return df

#투자자별 매매동향 정보 크롤링
def getForeignerData(code,startYear,startMonth,startDay,agencyNetsales,foreignerNetsales,foreignerSharesheld):
    url = 'https://finance.naver.com/item/frgn.nhn?code={code}'.format(code=code)
    res = requests.get(url)
    res.encoding = 'utf-8'

    soap = BeautifulSoup(res.text, 'lxml')

    # page_navigation 마지막 번호(pg_last)
    el_table_navi = soap.find("table", align="center")
    el_td_last = el_table_navi.find_all("td", class_="pgRR")
    pg_last = int(el_td_last[0].a.get('href')[-3:])

    str_datefrom = datetime.datetime.strftime(datetime.datetime(year=startYear, month=startMonth, day=startDay), '%Y.%m.%d')
    str_dateto = datetime.datetime.strftime(datetime.datetime.today(), '%Y.%m.%d')

    df = None

    for page in range(1, pg_last + 1):
        _df = parse_page(code, page)
        _df_filtered = _df[_df['날짜'> str_datefrom]

        if df is None:
            df = _df_filtered
        else:
            df = pd.concat([df, _df_filtered])
        if len(_df) > len(_df_filtered):
            break

    return df




