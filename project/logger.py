# -*- coding: utf-8 -*-
from datetime import datetime

def log(text):
    now = datetime.now()
    print(str(now) + ":" + text)
