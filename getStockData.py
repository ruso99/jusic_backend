import requests
from bs4 import BeautifulSoup
import traceback
import pandas as pd
import datetime
import ast


#basic정보페이지를 파싱
def parse_page(code, page):
    try:
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'.format(code=code, page=page)
        res = requests.get(url)
        _soap = BeautifulSoup(res.text, 'lxml')
        _df = pd.read_html(str(_soap.find("table")), header=0)[0]  # 리스트에 [0]붙여서 dataframe 만들기
        _df = _df.dropna()  # NaN값 제거
        del _df['전일비']
        return _df
    except Exception as e:
        traceback.print_exc()
        return None

#foregin정보페이지를 파싱
def parse_pageForeign(code, page):
    url = 'https://finance.naver.com/item/frgn.nhn?code={code}&page={page}'.format(code=code, page=page)
    html = requests.get(url)
    table = pd.read_html(html.text)

    Foreigndf = table[2].dropna()
    Foreigndf.drop(['종가', '전일비', '등락률', '거래량'], axis='columns', inplace=True)
    Foreigndf.columns = ['날짜', '기관순매매량', '외국인순매매량', '보유주수', '외국인보유율']
    del Foreigndf['외국인보유율']
    return Foreigndf

#환율정보페이지 파싱
def parse_pageER(code,page):
    try:
        url = 'https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd={code}&page={page}'.format(code=code, page=page)
        res = requests.get(url)
        _soap = BeautifulSoup(res.text, 'lxml')
        _df = pd.read_html(str(_soap.find("table")), header=0)[0] #리스트에 [0]붙여서 dataframe 만들기
        _df = _df.dropna() #NaN값 제거
        _df.drop(['전일대비', '현찰', '현찰.1', '송금', '송금.1', 'T/C 사실때', '외화수표 파실 때'], axis='columns', inplace=True)
        _df = _df.drop(0, 0)
        return _df
    except Exception as e:
        traceback.print_exc()
        return None


# 증시정보페이지 파싱(해외)
def parse_pageWorld(code, page):
    try:
        pd.set_option('mode.chained_assignment', None)

        url = 'https://finance.naver.com/world/worldDayListJson.nhn?symbol={code}&fdtc=0&page={page}'.format(code=code,
                                                                                                             page=page)
        res = requests.get(url)

        _soap = BeautifulSoup(res.text, 'lxml').text
        # data = _soap.find('p')
        # df = pd.DataFrame.from_dict(_soap)
        x = ast.literal_eval(_soap)
        df = pd.DataFrame(x)
        df.drop(['symb', 'rate', 'gvol'], axis='columns', inplace=True)
        df.columns = ['날짜', '시가', '고가', '저가', '종가', '전일대비']

        for i in range(0, len(df['날짜'])):
            s = df['날짜'][i]
            obj = datetime.datetime.strptime(s, '%Y%m%d')
            string = obj.strftime('%Y.%m.%d')
            df['날짜'][i] = string

        return df
    except Exception as e:
        traceback.print_exc()
        return None

#증시정보페이지 파싱(국내)
def parse_pageKorea(code, page):
    try:
        url = 'https://finance.naver.com/sise/sise_index_day.nhn?code={code}&page={page}'.format(code=code, page=page)
        res = requests.get(url)
        _soap = BeautifulSoup(res.text, 'lxml')
        _df = pd.read_html(str(_soap.find("table", summary="일별 시세표:날짜에 따른 체결가 전일비 등락률 거래량 거래대금 정보를 제공합니다.")), header=0)[
            0]  # 리스트에 [0]붙여서 dataframe 만들기
        _df = _df.dropna()  # NaN값 제거
        _df.columns = ['날짜', '체결가', '전일비', '등락률', '거래량(천주)', '거래대금(백만)']

        return _df
    except Exception as e:
        traceback.print_exc()
        return None


#basic정보 크롤링
def getBasicData(code, toYear, toMonth, toDay):
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    res = requests.get(url)
    res.encoding = 'utf-8'
    soap = BeautifulSoup(res.text,'lxml')

    # page_navigation 마지막 번호(pg_last)
    el_table_navi = soap.find("table", class_="Nnavi")
    el_td_last = el_table_navi.find("td", class_="pgRR")
    pg_last = el_td_last.a.get('href').rsplit('&')[1]
    pg_last = pg_last.split('=')[1]
    pg_last = int(pg_last)

    str_datefrom = datetime.datetime.strftime(datetime.datetime(year=toYear, month=toMonth, day=toDay), '%Y.%m.%d')
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
    df = df.reset_index(drop=True)
    return df

