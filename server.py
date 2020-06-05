#-*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
#import getStockData
import pymysql
import pandas as pd

app = Flask(__name__)
CORS(app)

def getStockCode():
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
        df = pd.read_html(url, header=0)[0]
        #df = df[['회사명','종목코드']]
        df = df.rename(columns={'회사명':'name','종목코드':'code'})
        df['code'] = df['code'].astype(str)
        df['code'] = df['code'].str.zfill(6)

        return df


#페이지 첫 로드시에 가져오는 데이터
@app.route('/get/company/list', methods=['POST'])
def getCompanyList():
        data = request.get_json()

        # 종목코드를 받아서 딕셔너리 형태로 바꿈({"name":"code", "company1":"code1", "company2":"code2"})
        df = getStockCode()
        res = df.set_index('name').T.to_dict('list')
        return json.dumps(res,ensure_ascii=False)


@app.route('/get/result', methods=['GET'])
def getResult():
        #받아오는 데이터
        data = request.get_json()
        data = json.loads(data)

        nickname = data['nickname']
        companyName = data['companyName']
        companyCode = data['companyCode']
        startDate = data['startDate']
        predictDate = data['predictDate']
        agencyNetsales = data['agencyNetsales']
        foreignNetsales = data['foreignNetsales']
        foreignSharesheld = data['foreignSharesheld']
        usdkrw = data['usdkrw']
        jpykrw = data['jpykrw']
        cnykrw = data['cnykrw']
        kospi = data['kospi']
        kosdaq = data['kosdaq']
        dji = data['dji']
        nas = data['nas']
        shs = data['shs']
        nii = data['nii']
        ex1 = data['ex1']
        ex2 = data['ex2']
        ex3 = data['ex3']
        ex4 = data['ex4']
        ex5 = data['ex5']
        ex6 = data['ex6']

        #딥러닝 작업
        result = Deeplearning.run(data)

        #클라이언트로부터 받아온 데이터(data) 와 딥러닝 결과를 DB에 저장
        dbcon = pymysql.connect(host='ec2-13-125-236-211.ap-northeast-2.compute.amazonaws.com', port=3306, user='user',passwd='stockprice', db='stock_info', charset='utf8')
        curs = dbcon.cursor(pymysql.cursors.DictCursor)

        #reqNum값 구하기
        sql = ("SELECT MAX(reqNum) FROM REQUEST")
        curs.execute(sql)
        reqNum = curs.fetchall()
        #print(reqNum[0]["MAX(reqNum)"])
        reqNum = reqNum[0]["MAX(reqNum)"]+1

        #클라이언트로부터 온 데이터 DB에 저장
        sql1 = """INSERT INTO REQUEST(reqNum,nickname,companyName,companyCode,startDate,predictDate,agencyNetsales,foreignNetsales,foreignSharesheld,usdkrw,jpykrw,cnykrw,kospi,kosdaq,dji,nas,shs,nii,ex1,ex2,ex3,ex4,ex5,ex6,diffRate)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        sql2 = """INSERT INTO 'RESULT(reqNum,date,close,predicted) VALUES(%s,%s,%s,%s)"""

        curs.execute(sql1,(reqNum,nickname,companyName,companyCode,startDate,predictDate,agencyNetsales,foreignNetsales,foreignSharesheld,usdkrw,jpykrw,cnykrw,kospi,kosdaq,dji,nas,shs,nii,ex1,ex2,ex3,ex4,ex5,ex6,result['error']))

        #딥러닝 결과를 DB에 저장
        for i in len(result['predicted']):
                curs.execute(sql2,(reqNum,result['predicted_Date'][i],result['real_Close'][i],result['predicted_Close'][i]))

        dbcon.close()

        return json.dumps(result,ensure_ascii=False)


@app.route('/get/rankinginfo', methods=['GET'])
def getRankingInfo():
        dbcon = pymysql.connect(host='ec2-13-125-236-211.ap-northeast-2.compute.amazonaws.com', port=3306, user='user',passwd='stockprice', db='stock_info', charset='utf8')
        curs = dbcon.cursor(pymysql.cursors.DictCursor)

        sql1 = "SELECT nickname,companyName,companyCode,startDate,predictDate,agencyNetsales,foreignNetsales,foreignSharesheld, usdkrw,jpykrw, cnykrw, kospi, kosdaq, dji, nas, shs, nii,ex1,ex2,ex3,ex4,ex5,ex6,diffRate  FROM REQUEST"
    
        req = curs.execute(sql1)
        rows = curs.fetchall()
        for i in range(len(rows)):
                rows[i]['RankingNum'] = (i+1)
        dbcon.close()

        return json.dumps(rows,ensure_ascii=False)


#랭킹 페이지(랭킹기록과 다이얼로그데이터보냄)
@app.route('/get/rankinginfos', methods=['GET'])
def getRankingInfos():

        dbcon = pymysql.connect(host='ec2-13-125-236-211.ap-northeast-2.compute.amazonaws.com', port=3306, user='user',passwd='stockprice', db='stock_info', charset='utf8')
        curs = dbcon.cursor(pymysql.cursors.DictCursor)

        #dic의 'response'
        sql1 = "SELECT nickname,companyName,companyCode,startDate,predictDate,agencyNetsales,foreignNetsales,foreignSharesheld, usdkrw,jpykrw, cnykrw, kospi, kosdaq, dji, nas, shs, nii,ex1,ex2,ex3,ex4,ex5,ex6,diffRate  FROM REQUEST  ORDER BY diffRate ASC"
        req = curs.execute(sql1)
        reqRows = curs.fetchall()
        for i in range(len(reqRows)):
                reqRows[i]['RankingNum'] = (i+1)

        #dic의 'result'
        reqNumArr = []
        sql = 'SELECT reqNum FROM REQUEST ORDER BY reqNum ASC'
        reqNumArr = curs.execute(sql)
        reqNumArr = curs.fetchall()
        #print(reqNumArr[0]['reqNum'])

        res = []

        for i in reqNumArr:
                #print(i)
                try:
                        #print(type(i[0]))
                        index = i['reqNum']
                        sql2 = 'SELECT * FROM RESULT WHERE reqNum=%d'%(index)
                        x = curs.execute(sql2)
                        x = curs.fetchall()
                        res.append(x)

                except KeyError:
                        res = "error"
        #print(res)
        dic = {}
        dic["request"] = reqRows
        dic["result"] = res
        #print(dic)

        dbcon.close()

        return json.dumps(dic,ensure_ascii=False)





if __name__ == '__main__':
        app.run(host = '0.0.0.0',port=5000) #이 포트 포워딩하기


