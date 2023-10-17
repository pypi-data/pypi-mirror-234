######### Input box ############
#### Sell= 50 , Buy= 2.5 , SL= 70%

entry_time=time(9,45,0,0)   ##### entry time in hr, min, sec for strategy
num_strikes=71   ##### max no of strikes to consider: i/p odd number like 25,35,etc --> changeable
expiry= date(2023,9,13)      #### expiry selection date(yyyy,mm,dd)--> changeable
Buy_prm_closest= 2.5 ## BUY Closest premium i/p
Delay_buy=1  ## Seconds delay in sell
Sell_prm_closest= 50 ## SELL Closest premium i/p
Stop_loss=1.7 ##for 70% stoploss, Stop_loss = 1.7
lots=4 ## qty=lots*perlotqty, perlotqty is 40 for FINNIFTY, 15 for BANKNIFTY, 75 for MIDCPNIFTY, 50 for NIFTY

##FOr 1 LOT, Margin is approx 1.1L for BANKNIFTY PE and CE SELL-ONLY, 50k for BANKNIFTY PE and CE BUY-SELL
##FOr 1 LOT, Margin is approx 1.1L for FINNIFTY PE and CE SELL-ONLY, 50k for BANKNIFTY PE and CE BUY-SELL

underlying_print="BANKNIFTY"  ### "FINNIFTY", "MIDCPNIFTY", "BANKNIFTY", "NIFTY"
buy_sell_order="BS"   #### "SO" SELL-ONLY, "BS" BUY-SELL 
same_day_sqoff="E"  #### "E" for ENABLED, "D" for DISABLED
squareoff_time=time(15,15,0,0)


strike_step_dict={"BANKNIFTY": 100, "FINNIFTY":50, "MIDCPNIFTY": 50, "NIFTY": 50} ###100 for BN, 50 for FN, MIDCPNIFTY, NIFTY
strike_step=strike_step_dict[underlying_print]
underlying_dict={"FINNIFTY":999920041, "MIDCPNIFTY": 999920043, "BANKNIFTY": 999920005, "NIFTY": 999920000} 
scripcode_underlying=underlying_dict[underlying_print]
lotsize={"FINNIFTY":40, "MIDCPNIFTY": 75, "BANKNIFTY": 15, "NIFTY": 50}
lotsize_underlying=lotsize[underlying_print]
qty=int(lots*lotsize_underlying)
buy_sell_print={"SO":"SELL-ONLY", "BS": "BUY AND SELL"}

print("Input time =",datetime.now(pytz.timezone('Asia/Kolkata')))
print("::::::::::::Inputting successful:::::::::::::::::::")



pd.set_option('display.max_rows', 1000) ## to make max rows visible
pd.set_option('display.max_columns', 1000) ## to make max columns visible

