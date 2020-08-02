import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from datetime import datetime as dt
import dash_html_components as html
from dash.dependencies import Output, Input, State
from iexfinance.stocks import get_historical_data
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import datetime
import pandas as pd
import requests
import os
import dash_table
import base64
import io
import pandas as pd

from tabs.tab1 import tab_1_layout
from tabs.tab2 import tab_2_layout

import numpy as np
import pandas as pd
import zipline
from yahoofinancials import YahooFinancials
import warnings
import pandas_datareader as pdr
from zipline.api import order, record, symbol, set_benchmark
import zipline
import pytz
from scripts.get_from_pdr_to_panel import get_from_pdr_to_panel
from zipline.api import order, record, symbol, set_benchmark
import zipline
from datetime import datetime
import pytz
import json

UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


start = datetime.today() - relativedelta(years=5)
end = datetime.today()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions'] = False

app.layout = html.Div([
    html.Div([
        html.H2("Stock App"),
        # html.Img(src="/assets/stock-icon.png")
    ], className="banner"),

    html.Div([
        dbc.Tabs(id='tabs', children=[
            dbc.Tab(tab_1_layout, tab_id='tab1id', label='Tab one'),
            dbc.Tab(tab_2_layout, tab_id='tab2id', label='Tab two'),
        ], active_tab="tab1id"),
        html.Div(id='tab-content')
    ]),

    html.Div(id='intermediate-value', children=['<p>intermediate</p>'])
])

# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })


@app.callback(
    # Button: switch to Tab 2
    Output("tabs", "active_tab"),
    [Input("tab1_btn_submit", "n_clicks")]
)
def tab_resources(click):
    if click:
        return "tab2id"
    else:
        return "tab1id"


# @app.callback(
#     Output('graph_close', 'figure'),
#     [Input("tab1_btn_submit", "n_clicks")],
#     # [State('intermediate-value', 'children')]
# )


# @app.callback(
#     Output('tab2-lyt', 'children'),
#     # Button: switch to Tab 2
#     [Input("tabs", "active_tab")],
#     [State("intermediate-value", "children")]
# )
# def update_fig(n_clicks, input_value):
#     if n_clicks is not None:
#         # parsed = json.loads(input_value)
#         # df=pd.read_csv(input_value)
#         print(input_value)
#         print(type(input_value))
#         df = pd.read_json(input_value, orient='records')
#         # df=pd.DataFrame(json.loads(str(df)))
#         # print(df)
#         panel = get_from_pdr_to_panel()  # nvidia

#         def initialize(context):
#             pass

#         def handle_data(context, data):
#             todays_pr = data.current(symbol('NVDA'), 'price')
#             diff = context.portfolio.cash - todays_pr

#             hist = data.history(symbol('NVDA'), 'price', 35, '1d')
#             sma_35 = hist.mean()
#             sma_5 = hist[-5:].mean()
#             # print(hist)
#             record(sma_35=sma_35)
#             record(sma_5=sma_5)
#             record(NVDA=todays_pr)

#             if diff > 0:
#                 # Trading logic
#                 if sma_5 > sma_35:
#                     # order_target orders as many shares as needed to
#                     # achieve the desired number of shares.
#                     order(symbol("NVDA"), 2)
#                 elif sma_5 < sma_35:
#                     order(symbol("NVDA"), -2)

#         perf = zipline.run_algorithm(start=datetime(2016, 2, 24, 0, 0, 0, 0, pytz.utc),
#                                      end=datetime(2017, 12, 29, 0,
#                                                   0, 0, 0, pytz.utc),
#                                      initialize=initialize,
#                                      capital_base=100,
#                                      handle_data=handle_data,
#                                      data=panel)
#         perf.plots = [go.Scatter(x=perf.index, y=perf.sma_35, mode='lines', name="sma_35"),
#                       go.Scatter(x=perf.index, y=perf.sma_5,
#                                  mode='lines', name="sma_5")
#                       ]

