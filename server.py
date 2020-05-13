#-*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

def getStockCode():

        url = 'https://dev-kind.krx.co.kr/corpgeneral/corpList.do'
        df = pd.read_html(url, header=0)[0]
        df = df[['회사명','종목코드']]
        df = df.rename(columns={'회사명':'name','종목코드':'code'})
        return df

@app.route('/get/result', methods=['POST'])
def getResult():
    #받아오는 데이터
    data = request.get_json()

    #여기서 작업

    # 받아온 데이터에 해당하는 데이터 크롤링

    # 크롤링한 데이터 딥러닝에 전달

    #프론트에 보낼 데이터(넘겨야할 데이터를 여기에 담으면 됨, 무조건 딕셔너리 형태로 담아야함)
    res = { "result" : "성공" }
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

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5080)