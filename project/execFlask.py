# -*- coding: utf-8 -*-
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def root():
    return 'OK'

@app.route("/reset")
def reset():
    return ""

@app.route("/ontick")
def ontick():
    directory = request.args.get('directory')

    f = open(directory + '\\datetime.txt', 'rb')
    lines = f.readlines()
    for line in lines:
        line = line.decode().strip()
        print(line)
        print(datetime.fromtimestamp(int(line)))
    return 'OK'

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=80)