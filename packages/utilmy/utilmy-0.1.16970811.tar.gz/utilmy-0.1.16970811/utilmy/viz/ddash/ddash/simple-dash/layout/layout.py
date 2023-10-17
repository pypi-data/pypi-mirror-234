import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "11rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "11rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H5("the UI"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("HDFS Browser", href="/hdfs", active="exact"),
                dbc.NavLink("WWQ Nohit", href="/WWQ-nohit", active="exact"),
                dbc.NavLink("nosos", href="/nosos-viewer", active="exact"),
                dbc.NavLink("CA", href="/cadev", active="exact"),
                dbc.NavLink("YARN-APPS", href="/yarn", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    id="page-content",
    style=CONTENT_STYLE
)

layout = html.Div([dcc.Location(id="url"), sidebar, content])
