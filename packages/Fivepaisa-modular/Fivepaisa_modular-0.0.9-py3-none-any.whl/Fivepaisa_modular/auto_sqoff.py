from py5paisa.order import Order, OrderType, Exchange
import pandas as pd
import time as tym
from datetime import datetime, date, time
import pytz # for timezone

def sqoff_place(client, iDict, oDict):
    
    CE_Scripcode_SELL=oDict['CE_Scripcode_SELL']
    CE_Scripcode_BUY=oDict['CE_Scripcode_BUY']
    PE_Scripcode_SELL=oDict['PE_Scripcode_SELL']
    PE_Scripcode_BUY=oDict['PE_Scripcode_BUY']
    
    qty=iDict['qty']
    buy_sell_order=iDict['buy_sell_order']
    same_day_sqoff=iDict['same_day_sqoff']
    Delay_buy=iDict['Delay_buy']
    Stop_loss=iDict['Stop_loss']
    squareoff_time=iDict['squareoff_time']


    ############## SAME DAY SL and AUTOSQUAREOFF CODE###########
    if same_day_sqoff=="E":
        print("Waiting for square-off at", squareoff_time)
        while True:
            tym.sleep(5)
            if squareoff_time<datetime.now(pytz.timezone('Asia/Kolkata')).time():
                print("Autosquareoff started at=",datetime.now(pytz.timezone('Asia/Kolkata')).time())
                client.squareoff_all()
                tym.sleep(5)
                client.squareoff_all()
                a="square off all completed"
                print(a)
                break
    else:
        a="auto_squareoff disabled"
        print(a)
    return a