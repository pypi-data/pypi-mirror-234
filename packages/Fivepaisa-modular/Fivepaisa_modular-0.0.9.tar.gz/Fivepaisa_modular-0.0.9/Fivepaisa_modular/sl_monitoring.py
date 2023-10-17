import pandas as pd
import numpy as np
from datetime import datetime, date, time
import time as tym
import pytz # for timezone
from py5paisa.order import Order, OrderType, Exchange
from IPython.display import clear_output

def sl_monitor(client, iDict, rec):

    rec=rec
    Stop_loss=iDict['Stop_loss'] 

    today=datetime.now(pytz.timezone('Asia/Kolkata')).date()
    temp_dataframe=pd.DataFrame()
    clear_dataframe=pd.DataFrame()

    df_order=pd.json_normalize(client.order_book())
    df_order=df_order[(df_order.OrderStatus == "Pending")]
    df_order=df_order[['ExchOrderID','OrderStatus','SLTriggerRate','ScripCode','ScripName','Qty']]
    df_order.reset_index(inplace=True)


    df_pos=pd.json_normalize(client.positions())
    # df_pos=pd.read_pickle("df_pos3.pkl")
    df_pos=df_pos[(df_pos.NetQty<0)]
    df_pos.reset_index(inplace=True)

    prices_dataframe1=pd.DataFrame(index=range(len(df_pos.index)))
    prices_dataframe1['Close']='NaN'
    prices_dataframe1['Scripcode']='NaN'
    prices_dataframe1['ScripName']='NaN'
    prices_dataframe1['ExchOrderID']='NaN'
    prices_dataframe1['SLTriggerRate']='NaN'
    prices_dataframe1['Qty']='NaN'
    prices_dataframe1['Sell_Price']='NaN'


    for i in range(len(df_pos.index)):
        temp_dataframe=client.historical_data('N','d',int(df_pos.iloc[i]['ScripCode']),'1m',today,today)
        if temp_dataframe.empty is None:
            print("None historical data")
        elif temp_dataframe.empty==False:
            prices_dataframe1.loc[i,'Close']=temp_dataframe.iloc[-1]['Close']
        prices_dataframe1.loc[i,'Scripcode']=df_pos.iloc[i]['ScripCode']
        prices_dataframe1.loc[i,'ScripName']=df_pos.iloc[i]['ScripName']
        prices_dataframe1.loc[i,'Qty']=int(abs(df_pos.iloc[i]['NetQty']))
        if df_pos.loc[i,'SellAvgRate']==0:
        prices_dataframe1.loc[i,'Sell_Price']=df_pos.iloc[i]['AvgRate']
        else:
        prices_dataframe1.loc[i,'Sell_Price']=df_pos.iloc[i]['SellAvgRate']

    for i in range(len(prices_dataframe1.index)):
        for j in range(len(df_order.index)):
            if df_order.loc[j,'ScripCode']==prices_dataframe1.loc[i,'Scripcode']:
                prices_dataframe1.loc[i,'ExchOrderID']=df_order.loc[j,'ExchOrderID']
                prices_dataframe1.loc[i,'SLTriggerRate']=df_order.loc[j,'SLTriggerRate']

    tym.sleep(10)

    df_pos=pd.json_normalize(client.positions())
    # df_pos=pd.read_pickle("df_pos3.pkl")
    df_pos=df_pos[(df_pos.NetQty<0)]
    df_pos.reset_index(inplace=True)

    prices_dataframe2=pd.DataFrame(index=range(len(df_pos.index)))
    prices_dataframe2['Close']='NaN'
    prices_dataframe2['Scripcode']='NaN'
    prices_dataframe2['ScripName']='NaN'
    prices_dataframe2['ExchOrderID']='NaN'
    prices_dataframe2['SLTriggerRate']='NaN'
    prices_dataframe2['Qty']='NaN'
    prices_dataframe2['Sell_Price']='NaN'

    for i in range(len(df_pos.index)):
        temp_dataframe=client.historical_data('N','d',int(df_pos.iloc[i]['ScripCode']),'1m',today,today)
        if temp_dataframe.empty is None:
            print("None historical data")
        elif temp_dataframe.empty==False:
            prices_dataframe2.loc[i,'Close']=temp_dataframe.iloc[-1]['Close']
        prices_dataframe2.loc[i,'Scripcode']=df_pos.iloc[i]['ScripCode']
        prices_dataframe2.loc[i,'ScripName']=df_pos.iloc[i]['ScripName']
        prices_dataframe2.loc[i,'Qty']=int(abs(df_pos.iloc[i]['NetQty']))
        if df_pos.loc[i]['SellAvgRate']==0:
        prices_dataframe2.loc[i,'Sell_Price']=df_pos.iloc[i]['AvgRate']
        else:
        prices_dataframe2.loc[i,'Sell_Price']=df_pos.iloc[i]['SellAvgRate']

    for i in range(len(prices_dataframe2.index)):
        for j in range(len(df_order.index)):
            if df_order.loc[j,'ScripCode']==prices_dataframe2.loc[i,'Scripcode']:
                prices_dataframe2.loc[i,'ExchOrderID']=df_order.loc[j,'ExchOrderID']
                prices_dataframe2.loc[i,'SLTriggerRate']=df_order.loc[j,'SLTriggerRate']

    # prices_dataframe1.loc[1,'Close']=1000 for testing
    # prices_dataframe2.loc[1,'Close']=1000 for testing
    if(len(prices_dataframe1.index))==0:
    print("NO sell positions for SL monitoring at: ",datetime.now(pytz.timezone('Asia/Kolkata')))

    for i in range(len(prices_dataframe1.index)):
        for j in range(len(prices_dataframe2.index)):
            if prices_dataframe2.loc[j,'Scripcode']==prices_dataframe1.loc[i,'Scripcode']:
                if (prices_dataframe2.loc[j,'Close']>Stop_loss*prices_dataframe2.loc[j,'Sell_Price'])&(prices_dataframe1.loc[i,'Close']>Stop_loss*prices_dataframe1.loc[i,'Sell_Price']):
                # if (prices_dataframe2.loc[j,'Close']>-1)&(prices_dataframe1.loc[i,'Close']>-1):
                    print("At time:",datetime.now(pytz.timezone('Asia/Kolkata')),", Price beyond SL for: ",prices_dataframe2.loc[j,'ScripName'])
                    if prices_dataframe1.loc[i,'ExchOrderID']!='NaN':
                    client.cancel_order(exch_order_id=prices_dataframe1.loc[i,'ExchOrderID'])
                    print("Existing SL order cancelled")
                    print("Squaring OFF")
                    r=client.place_order(OrderType='B',Exchange='N',ExchangeType='D',ScripCode= int(prices_dataframe2.loc[j,'Scripcode']),Qty=int(prices_dataframe1.loc[i,'Qty']), DisQty=int(prices_dataframe1.loc[i,'Qty']), IsIntraday= False, IsStopLossOrder= False,
                        StopLossPrice=0, Price= 0,AHPlaced='N')   ## To place CE Buy
                    if r!=None:
                        rec1=pd.json_normalize(r)
                        rec=pd.concat([rec,rec1])
                    else:
                        print("NONE response")
                else:
                    print("At time:",datetime.now(pytz.timezone('Asia/Kolkata')),", SL monitoring OK for: ",prices_dataframe2.loc[j,'ScripName'])

return rec