#         # print(perf)
#         # trace_line = go.Scatter(x=list(df.date),
#         #                         y=list(df.close),
#         #                         # visible=False,
#         #                         name="Close",
#         #                         showlegend=False)
#         # updatemenus = list([
#         #     dict(
#         #         buttons=list([
#         #             dict(
#         #                 args=[{'visible': [True, False, False]}],
#         #                 label='Line',
#         #                 method='update'
#         #             ),
#         #             dict(
#         #                 args=[{'visible': [False, True, False]}],
#         #                 label='Candle',
#         #                 method='update'
#         #             ),
#         #             dict(
#         #                 args=[{'visible': [False, False, True]}],
#         #                 label='Bar',
#         #                 method='update'
#         #             ),
#         #         ]),
#         #         direction='down',
#         #         pad={'r': 10, 't': 10},
#         #         showactive=True,
#         #         x=0,
#         #         xanchor='left',
#         #         y=1.05,
#         #         yanchor='top'
#         #     ),
#         # ])

#         layout = dict(
#             title="hello",
#             # updatemenus=updatemenus,
#             autosize=False,
#             xaxis=dict(
#                 rangeselector=dict(
#                     buttons=list([
#                         dict(count=1,
#                              label='1m',
#                              step='month',
#                              stepmode='backward'),
#                         dict(count=6,
#                              label='6m',
#                              step='month',
#                              stepmode='backward'),
#                         dict(count=1,
#                              label='YTD',
#                              step='year',
#                              stepmode='todate'),
#                         dict(count=1,
#                              label='1y',
#                              step='year',
#                              stepmode='backward'),
#                         dict(step='all')
#                     ])
#                 ),
#                 rangeslider=dict(
#                     visible=True
#                 ),
#                 type='date'
#             )
#         )

#         trace_line = go.Figure(layout=layout)
#         trace_line.add_scatter(x=perf.index, y=perf.NVDA,
#                                mode='lines', name="NVDA")
#         for i in perf.plots:
#             trace_line.add_trace(i)

#         # return dcc.Graph(
#         #     id="graph_close",
#         #     figure=go.Figure(trace_line)
#         # )

#         trace_candle = go.Figure(layout=layout)
#         trace_candle.add_trace(go.Candlestick(x=df.date,
#                                               open=df.open,
#                                               high=df.high,
#                                               low=df.low,
#                                               close=df.close,
#                                               # increasing=dict(line=dict(color="#00ff00")),
#                                               # decreasing=dict(line=dict(color="white")),
#                                               visible=True,
#                                               showlegend=False)
#                                )
#         for i in perf.plots:
#             trace_candle.add_trace(i)

#         # return trace_candle

#         trace_bar = go.Figure(layout=layout)
#         trace_bar .add_trace(go.Ohlc(x=df.date,
#                                      open=df.open,
#                                      high=df.high,
#                                      low=df.low,
#                                      close=df.close,
#                                      # increasing=dict(line=dict(color="#888888")),
#                                      # decreasing=dict(line=dict(color="#888888")),
#                                      visible=False,
#                                      showlegend=False))
#         for i in perf.plots:
#             trace_bar.add_trace(i)

#         data = [trace_line, trace_candle, trace_bar]

#         return dcc.Graph(
#             id="graph_close",
#             figure=trace_line
#         )


