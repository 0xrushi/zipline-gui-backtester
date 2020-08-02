import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt


tab_2_layout = html.Div(id='tab2-lyt',
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
                                value='001'
                            ),
                            html.Div(id='dd-output-container'),



                            dcc.Graph(
                                id="graph_close",
                            )
                        ],
                        className="six columns")
