from py5paisa.order import Order, OrderType, Exchange
import pandas as pd
import time as tym
from datetime import datetime, date, time
import pytz # for timezone

def order_place(client, iDict, oDict):
    
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
    
    
    rec=pd.DataFrame()
    
    if buy_sell_order=="BS":
        print("BUY AND SELL")
        print("CE BUY order placed")
        r=client.place_order(OrderType='B',Exchange='N',ExchangeType='D',
                    ScripCode= int(CE_Scripcode_BUY),
                    Qty=qty, DisQty=qty, IsIntraday= False, IsStopLossOrder= False,
                        StopLossPrice=0, Price= 0,AHPlaced='N')   ## To place CE Buy
        if r!=None:
            rec1=pd.json_normalize(r)
            rec=pd.concat([rec,rec1])
        else:
            print("NONE response")    

        print("PE BUY order placed")
        r=client.place_order(OrderType='B',Exchange='N',ExchangeType='D',
                    ScripCode= int(PE_Scripcode_BUY),
                    Qty=qty, DisQty=qty, IsIntraday= False, IsStopLossOrder= False,
                        StopLossPrice=0, Price= 0, AHPlaced='N')  ## To place PE Buy
        if r!=None:
            rec1=pd.json_normalize(r)
            rec=pd.concat([rec,rec1])
        else:
            print("NONE response") 
            
        tym.sleep(Delay_buy) #to add delay between buy and sell
    
    if buy_sell_order=="SO":
        print("SELL ONLY")
    
    print("CE SELL order placed")
    r=client.place_order(OrderType='S',Exchange='N',ExchangeType='D',
                ScripCode = int(CE_Scripcode_SELL),
                Qty=qty, DisQty=qty, IsIntraday= False, IsStopLossOrder= False,
                    StopLossPrice=0, Price= 0, AHPlaced='N') ## To place CE Sell
    if r!=None:
        rec1=pd.json_normalize(r)
        rec=pd.concat([rec,rec1])
    else:
        print("NONE response") 

    tym.sleep(Delay_buy) #to add delay between sell and sell
    print("PE SELL order placed")
    r=client.place_order(OrderType='S',Exchange='N',ExchangeType='D',
                ScripCode = int(PE_Scripcode_SELL),
                Qty=qty, DisQty=qty, IsIntraday= False, IsStopLossOrder= False,
                    StopLossPrice=0, Price= 0, AHPlaced='N') ## To place PE Sell
    if r!=None:
        rec1=pd.json_normalize(r)
        rec=pd.concat([rec,rec1])
    else:
        print("NONE response") 

    tym.sleep(Delay_buy)

    return rec
