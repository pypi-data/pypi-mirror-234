import dash
# import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from flask import request

#APP resource
from ng_word import ng_table
from urlx_limited_word import urlx_limited_table

app = dash.Dash(title='HelloWorld', external_stylesheets=[dbc.themes.BOOTSTRAP])
# title is the title on html title

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "10rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "10rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H5("YAW-WWQ"),
        html.Hr(),
        # html.P(
        #     "A simple sidebar layout with navigation links", className="lead"
        # ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

sidebar_devs = html.Div(
    [
        html.H5("YAW-WWQ"),
        html.Hr(),
        # html.P(
        #     "A simple sidebar layout with navigation links", className="lead"
        # ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("NG words", href="/ng-table", active="exact"),
                dbc.NavLink("urlx-limit", href="/urlx-limited-table", active="exact"),
                dbc.NavLink("Secret", href="/secret", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

dynamic_sidebar = html.Div(id='dynamic-sidebar'
, style=SIDEBAR_STYLE
)

content = html.Div(id="page-content"
, style=CONTENT_STYLE
)

app.layout = html.Div([dcc.Location(id="url"), dynamic_sidebar, content])

def get_secret_body():
    import datetime
    return html.Div([
        html.P('this is secret'),
        html.P(f'{request.host_url} {request.url_root} {request.host} {request.args.get("language")}'),
        html.P(f'{request.get_json()["inputs"]}'),
        html.P(f'{datetime.datetime.utcnow()}')
    ])

@app.callback(
    Output('dynamic-sidebar', 'children'),
    Output("page-content", "children"),
    Input("url", "pathname")
    )
def render_page_content(pathname):
    is_dev = False
    is_dev = request.host == 'ddddd:8880'
    # for inputs in request.get_json()["inputs"]:
    #     if (inputs['id'] == 'url') & (inputs['value'] == '/page-2'):
    #         is_dev = True

    if is_dev:
        dynamic_sidebar = sidebar_devs
    else:
        dynamic_sidebar = sidebar
    if pathname == "/":
        content = html.P("A secret place for YAW WWQ projects")
    elif pathname == "/ng-table":
        content = ng_table
    elif pathname == "/urlx-limited-table":
        content = urlx_limited_table
    elif pathname == '/secret':
        content = get_secret_body()
    # If the user tries to reach a different page, return a 404 message
    else:
        content = dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
    return dynamic_sidebar, content

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8880)