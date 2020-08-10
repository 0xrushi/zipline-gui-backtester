import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt


datepicker_input = dbc.FormGroup(
    [
        dbc.Label("DateRange  ", html_for="datepickerinp", width=3),
        dbc.Col(
            dcc.DatePickerRange(
                end_date=dt(2017, 6, 21, 23,
                            59, 59, 999999),
                display_format='MMM Do, YY',
                start_date_placeholder_text='MMM Do, YY', id='datepickerinp',
            ),
            width=8)], row=True, className='datepickker-input')

stock_name_inp = dbc.FormGroup(
    [dbc.Label("Ticker ", width=3),
     dbc.Col(dbc.Input(placeholder="TickerName...", type="text"), width=8)], row=True)

fileupload_input = dbc.FormGroup(
    [dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]), style={
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
        }),
     html.Div(id='output-data-upload'),
     ]
)

btn = dbc.Button("Submit", color="primary", id="tab1_btn_submit", style={
    "width": "200px",
    "margin": "0 auto",
    "display": "block"})

form = dbc.Form([datepicker_input, stock_name_inp, fileupload_input, btn],
                id="example-form")


tab_1_layout = html.Div([
    html.H3('Tab content 2'),
    form
])

card_content_1 = [
    dbc.CardBody(
        [
            form
        ], className="co-md-4"
    ),
]
tab_1_layout = dbc.Card(card_content_1, color="#222831",
                        inverse=False, className='card-class-dark')