@app.callback(
    Output('tab2-lyt', 'children'),
    [Input("linecandle-dropdown", "value")],
    [State("intermediate-value", "children")]
)
def update_fig2(nval, input_value):
    print(input_value)
    print(type(input_value))
    df = pd.read_json(input_value, orient='records')
    # df=pd.DataFrame(json.loads(str(df)))
    # print(df)
    panel = get_from_pdr_to_panel()  # nvidia

    def initialize(context):
        pass

    def handle_data(context, data):
        todays_pr = data.current(symbol('NVDA'), 'price')
        diff = context.portfolio.cash - todays_pr

        hist = data.history(symbol('NVDA'), 'price', 35, '1d')
        sma_35 = hist.mean()
        sma_5 = hist[-5:].mean()
        # print(hist)
        record(sma_35=sma_35)
        record(sma_5=sma_5)
        record(NVDA=todays_pr)

        if diff > 0:
            # Trading logic
            if sma_5 > sma_35:
                # order_target orders as many shares as needed to
                # achieve the desired number of shares.
                order(symbol("NVDA"), 2)
            elif sma_5 < sma_35:
                order(symbol("NVDA"), -2)

    perf = zipline.run_algorithm(start=datetime(2016, 2, 24, 0, 0, 0, 0, pytz.utc),
                                 end=datetime(2017, 12, 29, 0,
                                              0, 0, 0, pytz.utc),
                                 initialize=initialize,
                                 capital_base=100,
                                 handle_data=handle_data,
                                 data=panel)
    perf.plots = [go.Scatter(x=perf.index, y=perf.sma_35, mode='lines', name="sma_35"),
                  go.Scatter(x=perf.index, y=perf.sma_5,
                             mode='lines', name="sma_5")
                  ]

    layout = dict(
        title="hello",
        # updatemenus=updatemenus,
        autosize=False,
        width=2000,
        height=500,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )

    trace_line = go.Figure(layout=layout)
    trace_line.add_scatter(x=perf.index, y=perf.NVDA,
                           mode='lines', name="NVDA")
    for i in perf.plots:
        trace_line.add_trace(i)

    # return dcc.Graph(
    #     id="graph_close",
    #     figure=go.Figure(trace_line)
    # )

    trace_candle = go.Figure(layout=layout)
    trace_candle.add_trace(go.Candlestick(x=df.date,
                                          open=df.open,
                                          high=df.high,
                                          low=df.low,
                                          close=df.close,
                                          # increasing=dict(line=dict(color="#00ff00")),
                                          # decreasing=dict(line=dict(color="white")),
                                          visible=True,
                                          showlegend=False)
                           )
    for i in perf.plots:
        trace_candle.add_trace(i)

    # return trace_candle

    trace_bar = go.Figure(layout=layout)
    trace_bar .add_trace(go.Ohlc(x=df.date,
                                 open=df.open,
                                 high=df.high,
                                 low=df.low,
                                 close=df.close,
                                 # increasing=dict(line=dict(color="#888888")),
                                 # decreasing=dict(line=dict(color="#888888")),
                                 visible=False,
                                 showlegend=False))
    for i in perf.plots:
        trace_bar.add_trace(i)

    data = [trace_line, trace_candle, trace_bar]
    if nval == '001':
        ffig = data[0]
    elif nval == '010':
        ffig = data[1]
    elif nval == '100':
        ffig = data[2]

    print("nval "+str(nval))

    return html.Div(id='tab2-lyt',
                    children=[
                        dcc.Dropdown(
                            id='demo-dropdown',
                            options=[
                                {'label': 'MA crossover', 'value': 'MA'},
                                {'label': 'Montreal', 'value': 'MTL'},
                                {'label': 'San Francisco', 'value': 'SF'}
                            ],
                            value='SF'
                        ),
                        dcc.Dropdown(
                            id='linecandle-dropdown',
                            options=[
                                {'label': 'Line',
                                 'value':  '001'},
                                {'label': 'Candle', 'value': '010'},
                                {'label': 'ohc',
                                 'value': '100'}
                            ],
                            value=nval
                        ),
                        html.Div(id='dd-output-container'),



                        dcc.Graph(
                            id="graph_close",
                            figure=ffig
                        )
                    ],
                    className="six columns")


pre_style = {
    'whiteSpace': 'pre-wrap',
    'wordBreak': 'break-all',
    'whiteSpace': 'normal'


}


# @app.callback(Output('output-data-upload', 'children'),
@ app.callback(Output('intermediate-value', 'children'),
               [Input('upload-data', 'contents')])
def update_output(contents):
    if contents is not None:
        # print(contents)
        content_type, content_string = contents.split(',')
        content_string = base64.b64decode(content_string).decode('utf-8')
        # print(content_string)
        if 'csv' in content_type:
            # df = pd.read_csv(io.StringIO(content_string))
            cleaned_df = pd.read_csv(io.StringIO(content_string))
            return cleaned_df.to_json(date_format='iso', orient='records')
            # return "content_string"
    return


@ app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output_dd(value):
    return 'You have selected "{}"'.format(value)


if __name__ == "__main__":
    app.run_server(debug=True, port=5001)
