# -*- coding: utf-8 -*-
from flask import Flask, request
from datetime import datetime
from historyData import HistoryPeriods
import historyLoader
from attribute import Attribute
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
    return str(result)

def MonthlyDataconvert(year, month, historyPeriod):
    historyData = historyLoader.loadMonthlyHistory(year, month, historyPeriod)
    return convert(historyData)
    
def convert(historyData):
    attribute = Attribute(historyData)
    return attribute.result

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=80)