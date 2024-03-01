import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
import random
from itertools import chain
import math
import pytz
import businesstimedelta
from pycelonis import get_celonis
from datetime import date

def businesshrs_func():
    workday = businesstimedelta.WorkDayRule(
    start_time=dt.time(9),
    end_time=dt.time(18),
    working_days=[0, 1, 2, 3, 4])

    # Take out the lunch break
    lunchbreak = businesstimedelta.LunchTimeRule(
        start_time=dt.time(12),
        end_time=dt.time(13),
        working_days=[0, 1, 2, 3, 4])
    businesshrs = businesstimedelta.Rules([workday, lunchbreak])
    return businesshrs
businesshrs = businesshrs_func()

# Random date
def random_dates(start, end, unit='D', seed=None):
    if not seed:
        np.random.seed(0)
    ndays = (end - start).days
    return start + dt.timedelta(
        random.randint(0, ndays))

def random_dates_business(start, end):
    date = random_dates(start, end).strftime('%Y-%m-%d')
    
    while not np.is_busday(date):
        date = (pd.to_datetime(date) + dt.timedelta(days=1)).strftime('%Y-%m-%d')        
    return pd.to_datetime(date)

# Aggiungi giorni se il giorno è festivo
def dates_business(start):
    start = start.strftime('%Y-%m-%d')
    while not np.is_busday(start):
        start = (pd.to_datetime(start) + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    return pd.to_datetime(start)

def get_tables(anomaly = False, new = False):
    if anomaly == True:
        an = 'anomaly/'
    else: an = ''
    if new == True:
        an = 'NEW/'
    else: an = ''
        
    EBAN = pd.read_csv('data/latest_tab/' + an + 'EBAN.csv', dtype = {'BANFN' : str, 'BNFPO' : str, 'BSAKZ' : str, 'EBELP' : str,'EBELN' : str, 'BELNR' : str, 'PERNR' : str, 'ERNAM' : str, 'WERKS' : str})
    EBAN['BADAT'] = pd.to_datetime(EBAN['BADAT'])
    EBAN['FRGDT'] = pd.to_datetime(EBAN['FRGDT'])

    RBKP = pd.read_csv('data/latest_tab/' + an + 'RBKP.csv', dtype = {'BELNR' : str, 'LIFNR' : str})
    RBKP['BLDAT'] = pd.to_datetime(RBKP['BLDAT'])
    RBKP['BUDAT'] = pd.to_datetime(RBKP['BUDAT'])
    RBKP['BPDAT'] = pd.to_datetime(RBKP['BPDAT'])
    RBKP['BLOCK'] = pd.to_datetime(RBKP['BLOCK'])
    RBKP['RLOCK'] = pd.to_datetime(RBKP['RLOCK'])
    
    RSEG = pd.read_csv('data/latest_tab/' + an + 'RSEG.csv', dtype = {'EBELN' : str, 'MATNR' : str,'EBELP' : str, 'BELNR' : str, 'BUZEI' : str,  'BANFN' : str, 'WERKS' : str})

    EKPO = pd.read_csv('data/latest_tab/' + an + 'EKPO.csv',keep_default_na = True, dtype = {'EBELN' : str, 'EBELP' : str,
                                                                                             'MATNR' : str, 'BELNR' : str,
                                                                                             'BANFN' : object, 'BNFPO' : str,
                                                                                             'WERKS' : str, 'EKNAM' : str, 'EKRNR' : str})
    EKPO['SEDAT'] = pd.to_datetime(EKPO['SEDAT'])
    EKPO['DRDAT'] = pd.to_datetime(EKPO['DRDAT'])
    EKPO['LEWED'] = pd.to_datetime(EKPO['LEWED'])
    EKPO['ITDAT'] = pd.to_datetime(EKPO['ITDAT'])
    EKPO['LCWED'] = pd.to_datetime(EKPO['LCWED'])

    EKKO = pd.read_csv('data/latest_tab/' + an + 'EKKO.csv', dtype = {'EBELN' : str, 'ERNAM' : str,'WERKS' : str})
    EKKO['AEDAT'] = pd.to_datetime(EKKO['AEDAT'])
    
    df_materiali = pd.read_csv('data/materiali.csv', delimiter = ',', keep_default_na=False, dtype = {'MATNR' : str, 'LIFNR' : str})
    P0002 = pd.read_csv('data/P0002.csv', delimiter = ',', keep_default_na=False, dtype = {'PERNR' : str})
    
    EKDS = pd.read_csv('data/latest_tab/' + an + 'EKDS.csv', delimiter = ',', keep_default_na=True, dtype = {'EBELN' : str, 'EBELP' : str, 'BANFN' : str, 'BNFPO' : str})
    EKDS['UDATE'] = pd.to_datetime(EKDS['UDATE'])
    
    return EBAN, RBKP, RSEG, EKPO, EKKO, df_materiali, P0002, EKDS