import os
import json
from datetime import datetime
import threading

from alpha_vantage.timeseries import TimeSeries

# TODO Put the API key inside config file
API_KEY = 'WVACBBNC78SCCTUB'


def get_daily(symbol):
    """
    Returns the daily stock info of a symbol
    
    Arguments:
        symbol {str} -- Symbol of the stock
    """
    try:
        data = _load_daily_data(symbol)
    except:
        return None

    return data


def _load_daily_data(symbol):

    file_name = "{}_daily.json".format(symbol)
    file_path = "stock_data/{}".format(file_name)
    # Check if we already have the symbol information
    # TODO Make a special folder/path for the files
    if os.path.isfile(file_path):
        # File exists, load it and check if it's up to date
        with open(file_path) as json_file:
            symbol_json = json.load(json_file)

        update_date = symbol_json['update_date']
        update_date = datetime.strptime(update_date, '%d-%m-%Y')
        today = datetime.now()
        today = datetime(today.year, today.month, today.day)
        if update_date < today:
            print("{} - Updating {} file".format(__name__, file_name))
            symbol_json = _update_symbol_file(symbol)
            data = symbol_json['data']
        else:
            print("{} - Retrieving data from {} file".format(__name__, file_name))
            data = symbol_json['data']
    else:
        print("{} - Creating {} file".format(__name__, file_name))
        symbol_json = _update_symbol_file(symbol)
        data = symbol_json['data']

    return data

def _update_symbol_file(symbol):
        data, _ = TimeSeries(key=API_KEY, output_format='json').get_daily(symbol=symbol, outputsize='full')

        thread = threading.Thread(target = _update_symbol_file_aux, args=(symbol, data))
        thread.start()

        return data

def _update_symbol_file_aux(symbol, data):
    file_name = "{}_daily.json".format(symbol)
    file_path = "stock_data/{}".format(file_name)

    symbol_data = {
        'update_date': datetime.now().strftime('%d-%m-%Y'),
        'data': data
    }

    with open(file_path, 'w') as json_file:
        json.dump(symbol_data, json_file)
