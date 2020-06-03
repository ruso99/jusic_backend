#-*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template
import json
import getStockData
import pymysql
import pandas as pd


app = Flask(__name__)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def getStockCode():
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
        df = pd.read_html(url, header=0)[0]
        df = df[['회사명','종목코드']]
        df = df.rename(columns={'회사명':'name','종목코드':'code'})
        df['code'] = df['code'].astype(str)
        df['code'] = df['code'].str.zfill(6)

        return df


=======
>>>>>>> parent of c436714... [ADD]getCompanyList() 추가
=======
>>>>>>> parent of c436714... [ADD]getCompanyList() 추가
=======
>>>>>>> parent of c436714... [ADD]getCompanyList() 추가
@app.route('/get/result', methods=['POST'])
def getResult():
    #받아오는 데이터
    data = request.get_json()

    #여기서 작업
    #여기서 딥러닝 작업
    result = Deeplearning.run(data)


    #프론트에 보낼 데이터(넘겨야할 데이터를 여기에 담으면 됨, 무조건 딕셔너리 형태로 담아야함)
    res = { "result" : "성공" }

    #결과를 DB에 저장

    return json.dumps(res,ensure_ascii=False)

#페이지 첫 로드시에 가져오는 데이터
@app.route('/get/company/list', methods=['POST'])
def getCompanyList():
    data = request.get_json()
    
    # 종목코드를 받아서 딕셔너리 형태로 바꿈({"name":"code", "company1":"code1", "company2":"code2"})
    stock_cd = getStockCode()
    stock_cd.to_dict(zip(df['name'], df['code']))
    res = stock_cd
    return json.dumps(res,ensure_ascii=False)

#랭킹 페이지
@app.route('/get/rankinginfos',methods=['POST'])
def getRanking():
    #MySQL Connection 연결
    dbcon = pymysql.connect(host='ec2-13-125-236-211.ap-northeast-2.compute.amazonaws.com', port=3306, user='user',
                         passwd='stockprice', db='stock_info', charset='utf8')
    #Connection 으로부터 Cursor 생성
    curs = dbcon.cursor(pymysql.cursors.DictCursor)

    #SQL문 실행
    sql = "SELECT * FROM REQUEST"
    res = curs.execute(sql)

    #데이터 Fetch
    rows = curs.fetchall()

    #Connection 닫기
    dbcon.close()

    #프론트에 보낼 데이터
    return json.dumps(res,ensure_ascii=False)


if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5080) #이 포트 포워딩하기
