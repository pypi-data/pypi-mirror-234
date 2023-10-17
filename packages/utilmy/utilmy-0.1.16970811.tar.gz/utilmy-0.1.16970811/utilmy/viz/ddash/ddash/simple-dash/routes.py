
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL

from app import app

from pages.hdfs_viewer import hdfs_viewer
from pages.nohit_explorer import WWQnohit_content
from pages.nosos_viewer import viewer
from pages.ca_targeting_qa import ca_qa_content
from pages.yarn_apps import viewer as yarn_viewer

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
    )
def render_page_content(pathname):
    if pathname == "/":
        content = html.P("A secret place for YAW WWQ projects")
    elif pathname == '/hdfs':
        content = hdfs_viewer
    elif pathname == '/WWQ-nohit':
        content = WWQnohit_content
    elif pathname == '/nosos-viewer':
        content = viewer
    elif pathname == '/cadev':
        content = ca_qa_content
    elif pathname == '/yarn':
        content = yarn_viewer
    else:
        content = dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
    return content