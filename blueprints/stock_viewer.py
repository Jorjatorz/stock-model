from flask import Blueprint, render_template, request, Response
import json
import plotly, plotly.graph_objs
from model.stock_data_getter.stock_data_getter import get_daily

stock_viewer_blueprint = Blueprint('stock-viewer', __name__)

@stock_viewer_blueprint.route('/stock-viewer/')
def index():
    return render_template('stock_viewer.html')

@stock_viewer_blueprint.route('/stock_data/', methods=['GET'])
def get_symbol_daily():
    symbol = request.args.get('symbol')
    graph_format = request.args.get('format')
    if symbol and graph_format:
        data = get_daily(symbol, format='json')
        if data is not None:
            if graph_format == 'line':
                trace = plotly.graph_objs.Scatter(
                    x = list(data.keys()),
                    y = [elem['4. close'] for elem in data.values()],
                    mode = 'lines'
                )
            return Response(json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder), mimetype='application/json')
        else:
            return Response("Symbol not found", status=404)
    else:
        return Response("Error: symbol or graph_format empty", status=500)