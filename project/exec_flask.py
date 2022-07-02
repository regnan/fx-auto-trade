# -*- coding: utf-8 -*-
from flask import Flask
import predict

app = Flask(__name__)
request_count = 0

@app.route("/")
def root():
    return 'OK'

@app.route("/reset")
def reset():
    return ""

@app.route("/ontick//<int:timeFrame>")
def ontick(timeFrame):
    # global request_count 
    # request_count = request_count + 1
    # if request_count < 100:
    #     return ""
    result =  predict.predict(timeFrame)
    print("predictresult:" + str(result))
    return str(result)

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=80)