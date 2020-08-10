import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
import dash_table


tab_2_layout = html.Div(id='tab2-lyt', style={'color': 'white'},
                        children=[
                            dcc.Dropdown(
                                id='demo-dropdown',
                                options=[
                                    {'label': 'MA crossover', 'value': 'MA'},
                                    {'label': 'Montreal', 'value': 'MTL'},
                                    {'label': 'Select a strategy or upload one',
                                        'value': 'default'}
                                ],
                                value='default',
                                # style={'height': '30px', 'width': '100px',
                                #        'background': 'green'}
                            ),
                            # dbc.DropdownMenu(
                            #     [
                            #         dbc.DropdownMenuItem(
                            #             "MA crossover", id="MA"),
                            #         dbc.DropdownMenuItem(
                            #             "San Francisco", id="SF"),
                            #     ], label="San Francisco", id='demo-dropdown'),
                            # dcc.Dropdown(
                            #     id='linecandle-dropdown',
                            #     options=[
                            #         {'label': 'Line',
                            #             'value':  '001'},
                            #         {'label': 'Candle', 'value': '010'},
                            #         {'label': 'ohc',
                            #             'value': '100'}
                            #     ],
                            #     value='001',
                            #     searchable=False,
                            #     multi=False
                            # ),
                            html.Div(id='dd-output-container'),


                            html.Div(id='figdiv', style={'display': 'none'},
                                     children=dcc.Graph(
                                id="graph_close"
                            )),
                            html.Div(id='perf-table')
],
    className="six columns")
