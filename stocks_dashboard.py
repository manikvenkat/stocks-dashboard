import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas_datareader.data as web
import pandas_datareader as data_reader
from datetime import datetime
from dash.dependencies import Input, Output, State
import dash_auth

USERNAME_PASSWORD_PAIRS = [['username','password'],['manik','hero']]

nsdq = data_reader.nasdaq_trader.get_nasdaq_symbols()
options = []
for tic in nsdq.index:
    options.append({'label': '{} {}'.format(tic, nsdq.loc[tic]['Security Name']), 'value': tic})

app = dash.Dash()
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Select stock symbols:', style={'paddingRight': '30px'}),
        dcc.Dropdown(
            id='my_ticker_symbol',
            options=options,
            value=['TSLA'],
            multi=True
        )
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%'}),
    html.Div([
        html.H3('Select start and end dates:'),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2018, 1, 1),
            end_date=datetime.today()
        )
    ], style={'display': 'inline-block'}),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize': 24, 'marginLeft': '30px'}
        ),
    ], style={'display': 'inline-block'}),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1, 2], 'y': [3, 1]}
            ]
        }
    )
])


@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
     State('my_date_picker', 'start_date'),
     State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic, start = start, end = end, data_source = 'yahoo')
        traces.append({'x': df.index, 'y': df.Close, 'name': tic})
    fig = {
        'data': traces,
        'layout': {'title': ', '.join(stock_ticker) + ' Closing Prices'}
    }
    return fig


if __name__ == '__main__':
    app.run_server()
