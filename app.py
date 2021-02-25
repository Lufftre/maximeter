import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.subplots
from dash.dependencies import Input, Output
from db import Session
from garmin.gnd10 import read_messages3
from queue import Queue
import datetime
import logging
import multiprocessing
logging.basicConfig(level='DEBUG')
q = multiprocessing.Queue()
p = multiprocessing.Process(target=read_messages3, args=(q,))
p.start()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1000,
            n_intervals=0
        )
    ])
)
data = {
    'time': [],
    'Boat Speed': [],
    'Wind Speed': [],
}

@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    c = 0
    # for i in range(5):
    while not q.empty() and c < 10:
        logging.debug('GET: %s', q.qsize())
        c += 1
        p = q.get_nowait()
        logging.debug(p)
        data['time'] += [p['time']]
        data['Boat Speed'] += [p['boat_speed']]
        data['Wind Speed'] += [p['wind_speed']]

    data['time'] = data['time'][-100:]
    data['Boat Speed'] = data['Boat Speed'][-100:]
    data['Wind Speed'] = data['Wind Speed'][-100:]
    fig = plotly.subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    # fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data['Boat Speed'],
        'name': 'Boat Speed',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['time'],
        'y': data['Wind Speed'],
        'name': 'Wind Speed',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
