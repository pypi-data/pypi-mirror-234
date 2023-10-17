import pandas as pd
import numpy as np
from datetime import datetime, date, time
import time as tym
import pytz # for timezone
from py5paisa.order import Order, OrderType, Exchange
from IPython.display import clear_output, display


def df_strikeprice_func(client, iDict, Scripmaster):

    entry_time=iDict['entry_time']
    num_strikes=iDict['num_strikes']
    expiry=iDict['expiry'] 
    Buy_prm_closest=iDict['Buy_prm_closest']
    Delay_buy=iDict['Delay_buy'] 
    Sell_prm_closest=iDict['Sell_prm_closest'] 
    qty=iDict['qty']
    Stop_loss=iDict['Stop_loss']
    strike_step=iDict['strike_step']
    underlying_print=iDict['underlying_print']
    Scripcode_underlying=iDict['Scripcode_underlying'] 
    
    start = tym.time() ## time counter start
    ######### Codes for fetching underlying live value into df_strikeprice ##########
    today=datetime.now(pytz.timezone('Asia/Kolkata')).date()
    code_start=datetime.now(pytz.timezone('Asia/Kolkata')).time()
    print("New Code start time=",code_start)
    #will work on Saturday too with client.historical data fetching last market day data for today
    #print(today)
    underlying= client.historical_data('N','C',Scripcode_underlying,'1m',today,today)
    ## historical_data(<Exchange>,<Exchange Type>,<Scrip Code>,<Time Frame>,<From Data>,<To Date>)
    ## Exchange: N- NSE, B- BSE, M- Mcx
    ## Exchange Type: exchange_segment C- Cash, D- Derivative, U-Currency
    ## Scripcode: Refer Scripmaster
    ## Time Frame: 1m, 5m, 10m, 15m, 30m, 60m, 1d
    ## From Date: Start date
    ## To  Date: End Date

    ######### Codes for strikes generation for Underlying into df_strikeprice ##########

    underlying_ref= round((underlying["Close"][len(underlying)-1])/strike_step,0)*strike_step

    df_strikeprice=pd.DataFrame(index=range(num_strikes))
    df_strikeprice["Strike_Selection"]=np.nan  ## filling  strike price column with nan values in new column
    df_strikeprice["Scripcode_CE"]=np.nan ## filling CE scripcode column with nan values in new column
    df_strikeprice["Scripcode_PE"]=np.nan ## filling  PE scripcode columnwith nan values in new column
    df_strikeprice["CE_LTP"]=np.nan ## filling  CE LTP columnwidth nan values in new column
    df_strikeprice["PE_LTP"]=np.nan ## filling  PE LTP columnwidth nan values in new column

    for i in range(num_strikes):   ## finding all the strikes referring ATM calculated as above
        df_strikeprice["Strike_Selection"][i]=underlying_ref - strike_step*((num_strikes-1)/2-i)


    ######### Codes for Scripcode selection for scripcodes of above strikes and output into df_strikeprice ##########

    #Scripmaster = pd.read_csv('scripmaster-csv-format.csv')  ## to read csv files

    #Convert datetime like "01-01-2023 14:00:00" in datetime column to date
    Scripmaster['Expiry'] = pd.to_datetime(Scripmaster['Expiry']).dt.date
    #Alternate method Scripmaster['Expiry']=pd.to_datetime(Scripmaster['Expiry'], format='%Y-%m-%d').dt.date


    Scripmaster_CE=Scripmaster[(Scripmaster.ISIN == underlying_print)  & (Scripmaster.Expiry == expiry) & (Scripmaster.CpType=="CE")]  ## Setting filter in columns
    Scripmaster_PE=Scripmaster[(Scripmaster.ISIN == underlying_print) & (Scripmaster.Expiry == expiry) & (Scripmaster.CpType=="PE")] ## Setting filter in columns
    #Scripmaster_CE and Scripmaster_PE are temporary dataframe tables for filtering current expiry PE scripcode values from Scripmaster

    Scripmaster_CE.reset_index(inplace=True) ## Resetting the index and after slicing dataframe
    Scripmaster_PE.reset_index(inplace=True) ## Resetting the index and after slicing dataframe

    for i in range(len(df_strikeprice.index)):  ## looking for strikes from data extr from CSV and saving respective scripcodes
        for j in range(len(Scripmaster_CE.index)):
            if Scripmaster_CE['StrikeRate'][j]==df_strikeprice['Strike_Selection'][i]:
                df_strikeprice['Scripcode_CE'][i]=Scripmaster_CE['Scripcode'][j]
        for k in range(len(Scripmaster_PE.index)):
            if Scripmaster_PE['StrikeRate'][k]==df_strikeprice['Strike_Selection'][i]:
                df_strikeprice['Scripcode_PE'][i]=Scripmaster_PE['Scripcode'][k]
                
    mid1 = tym.time()
    ###########Code for fetching CE and PE LTPs of strike prices in each row from 5PAISA live data##########

    temp_dataframe=pd.DataFrame() ##temporary dataframe for receiving historical price table
    temp_empty=pd.DataFrame() ##empty dataframe only used for making temp_dataframe empty

    for i in range(len(df_strikeprice.index)):    # if len is 2, range(len) is 0,1,2. for i in range(len) starts from i=0 and doesnot execute for i=len
        if np.isnan(df_strikeprice['Scripcode_CE'][i])==False:
            temp_dataframe=client.historical_data('N','d',int(df_strikeprice['Scripcode_CE'][i]),'1m',today,today) ##from 5paisa
            if temp_dataframe.empty is None:
                temp_dataframe=temp_empty
            elif temp_dataframe.empty==False:
                df_strikeprice.loc[i,'CE_LTP']=temp_dataframe['Close'].iloc[-1]
                temp_dataframe=temp_empty  ## clear temp_dataframe using empty dataframe temp_empty
            else:
                temp_dataframe=temp_empty
        if np.isnan(df_strikeprice['CE_LTP'][i]):
            df_strikeprice.loc[i,'CE_LTP']=10000 #replacing NaN with large no like 10000


        if np.isnan(df_strikeprice['Scripcode_PE'][i])==False:
            temp_dataframe=client.historical_data('N','d',int(df_strikeprice['Scripcode_PE'][i]),'1m',today,today) ##from 5paisa
            if temp_dataframe.empty is None:
                temp_dataframe=temp_empty
            elif temp_dataframe.empty==False:
                df_strikeprice.loc[i,'PE_LTP']=temp_dataframe['Close'].iloc[-1]
                temp_dataframe=temp_empty  ## clear temp_dataframe using empty dataframe temp_empty
            else:
                temp_dataframe=temp_empty
        if np.isnan(df_strikeprice['PE_LTP'][i]):
            df_strikeprice.loc[i,'PE_LTP']=10000 #replacing NaN with large no like 10000

    mid2 = tym.time()

    ########Code for finding Scripcode of CE nearest to 110 and 10 premiums#######
    lst = df_strikeprice['CE_LTP'].to_numpy()

    CE_indx_SELL= (np.abs(lst - Sell_prm_closest)).argmin()
    CE_indx_BUY= (np.abs(lst - Buy_prm_closest)).argmin()

    CE_Scripcode_SELL=df_strikeprice.loc[CE_indx_SELL,'Scripcode_CE']
    CE_Scripcode_SELL = getattr(CE_Scripcode_SELL, "tolist", lambda: CE_Scripcode_SELL)() ##convert numpy int32 to native int to avoid 5paisa json serializable error
    CE_Scripcode_BUY=df_strikeprice.loc[CE_indx_BUY,'Scripcode_CE']
    CE_Scripcode_BUY = getattr(CE_Scripcode_BUY, "tolist", lambda: CE_Scripcode_BUY)() ##convert numpy int32 to native int to avoid 5paisa json serializable error

    ########Code for finding Scripcode of PE nearest to 110 and 10 premiums#######
    lst = df_strikeprice['PE_LTP'].to_numpy()
    PE_indx_SELL= (np.abs(lst - Sell_prm_closest)).argmin()
    PE_indx_BUY= (np.abs(lst - Buy_prm_closest)).argmin()

    PE_Scripcode_SELL=df_strikeprice.loc[PE_indx_SELL,'Scripcode_PE']
    PE_Scripcode_SELL = getattr(PE_Scripcode_SELL, "tolist", lambda: PE_Scripcode_SELL)() ##convert numpy int32 to native int to avoid 5paisa json serializable error
    PE_Scripcode_BUY=df_strikeprice.loc[PE_indx_BUY,'Scripcode_PE']
    PE_Scripcode_BUY = getattr(PE_Scripcode_BUY, "tolist", lambda: PE_Scripcode_BUY)() ##convert numpy int32 to native int to avoid 5paisa json serializable error 
    
    oDict={'CE_Scripcode_SELL':CE_Scripcode_SELL,
            'CE_Scripcode_BUY':CE_Scripcode_BUY,
            'PE_Scripcode_SELL':PE_Scripcode_SELL,
            'PE_Scripcode_BUY':PE_Scripcode_BUY}
    
    code_completion=tym.time()
    ##########Print strike selection, scripcode and LTPs#######################
    clear_output()
    print("Expiry date=",expiry)
    print("Code start time=",code_start)
    print("time till fetching data from 5paisa=", mid1-start)
    print("Time for fetching LTPs from 5paisa/above looptime=", mid2-mid1)
    print("Time after loop=",code_completion-mid2)
    print("Code Completion time=",code_completion-start)

    print("\n",underlying_print," LTP= ",round(underlying["Close"][len(underlying)-1],0))
    print("Strike CE=",df_strikeprice.loc[CE_indx_SELL,'Strike_Selection'],
        "  Price=",df_strikeprice.loc[CE_indx_SELL,'CE_LTP'],
        "   Scripcode=",df_strikeprice.loc[CE_indx_SELL,'Scripcode_CE'])
    print("Strike PE=",df_strikeprice.loc[PE_indx_SELL,'Strike_Selection'],
        "  Price=",df_strikeprice.loc[PE_indx_SELL,'PE_LTP'],
        "   Scripcode=",df_strikeprice.loc[PE_indx_SELL,'Scripcode_PE'])
    print("Strike CE=",df_strikeprice.loc[CE_indx_BUY,'Strike_Selection'],
        "  Price=",df_strikeprice.loc[CE_indx_BUY,'CE_LTP'],
        "   Scripcode=",df_strikeprice.loc[CE_indx_BUY,'Scripcode_CE'])
    print("Strike PE=",df_strikeprice.loc[PE_indx_BUY,'Strike_Selection'],
        "  Price=",df_strikeprice.loc[PE_indx_BUY,'PE_LTP'],
        "   Scripcode=",df_strikeprice.loc[PE_indx_BUY,'Scripcode_PE'])
    return [df_strikeprice,oDict]