import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# from get_forex_data import get_exchange_rate
from ..courtois.fmp_url import get_data_url
from .get_collection_fs import company_profile, get_fs_some

def get_exchange_rate(apikey: str='apikey', exchange: str='EURUSD', period: str='daily',\
    start_date: str= "2023-10-01", end_date: str='2023-10-04'):
    """
    params:
        apikey -- to access data from FMP;
        exchange -- required conversion from 'EUR' to 'USD';
        period -- either 'min', or 'hour', or 'daily';
    return: list of dictionaries
    """
    if period=='daily':
        url = (f"https://financialmodelingprep.com/api/v3/historical-price-full/{exchange}?from={start_date}&to={end_date}&apikey={apikey}")

    data = get_data_url(url=url)
    return data

def convert_data_to_common_currency(df, apikey: str='apikey', base: str='USD', data: str='finance', skipping=[]):
    """
    params:
        df -- data-frame numerical values of which we want to convert to commone currendy (base = 'USD')
        apikey -- to access data from FMP;
        data -- it can be either 'finance' (data of financial statement usually has data of 'reportedCurrency') or 'stock' 
            (stock data for which we need to inquire currency);
        skipping -- columns that we don't want to convert;
    return: list of dictionaries
    """
    if 'symbol' not in df.columns:
        print("We don't have the ticker data")
        return False
    else:
        tickers_df = set(df['symbol'])

    if 'currency' not in df.columns:
        df['currency'] = None
        for ticker in tickers_df:
            profile = company_profile(apikey=apikey, symbol=ticker)
            if profile != []:
                profile = profile[0]
                if 'currency' not in profile.keys():
                    if data == 'stock':
                        df.loc[df['symbol'] == ticker, 'currency'] = \
                            get_fs_some(apikey=apikey, symbol=ticker, period='quarter', limit=2)[0]['reportedCurrency']
                    elif data == 'finance':
                        if 'reportedCurrency' in df.columns:
                            df.loc[df['symbol'] == ticker, 'currency'] = df[df['symbol'] == ticker]['reportedCurrency'].mode()[0]
                    else:
                        print("We don't have reported currency information for financial data")
                        return False
                else:
                    df.loc[df['symbol'] == ticker, 'currency'] = profile['currency']


    df['currency'] = df['currency'].str.replace('ZAc', 'ZAR')
    df['currency'] = df['currency'].str.replace('ILA', 'ILS')

    if 'reportedCurrency' not in df.columns:
        df['reportedCurrency'] = None

    for i in df.index:
        if (df.loc[i, 'reportedCurrency'] != df.loc[i, 'reportedCurrency']) or (df.loc[i, 'reportedCurrency'] == None):
            df.loc[i, 'reportedCurrency'] = df.loc[i, 'currency']

    df['reportedCurrency'] = df['reportedCurrency'].str.strip()

    exchange_rate = df[['symbol', 'date']]
    exchange_rate.loc[df['reportedCurrency']==base, 'exchange_rate'] = 1

    j=0;
    ex_currendies = {}

    for i in df.index:
        if (df.loc[i, 'reportedCurrency'] == base):
            if (i%30==0):
                print(df.loc[i, 'reportedCurrency']);
        else :
            if (df.loc[i, 'reportedCurrency'], df.loc[i, 'date']) in ex_currendies.keys():
                exchange_rate.loc[i, 'exchange_rate'] = ex_currendies[(df.loc[i, 'reportedCurrency'], df.loc[i, 'date'])]
            else:
                date = datetime.strptime(df.loc[i, 'date'], '%Y-%m-%d');
                start_date = date - timedelta(days=3);
                start_date = start_date.strftime('%Y-%m-%d')
                end_date = date  + timedelta(days=4);
                end_date = end_date.strftime('%Y-%m-%d')
                x = df.loc[i, 'reportedCurrency'] + base;
                data = get_exchange_rate(apikey=apikey, exchange=x, start_date=start_date, end_date=end_date)
                data = pd.DataFrame(data["historical"])
                data['date'] = pd.to_datetime(data['date'])
                data.set_index('date', inplace=True)
                try:
                    exchange_rate.loc[i, 'exchange_rate'] =  np.nanmedian(data.loc[date, 'adjClose'])
                    ex_currendies[(df.loc[i, 'reportedCurrency'], df.loc[i, 'date'])] = exchange_rate.loc[i, 'exchange_rate']
                    print(df.loc[i, 'reportedCurrency'], df.loc[i, 'date'], i, 'try');
                except: 
                    ser = pd.to_numeric(data['adjClose'], downcast='float')
                    m = np.nanmedian(ser)
                    exchange_rate.loc[i, 'exchange_rate'] = m
                    ex_currendies[(df.loc[i, 'reportedCurrency'], df.loc[i, 'date'])] = exchange_rate.loc[i, 'exchange_rate']
                    print(df.loc[i, 'reportedCurrency'], df.loc[i, 'date'], i, 'except', m);

    df_usd = df.copy()

    skipping = list(set(skipping).union(set(['symbol', 'date', 'reportedCurrency', 'sector',\
        'industry', 'numberOfShares', 'currency', 'country'])))

    for col in df[df.columns.difference(skipping)].columns:
        df_usd[col] = df[col].mul(exchange_rate['exchange_rate'])
        # print(col)

    return df_usd