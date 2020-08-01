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

UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

# def update_news():
#     url = "https://api.iextrading.com/1.0/stock/`market`/news/last/5"
#     r = requests.get(url)
#     json_string = r.json()

#     df = pd.DataFrame(json_string)
#     df = pd.DataFrame(df[["headline", "url"]])
#     return df


def generate_html_table(max_rows=10):

    # df = update_news()

    return html.Div(
        [
            html.Div(
                html.Table(
                    # Header
                    [html.Tr([html.Th()])]
                ),
                style={"height": "300px", "overflowY": "scroll"},
            ),
        ],
        style={"height": "100%"},)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        html.H2("Stock App"),
        # html.Img(src="/assets/stock-icon.png")
    ], className="banner"),

    html.Div([
        dcc.Input(id="stock-input", value="SPY", type="text"),
        html.Button(id="submit-button", n_clicks=0, children="Submit")
    ]),

    html.Div([
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label='Tab one', value='tab-1'),
            dcc.Tab(label='Tab two', value='tab-2'),
        ]),
        html.Div(id='tabs-example-content')
    ]),
])

# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })


@app.callback(Output('tabs-example-content', 'children'),
              [Input('tab1_btn_submit', 'n_clicks')])
def render_content(click):
    if not click:
        datepicker_input = dbc.FormGroup(
            [dbc.Button("Select Date Range", color="primary", className="mr-1"),
                dcc.DatePickerRange(
                end_date=dt(2017, 6, 21, 23, 59, 59, 999999),
                display_format='MMM Do, YY',
                start_date_placeholder_text='MMM Do, YY'
            )])
        fileupload_input = dbc.FormGroup(
            [dcc.Upload([
                'Drag and Drop or ',
                html.A('Select a File')
            ], style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center'
            })]
        )

        btn = dbc.Button("Submit", color="primary", id="tab1_btn_submit")

        form = dbc.Form([datepicker_input, fileupload_input, btn],
                        id="example-form")

        return html.Div([
            html.H3('Tab content 2'),
            form])
    else:
        return html.Div([
            dcc.Graph(
                id="graph_close",
            )
        ], className="six columns")


@ app.callback(Output('graph_close', 'figure'),
               [Input("submit-button", "n_clicks")],
               [State("stock-input", "value")]
               )
def update_fig(n_clicks, input_value):
    # df = get_historical_data(input_value, start=start, end=end, output_format="pandas")
    df = pd.read_csv("aapl.csv")
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
        title=input_value,
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


if __name__ == "__main__":
    app.run_server(debug=True, port=5001)
