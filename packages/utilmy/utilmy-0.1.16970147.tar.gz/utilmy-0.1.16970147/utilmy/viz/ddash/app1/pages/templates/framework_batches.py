import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__, '/k8s-framework')

CONTENT_STYLE = {
    "margin-left": "10rem",
    "margin-right": "2rem",
    "padding": "2rem 2rem",
    "position": "fixed"
}

DAY_OPTIONS=[
          {'label': 'Today', 'value': 0},
          {'label': 'Yesterday', 'value': 1},
          {'label': '2 days ago', 'value': 2},
          {'label': '3 days ago', 'value': 3},
          {'label': '4 days ago', 'value': 4},
          {'label': '5 days ago', 'value': 5},
          {'label': '6 days ago', 'value': 6},
          {'label': '7 days ago', 'value': 7}
        ]

layout = dbc.Container(
  children=[
    dbc.Row([
      dbc.Col([
        html.B('K8S Frameoworks status'),
        html.Br(),
        html.Br()
      ], width = 8 )
    ]),
    dbc.Row([
      dbc.Col([
        html.Label('Select Days :'),
        dcc.Dropdown(
          options=DAY_OPTIONS,
          value=DAY_OPTIONS[0]['value'],
          id='days-dropdown'
        )
      ], width = 8 )
    ]),
    dbc.Row([
      dbc.Col([
        html.Br(),
        html.Div([
          html.Div(id='days-dropdown-output')
        ])
      ])
    ]),
    html.Hr(),
    html.Br(),
    html.B('Workers status'),
    html.Div(id='workers-table-output')
  ],
  class_name="content"
)