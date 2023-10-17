############# Import library modules #############
import pandas as pd
from datetime import datetime, date, time
import pytz # for timezone

###########Scripmaster Input########
def scripmaster_download_func():
    #Scripmaster = pd.read_csv('scripmaster-csv-format.csv')
    Scripmaster = pd.read_csv('https://images.5paisa.com/website/scripmaster-csv-format.csv')
    print("Last scripmaster download on =", datetime.now(pytz.timezone('Asia/Kolkata')))
    return Scripmaster