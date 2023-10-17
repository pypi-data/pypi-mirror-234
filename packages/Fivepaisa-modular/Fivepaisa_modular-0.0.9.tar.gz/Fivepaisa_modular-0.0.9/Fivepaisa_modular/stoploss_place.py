from py5paisa.order import Order, OrderType, Exchange
import pandas as pd
import time as tym
from datetime import datetime, date, time
import pytz # for timezone

def sl_place(client, iDict, oDict, rec):
    
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
    lpp_factor=iDict['lpp_factor']


    ################ Placing Stoploss Order ######################
    print("SL order to be placed")
    df_pos=pd.json_normalize(client.positions())
    for i in range(len(df_pos.index)):
        if df_pos['NetQty'][i]<0:
            print("SL order placed")
            r=client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = int(df_pos['ScripCode'][i]),
                                Qty=int(abs(df_pos['NetQty'][i])), DisQty=0, 
                                Price=int(round(df_pos['SellAvgRate'][i]*Stop_loss*lpp_factor,0)),
                                IsIntraday=False, StopLossPrice=int(df_pos['SellAvgRate'][i]*Stop_loss), 
                                AHPlaced='N')
            if r!=None:
                rec1=pd.json_normalize(r)
                rec=pd.concat([rec,rec1])
            else:
                print("NONE response") 
            
    return rec