#투자자별 매매동향 정보 크롤링
def getForeignerData(code, toYear, toMonth, toDay, agencyNetsales, foreignerNetsales, foreignerSharesheld):
    url = 'https://finance.naver.com/item/frgn.nhn?code={code}'.format(code=code)
    res = requests.get(url)
    res.encoding = 'utf-8'

    soap = BeautifulSoup(res.text, 'lxml')

    # page_navigation 마지막 번호(pg_last)
    el_table_navi = soap.find("table", align="center")
    el_td_last = el_table_navi.find_all("td", class_="pgRR")
    pg_last = int(el_td_last[0].a.get('href')[-3:])

    str_datefrom = datetime.datetime.strftime(datetime.datetime(year=toYear, month=toMonth, day=toDay), '%Y.%m.%d')
    str_dateto = datetime.datetime.strftime(datetime.datetime.today(), '%Y.%m.%d')

    df = None

    for page in range(1, pg_last + 1):
        _df = parse_pageForeign(code, page)

        try:
            _df_filtered = _df[_df["날짜"] > str_datefrom]

            if df is None:
                df = _df_filtered
            else:
                df = pd.concat([df, _df_filtered])
            if len(_df) > len(_df_filtered):
                break
        except:
            return 0

    df = df.reset_index(drop=True)

    if (agencyNetsales == False):
        del df['기관순매매량']

    if (foreignerNetsales == False):
        del df['외국인순매매량']

    if (foreignerSharesheld == False):
        del df['보유주수']

    return df

#환율 정보 크롤링
def getERData(ERcode,toYear, toMonth, toDay):
    code = ERcode
    nowDate = datetime.datetime.today()
    toDate = datetime.datetime(toYear,toMonth,toDay)
    pg_last = (((nowDate - toDate).days)//10)

    str_datefrom = datetime.datetime.strftime(datetime.datetime(year=toYear, month=toMonth, day=toDay), '%Y.%m.%d')
    str_dateto = datetime.datetime.strftime(datetime.datetime.today(), '%Y.%m.%d')

    df = None
    for page in range(1, pg_last + 1):
        _df = parse_pageER(code, page)
        _df_filtered = _df[_df['날짜'] > str_datefrom]

        if df is None:
            df = _df_filtered
        else:
            df = pd.concat([df, _df_filtered])
        if len(_df) > len(_df_filtered):
            break

    df = df.reset_index(drop=True)
    return df

#증시 정보 크롤링(해외)
def getWorldData(code, toYear, toMonth, toDay):
    nowDate = datetime.datetime.today()
    toDate = datetime.datetime(toYear, toMonth, toDay)
    pg_last = (((nowDate - toDate).days) // 10)

    str_datefrom = datetime.datetime.strftime(datetime.datetime(year=toYear, month=toMonth, day=toDay), '%Y.%m.%d')
    str_dateto = datetime.datetime.strftime(datetime.datetime.today(), '%Y.%m.%d')

    df = None
    for page in range(1, pg_last + 1):
        _df = parse_pageWorld(code, page)
        _df_filtered = _df[_df['날짜'] > str_datefrom]

        if df is None:
            df = _df_filtered
        else:
            df = pd.concat([df, _df_filtered])
        if len(_df) > len(_df_filtered):
            break
    df = df.reset_index(drop=True)
    return df

#증시 정보 크롤링(국내)
def getKoreaData(code, toYear, toMonth, toDay):
    url = 'https://finance.naver.com/sise/sise_index_day.nhn?code={code}'.format(code=code)
    res = requests.get(url)
    res.encoding = 'utf-8'
    soap = BeautifulSoup(res.text,'lxml')

    # page_navigation 마지막 번호(pg_last)
    el_table_navi = soap.find("table", class_="Nnavi")
    el_td_last = el_table_navi.find("td", class_="pgRR")
    pg_last = el_td_last.a.get('href').rsplit('&')[1]
    pg_last = pg_last.split('=')[1]
    pg_last = int(pg_last)


    str_datefrom = datetime.datetime.strftime(datetime.datetime(year=toYear, month=toMonth, day=toDay), '%Y.%m.%d')
    str_dateto = datetime.datetime.strftime(datetime.datetime.today(), '%Y.%m.%d')

    df = None
    for page in range(1, pg_last + 1):
        _df = parse_pageKorea(code, page)
        _df_filtered = _df[_df['날짜'] > str_datefrom]

        if df is None:
            df = _df_filtered
        else:
            df = pd.concat([df, _df_filtered])
        if len(_df) > len(_df_filtered):
            break
    df = df.reset_index(drop=True)
    return df
