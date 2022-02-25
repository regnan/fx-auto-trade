# -*- coding: utf-8 -*-
from flask import Flask
import predict

app = Flask(__name__)

@app.route("/")
def root():
    return 'OK'

@app.route("/reset")
def reset():
    return ""

@app.route("/ontick")
def ontick():
    result =  predict.predict()
    print("predictresult:" + str(result))
    return str(result)

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=80)