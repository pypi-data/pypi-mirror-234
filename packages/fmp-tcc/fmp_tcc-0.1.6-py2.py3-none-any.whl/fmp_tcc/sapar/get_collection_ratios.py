import pandas as pd

# import fmpsdk
from ..courtois.fmp_url import get_data_url
from get_collection_fs import calculate_years, calculate_months, get_fs_some

from datetime import datetime
from dateutil.relativedelta import relativedelta

# def get_ratios_fmp(apikey: str, symbol: str, period: str='annual', limit: int=10):
#     url = (f'https://financialmodelingprep.com/api/v3/ratios/{symbol}?period={period}&limit={limit}&apikey={apikey}')
#     data = get_data_url(url=url)
#     return data

def get_ratios(apikey: str, ticks: list, period: str = 'annual', 
           with_progress: bool = False, ratios=[], start_date: str= "N/A"):
    
    if start_date == "N/A":
        limit = 100;
    else:
        if period == "annual":
            limit = calculate_years(start_date=start_date) + 1;
        elif period == "quarter":
            limit = calculate_months(start_date=start_date) // 3 + 1;
        else:
            print("The period should be either 'annual' or 'quarter' ");
            return False;

    if (ratios == []):
        attributes_ratios = ['symbol', 'date', 
                             'daysOfSalesOutstanding', 'daysOfInventoryOutstanding', 'daysOfPayablesOutstanding',
                             'cashConversionCycle', 'cashRatio', 
                             'grossProfitMargin', 'inventoryTurnover', 'freeCashFlowPerShare']
    else:
        attributes_ratios = set(ratios);
        attributes_ratios.add('date');
        attributes_ratios.add('symbol');
        attributes_ratios = list(attributes_ratios);

    data_frames = []

    if with_progress:
        i = 0;
        n = len(ticks);

    for ticker in ticks:

        if with_progress:
            i += 1;

        ticker_ratios = get_fs_some(apikey=apikey, symbol=ticker, period=period, limit=limit, finance='ratios')

        if ((ticker_ratios == [])):
            continue

        if ((type(ticker_ratios) == dict) and (ticker_ratios.get('status', '') == 404)):
            continue

        data_ratios = pd.DataFrame(ticker_ratios)
        

        data_ratios = data_ratios[list(set(attributes_ratios).intersection(set(list(data_ratios.columns))))]
        if (('symbol' not in list(data_ratios.columns)) or ('date' not in list(data_ratios.columns))):
            continue
        data_ratios.drop_duplicates(subset=['symbol', 'date'], inplace=True)
        data_ratios.set_index(['symbol', 'date'], inplace=True)

        try:

            data_frames.append(data_ratios)

            if with_progress:
                print(f"With ticker (fs) -- {ticker} : {str(i)} / {str(n)} with limit -- {str(limit)} ")

        except:
            continue;
    
    # print(data_frames)

    if start_date == "N/A":
        df = pd.concat(data_frames)
    else:
        df = pd.concat(data_frames)
        df.reset_index(inplace=True)

        df = df[df['date'] >= start_date]

        df.set_index(['symbol', 'date'], inplace=True)

    return df