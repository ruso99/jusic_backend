#-*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template
import json
import getStockData
import pymysql


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

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    #받아온 데이터에 해당하는 데이터 크롤링
    userName = data["nickname"]
    companyName = data["companyName"]
    companyCode = data["companyCode"]
    toYear = data["toYear"]
    toMonth= data["toMonth"]
    toDay = data["toDay"]
    agencyNetsales = data["agencyNetsales"]
    foreignerNetsales = data["foreignNetsales"]
    foreignerSharesheld = data["foreignSharesheld"]
    usdkrw = data["usdkrw"]
    jpykrw = data["jpykrw"]
    cnykrw = data["cnykrw"]
    kospi = data["kospi"]
    kosdaq = data["kosdaq"]
    dji = data["dji"]
    nas = data["nas"]
    shs = data["shs"]
    nii = data["nii"]
    indicatorOne = data["supplementaryIndicator"]
    indicatorTwo = data["supplementaryIndicator"]

    #여기서 딥러닝 작업

=======
>>>>>>> parent of c436714... [ADD]getCompanyList() 추가
=======
>>>>>>> parent of c436714... [ADD]getCompanyList() 추가
=======
>>>>>>> parent of c436714... [ADD]getCompanyList() 추가
    #프론트에 보낼 데이터(넘겨야할 데이터를 여기에 담으면 됨, 무조건 딕셔너리 형태로 담아야함)
    res = { "result" : "성공" }

    #결과를 DB에 저장

    return json.dumps(res,ensure_ascii=False)

#페이지 첫 로드시에 가져오는 데이터
@app.route('/get/company/list', methods=['POST'])
def getCompanyList():
    data = request.get_json()

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    # 종목코드를 받아서 딕셔너리 형태로 바꿈({"name":"code", "company1":"code1", "company2":"code2"})
    df = getStockCode()
    res = df.set_index('name').T.to_dict('list')
    return json.dumps(res,ensure_ascii=False)

#랭킹 페이지
@app.route('/get/rankinginfos',methods=['POST'])
def getRanking():
    #MySQL Connection 연결
    dbcon = pymysql.connect(host='stockprice.ch9x2a3fnkvg.ap-northeast-2.rds.amazonaws.com', port=3306, user='admin',
                         passwd='stockprice', db='stock_info', charset='utf8')
    #Connection 으로부터 Cursor 생성
    curs = dbcon.cursor()

    #SQL문 실행
    sql = "select diff_rate,nickname,companyName,toYear,toMonth,toDay,agencyNetsales,foreignNetsales,foreignSharesheld,usdkrw,jpykrw,cnykrw,kospi,kosdaq,dji,nas,shs,nii FROM REQUEST ORDER BY diff_rate DESC"
    curs.execute(sql)

    #데이터 Fetch
    rows = curs.fetchall()

    #Connection 닫기
    dbcon.close()

    #프론트에 보낼 데이터
    res = rows
    return json.dumps(res,ensure_ascii=False)

#기록을 전송
@app.route('/get/record')
def getRecord():
    data = request.get_json()

=======
    res = { "result" : "성공" }
>>>>>>> parent of c436714... [ADD]getCompanyList() 추가
=======
    res = { "result" : "성공" }
>>>>>>> parent of c436714... [ADD]getCompanyList() 추가
=======
    res = { "result" : "성공" }
>>>>>>> parent of c436714... [ADD]getCompanyList() 추가
    return json.dumps(res,ensure_ascii=False)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5080) #이 포트 포워딩하기