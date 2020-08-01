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

from tabs.tab1 import tab_1_layout
from tabs.tab2 import tab_2_layout

UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()


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
@app.callback(
    Output('graph_close', 'figure'),
    # Button: switch to Tab 2
    [Input("tabs", "active_tab")],
    [State("intermediate-value", "children")]
)
def update_fig(n_clicks, input_value):
    if n_clicks is not None:
        # df = get_historical_data(input_value, start=start, end=end, output_format="pandas")
        #df = pd.read_csv("aapl.csv")
        #df = pd.read_csv(input_value)
        df = pd.read_json(input_value, orient='split')

        print(df)

        trace_line = go.Scatter(x=list(df.date),
                                y=list(df.close),
                                # visible=False,
                                name="Close",
                                showlegend=False)

        trace_candle = go.Candlestick(x=df.date,
                                      open=df.open,
                                      high=df.high,
                                      low=df.low,
                                      close=df.close,
                                      # increasing=dict(line=dict(color="#00ff00")),
                                      # decreasing=dict(line=dict(color="white")),
                                      visible=False,
                                      showlegend=False)

        trace_bar = go.Ohlc(x=df.date,
                            open=df.open,
                            high=df.high,
                            low=df.low,
                            close=df.close,
                            # increasing=dict(line=dict(color="#888888")),
                            # decreasing=dict(line=dict(color="#888888")),
                            visible=False,
                            showlegend=False)

        data = [trace_line, trace_candle, trace_bar]

        updatemenus = list([
            dict(
                buttons=list([
                    dict(
                        args=[{'visible': [True, False, False]}],
                        label='Line',
                        method='update'
                    ),
                    dict(
                        args=[{'visible': [False, True, False]}],
                        label='Candle',
                        method='update'
                    ),
                    dict(
                        args=[{'visible': [False, False, True]}],
                        label='Bar',
                        method='update'
                    ),
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

        return {
            "data": data,
            "layout": layout
        }


pre_style = {
    'whiteSpace': 'pre-wrap',
    'wordBreak': 'break-all',
    'whiteSpace': 'normal'
}


# @app.callback(Output('output-data-upload', 'children'),
@app.callback(Output('intermediate-value', 'children'),
              [Input('upload-data', 'contents')])
def update_output(contents):
    if contents is not None:
        # print(contents)
        content_type, content_string = contents.split(',')
        content_string = base64.b64decode(content_string).decode('utf-8')
        # print(content_string)
        if 'csv' in content_type:
            #df = pd.read_csv(io.StringIO(content_string))
            cleaned_df = pd.read_csv(io.StringIO(content_string))
            return cleaned_df.to_json(date_format='iso', orient='split')
            # return "content_string"
    return


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output_dd(value):
    return 'You have selected "{}"'.format(value)


if __name__ == "__main__":
    app.run_server(debug=True, port=5001)
