import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt


datepicker_input = dbc.FormGroup(
    [dbc.Button("Select Date Range", color="primary", className="mr-1"),
     dcc.DatePickerRange(
        end_date=dt(2017, 6, 21, 23, 59, 59, 999999),
        display_format='MMM Do, YY',
        start_date_placeholder_text='MMM Do, YY'
    )])
fileupload_input = dbc.FormGroup(
    [dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]), style={
            'width': '100%',
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

btn = dbc.Button("Submit", color="primary", id="tab1_btn_submit")

form = dbc.Form([datepicker_input, fileupload_input, btn],
                id="example-form")


tab_1_layout = html.Div([
    html.H3('Tab content 2'),
    form
])
