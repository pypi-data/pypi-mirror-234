from ..courtois.fmp_url import get_data_url

from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_exchange(apikey: str='apikey', exchange: str='EURUSD', start_date: str= "2023-10-01", end_date: str='2023-10-04'):
    url = (f"https://financialmodelingprep.com/api/v3/historical-price-full/{exchange}?from={start_date}&to={end_date}&apikey={apikey}")
    data = get_data_url(url=url)
    return data