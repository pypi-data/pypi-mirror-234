import pandas as pd
from datetime import datetime, date, time
import time as tym
import pytz # for timezone
from py5paisa.order import Order, OrderType, Exchange

def create_logbook(client):
    ###########For creating log##############
    order_book=client.order_book()
    order_book=pd.json_normalize(order_book)
    datestring=datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y.%m.%d_%H.%M.%S")
    log=pd.DataFrame()

    for i in range(len(order_book.index)):
    # df_strikeprice.loc[i,'CE_LTP']
        log.loc[i,'ExchOrderTime1']=datetime.fromtimestamp(float(order_book['ExchOrderTime'].iloc[i][6:16]))
        log.loc[i,'Script']=order_book['ScripName'].iloc[i]
        log.loc[i,'BuySell']=order_book['BuySell'].iloc[i]
        log.loc[i,'TradedQty']=order_book['Qty'].iloc[i]
        log.loc[i,'Price']=order_book['AveragePrice'].iloc[i]

    log['Entry Date']=log['ExchOrderTime1'].dt.date
    log['Entry Time']=log['ExchOrderTime1'].dt.time

    log.loc[(log['Script'].str[22:24] == 'CE'), 'CE/PE'] = 'Call'
    log.loc[(log['Script'].str[22:24] == 'PE'), 'CE/PE'] = 'Put'
    log['strike'] = log['Script'].str[25:30]
    log.loc[(log['BuySell'] == 'B'), 'BUY/SELL'] = 'BUY'
    log.loc[(log['BuySell'] == 'S'), 'BUY/SELL'] = 'SELL'

    log['Qty']=log['TradedQty'].astype(int)
    log['price']=log['Price']
    log=log.drop(['ExchOrderTime1','Script','BuySell','TradedQty','Price'], axis=1)

    return log