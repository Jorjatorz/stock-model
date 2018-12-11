from alpha_vantage.timeseries import TimeSeries

# TODO Put the API key inside config file
API_KEY = 'WVACBBNC78SCCTUB'


def get_daily(symbol, full = False, format = 'pandas'):
    """
    Returns the daily stock info of a symbol
    
    Arguments:
        symbol {str} -- Symbol of the stock
    
    Keyword Arguments:
        full {bool} -- If True returns the full stock history. If not, only the last 100 elements (default: {False})
    """
    try:
        data, _ = TimeSeries(key=API_KEY, output_format=format).get_daily(symbol=symbol, outputsize='full' if full else 'compact')
    except:
        return None

    return data