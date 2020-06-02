from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
#import getStockData
import pymysql


app = Flask(__name__)
CORS(app)

def getStockCode():
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
        df = pd.read_html(url, header=0)[0]
        df = df[['회사명','종목코드']]
        df = df.rename(columns={'회사명':'name','종목코드':'code'})
        df['code'] = df['code'].astype(str)
        df['code'] = df['code'].str.zfill(6)

        return df


@app.route('/get/result', methods=['POST'])
def getResult():
    #받아오는 데이터
    data = request.get_json()

    #여기서 작업

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

    #프론트에 보낼 데이터(넘겨야할 데이터를 여기에 담으면 됨, 무조건 딕셔너리 형태로 담아야함)
    res = { "result" : "성공" }

    #결과를 DB에 저장

    return json.dumps(res,ensure_ascii=False)

#페이지 첫 로드시에 가져오는 데이터
@app.route('/get/company/list', methods=['POST'])
def getCompanyList():
    data = request.get_json()

    # 종목코드를 받아서 딕셔너리 형태로 바꿈({"name":"code", "company1":"code1", "company2":"code2"})
    df = getStockCode()
    res = df.set_index('name').T.to_dict('list')
    return json.dumps(res,ensure_ascii=False)

#랭킹 페이지
@app.route('/get/rankinginfos',methods=['POST'])
def getRanking():
    #해당 DB에는 외부접속가능하니 접속해서 DB구조 옮기고 설정하면 됨
    #MySQL Connection 연결
    dbcon = pymysql.connect(host='ec2-13-125-236-211.ap-northeast-2.compute.amazonaws.com', port=3306, user='user',
                         passwd='stockprice', db='', charset='utf8')
    #Connection 으로부터 Cursor 생성
    curs = dbcon.cursor()

    #SQL문 실행
    sql = "select diff_rate,nickname,companyName,toYear,toMonth,toDay,agencyNetsales,foreignNetsales,foreignSharesheld,usdkrw,jpykrw,cnykrw,kospi,kosdaq,dji,nas,shs,nii FROM REQUEST ORDER BY diff_rate DESC"
    curs.execute(sql)

    #데이터 Fetch
    rows = curs.fetchall()
    print(rows)
    #Connection 닫기
    dbcon.close()

    #프론트에 보낼 데이터
    res = rows
    #return json.dumps(res,ensure_ascii=False)
    return res

#기록을 전송
@app.route('/get/record')
def getRecord():
    data = request.get_json()

    return json.dumps(res,ensure_ascii=False)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5000) #이 포트 포워딩하기