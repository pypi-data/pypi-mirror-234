import pandas as pd

# import fmpsdk

# try:
#     # For Python 3.0 and later
#     from urllib.request import urlopen
# except ImportError:
#     # Fall back to Python 2's urllib2
#     from urllib2 import urlopen

import plotly.graph_objects as go

from ..sapar.get_collection_fs import get_fs_some
from ..sapar.get_collection_ratios import get_ratios_fmp
from fmp_url import get_data_url

def data_merge(apikey, ticker, period): # get and merge data from BSS; CFS; IS; and ratios - input period and ticker
    
    symbol: str = ticker
        
    data_BSS = pd.DataFrame(get_fs_some(apikey=apikey, symbol=symbol, period=period, finance='balance-sheet-statement'))
    data_CFS = pd.DataFrame(get_fs_some(apikey=apikey, symbol=symbol, period=period, finance='income-statement'))
    data_IS = pd.DataFrame(get_fs_some(apikey=apikey, symbol=symbol, period=period, finance='cash-flow-statement'))
    data_ratios = pd.DataFrame(get_ratios_fmp(apikey=apikey, symbol=symbol, period=period))

    data_CFS.pop('inventory')
    data_CFS.pop('netIncome')
    data_CFS.pop('depreciationAndAmortization')

    data_annual = data_BSS.copy()
    data_annual = data_annual.merge(data_CFS, how='inner', on=['date', 'cik', 'period',
                                                               'reportedCurrency', 'symbol',
                                                               'link', 'finalLink', 'fillingDate',
                                                               'acceptedDate', 'calendarYear'])
    data_annual = data_annual.merge(data_IS, how='inner', on=['date', 'cik', 'period',
                                                              'reportedCurrency', 'symbol', 'link',
                                                              'finalLink', 'fillingDate',
                                                              'acceptedDate', 'calendarYear'])
    data_annual = data_annual.merge(data_ratios, how='inner', on=['date', 'period', 'symbol'])

    return data_annual

# def get_data_url(url): #Get data using API link - NOT fmpsdk lib
#     response = urlopen(url, cafile=certifi.where())
#     data = response.read().decode("utf-8")
#     data = json.loads(data)
#     return data

def get_competitors(apikey, ticker): #Get competitors - NOT fmpsdk lib
    
    url = (f'https://financialmodelingprep.com/api/v4/stock_peers?symbol={ticker}&apikey={apikey}')
    
    data = get_data_url(url)
    return data[0]['peersList']

def average_calc(apikey, ticker, field, period): #input a value and return avg competitors - NOT fmpsdk lib
    competitors = get_competitors(ticker)
    
    df_rtr = pd.DataFrame()
    for comp in competitors:
        try:
            data_comp = data_merge(apikey, comp, period)
            data_comp = data_comp[['calendarYear', 'period', field]]
            df_rtr = pd.concat([df_rtr, data_comp], ignore_index=True)
        except:
            pass
        
    averaged_df = df_rtr.groupby('calendarYear')[field].mean().reset_index()

    return averaged_df

def format_string(input_string):
    formatted_string = ''
    for char in input_string:
        if char.isupper():
            formatted_string += ' '
        formatted_string += char
    formatted_string = formatted_string.replace('_', ' ')
    formatted_string = formatted_string.strip()
    formatted_string = formatted_string.title()
    return formatted_string

def line_graph(field,data):
    x_values=data['date']
    y_values=data[field]
    
    trace = go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines',
    name='Line Graph'
    )
    
    layout = go.Layout(
    title='Line Graph Example',
    xaxis=dict(title='date'),
    yaxis=dict(title=format_string(field))
    )
    
    return go.Figure(data=[trace], layout=layout)