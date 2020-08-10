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
from strategies.macrossover import TradingAlgo as maalgo

import numpy as np
import pandas as pd
import zipline
from yahoofinancials import YahooFinancials
import warnings
import pandas_datareader as pdr
from zipline.api import order, record, symbol, set_benchmark
import zipline
import pytz
from scripts.get_from_pdr_to_panel import get_from_pdr_to_panel, get_from_df_to_panel
from zipline.api import order, record, symbol, set_benchmark
import zipline
from datetime import datetime
import pytz
import json


UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# external JavaScript files
external_scripts = [
]


start = datetime.today() - relativedelta(years=5)
end = datetime.today()


app = dash.Dash(__name__, external_scripts=external_scripts,
                external_stylesheets=[dbc.themes.DARKLY])
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


@app.callback(
    [Output('graph_close', 'figure'), Output(
        'figdiv', 'style'), Output('perf-table', 'children')],
    [Input('demo-dropdown', 'value')],
    [State("intermediate-value", "children")]
)
def update_fig2(strategy_name, input_value):
    print(type(input_value))
    print(strategy_name)

    if strategy_name == "MA":
        stg = maalgo

    df = pd.read_json(input_value, orient='records')
    panel = get_from_df_to_panel(df, symbol="AAPL")
    perf = stg(panel=panel, symb="AAPL")
    # print(perf)

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'visible': [True, True, False, False]}],
                    label='Line',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, True, True]}],
                    label='Candle',
                    method='update'
                )
            ]),
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0,
            xanchor='left',
            y=1.05,
            yanchor='top'
        ),
    ])

    layout = dict(
        title="hello",
        updatemenus=updatemenus,
        autosize=False,
        width=1800,
        height=500,
        font_color='white',
        title_font_color="white",
        legend_title_font_color="white",
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

    data = [dict(
        type='line',
        x=perf.index,
        y=perf.close,
        # increasing=dict(line=dict(color="#00ff00")),
        # decreasing=dict(line=dict(color="white")),
        visible=True,
        showlegend=False
    )]

    fig = dict(data=data, layout=layout)
    fig['data'].append(
        dict(x=perf.index, y=perf.sma_35, name="35 Moving Average"))
    fig['data'].append(
        dict(x=perf.index, y=perf.sma_5, name="5 Moving Average"))

    fig['data'].append(dict(
        type="candlestick",
        x=perf.index,
        open=perf.open,
        high=perf.high,
        low=perf.low,
        close=perf.close,
        # increasing=dict(line=dict(color="#00ff00")),
        # decreasing=dict(line=dict(color="white")),
        visible=False,
        showlegend=False
    ))

    fig['data'].append(dict(x=perf.index, y=perf.close,
                            name="Moving Average2", visible=False))
    fig['layout'] = layout
    fig["layout"].update(paper_bgcolor="#21252C",
                         plot_bgcolor="#21252C", font_color='white')

    table_header = [
        html.Thead(html.Tr([html.Th(i) for i in perf.columns]))
    ]

    rows = []
    for index, row in perf.iterrows():
        rows.append(html.Tr([html.Td(row[i])
                             for i in perf.columns]))

    table_body = [html.Tbody(rows)]
    perft = dbc.Table(table_header + table_body, bordered=True)

    return fig, {'display': 'block'}, perft


pre_style = {
    'whiteSpace': 'pre-wrap',
    'wordBreak': 'break-all',
    'whiteSpace': 'normal'
}


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


# @ app.callback(
#     dash.dependencies.Output('dd-output-container', 'children'),
#     [dash.dependencies.Input('demo-dropdown', 'value')])
# def update_output_dd(value):
#     return 'You have selected "{}"'.format(value)


if __name__ == "__main__":
    app.run_server(debug=True, port=5001)
