import logging

import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL

import humanize
import datetime
import pandas as pd

from yarn_api_client import ResourceManager



from app import app

yarn_endpoints = {
    'JPW1-C6000-PRO': 'http://hdp-rm6001.haas.jpw1a.dcnw.yyyyy:8088',
    'JPE2-C6000-PRO': 'http://hdp-rm6001.haas.jpe2b.dcnw.yyyyy:8088',
    'JPC1-C6000-PRO': 'http://hdp-rm6001.haas.jpc1a.dcnw.yyyyy:8088',

    # 'ECDC-C6000-PRO': 'http://hdp-rm6001.prod.iad1.bdd.local:8088',

    'JPE1-C4000-PRO': 'http://bhdprm4002.prod.hnd1.bdd.local:8088',
}

def get_pppppp_running_apps():
    running_apps = []
    for cluster_name, endpoint in yarn_endpoints.items():
        rm = ResourceManager([endpoint])
        res = rm.cluster_applications(states=['RUNNING'], user='pppppp')
        for _ in res.data.get('apps', {}).get('app', []):
            app = {k: v for k, v in _.items() if k in ['queue', 'name', 'elapsedTime']}
            if 'long' in app['queue']:
                continue
            app['cluster'] = cluster_name
            app['elapsedTime'] = humanize.precisedelta(
                datetime.timedelta(milliseconds=app['elapsedTime']),
                minimum_unit='seconds'
            )
            running_apps.append(app)
    return running_apps


def get_app_df():
    apps = get_pppppp_running_apps()
    return pd.DataFrame(apps)

viewer = html.Div(
    [
        html.H5('Running Apps on Yarn'),
        html.Hr(),
        html.Div(id='yarn-running-apps-content'),
        dcc.Interval(
            id='interval-component-yarn',
            interval=15*1000, # in milliseconds
            n_intervals=0
        ),
    ]
)

@app.callback(
    Output('yarn-running-apps-content', 'children'),
    [Input('interval-component-yarn', 'n_intervals'),
    ],
)
def render_job_content(n):
    df = get_app_df()
    if df.empty:
        return None
    df.sort_values('cluster', inplace=True)
    return html.Div([
            dash_table.DataTable(
                id='yarn-running-apps-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                filter_action='native',
                sort_action="native",
                sort_mode=None,
                row_selectable='multi',
                column_selectable='multi',
                style_table = {'minWidth': '100%', 'overflowY': 'auto'},
                style_as_list_view=False,
                style_cell={'textAlign': 'left'},
                fixed_columns={'headers': True, 'data': 1},
                )
            ],
            style = {'marginLeft': '1rem', 'marginRight': '1rem'}
        )
