#-*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

@app.route('/main/test', methods=['POST'])
def post_test():
    #받아오는 데이터
    data = request.get_json()

    #여기서 작업

    #프론트에 보낼 데이터(넘겨야할 데이터를 여기에 담으면 됨, 무조건 딕셔너리 형태로 담아야함)
    res = { "result" : "성공" }
    return json.dumps(res,ensure_ascii=False)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5080)