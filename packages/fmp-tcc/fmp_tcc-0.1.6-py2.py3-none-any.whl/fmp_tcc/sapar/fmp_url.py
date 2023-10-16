try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json

def get_data_url(url): #Get data using API link - NOT fmpsdk lib
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    data = json.loads(data)
    return data