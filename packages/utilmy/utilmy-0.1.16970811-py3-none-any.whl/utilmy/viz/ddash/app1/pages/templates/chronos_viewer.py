import logging

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL

import requests
import pandas as pd
import numpy as np

from app import app

def get_auth(url):
    if 'dcnw.yyyyy' in url:
        return ('nosos', 'Drilling-Tusk-Flashback8')
    return ('mesos', 'mesos1')

# Brink-Switch0-Jersey
nosos_options = dbc.Select(
    id="nosos-options",
    options=[
        {"label": "nosos-SMAD-1cloud", "value": "http://mesos-fip.YAW.jpe2b.dcnw.yyyyy:10053"},
        {"label": "nosos-SHARED-1cloud", "value": "http://mesos-fip.YAW.jpe2b.dcnw.yyyyy:10050"},
        {"label": "nosos-US-1cloud", "value": "http://mesos-fip.YAW.jpe2b.dcnw.yyyyy:10055"},
        {"label": "nosos-TEST-1cloud", "value": "http://mesos-fip.YAW.jpe2b.dcnw.yyyyy:10000"},
        {"label": "nosos-WWQCA-STG-1cloud", "value": "http://mesos-fip.YAW.jpe2b.dcnw.yyyyy:10103"},
        {"label": "(DONE)nosos-SMAD", "value": "http://zzzzzzzzz.local:10053"},
        {"label": "(DONE)nosos-SHARED", "value": "http://zzzzzzzzz.local:10050"},
        {"label": "(DONE)nosos-WWQCA-STG", "value": "http://zzzzzzzzz.local:10103"},
        {"label": "(DONE)nosos-ECDC-US", "value": "http://zzzzzzzzz.local:10055"},
        {"label": "(SKIP)nosos-WWQCA-PROD", "value": "http://zzzzzzzzz.local:10102"},
        {"label": "(SKIP)nosos-NEIL", "value": "http://zzzzzzzzz.local:10052"},
    ],
    value="http://mesos-fip.YAW.jpe2b.dcnw.yyyyy:10053"
)

def list_jobs(nosos_url):
    url = f'{nosos_url}/v1/scheduler/jobs'
    r = requests.get(url, auth=get_auth(nosos_url))
    if not r.ok:
        logging.warn(r.status_code)
        logging.warn(r.reason)
        return []
    return r.json()

def get_job_summary(nosos_url):
    url = f'{nosos_url}/v1/scheduler/jobs/summary'
    r = requests.get(url, auth=get_auth(nosos_url))
    if not r.ok:
        logging.warn(r.status_code)
        logging.warn(r.reason)
        return []
    return r.json()

def get_job_df(nosos_url):
    jobs = list_jobs(nosos_url)
    summary = get_job_summary(nosos_url)
    df_jobs = pd.DataFrame(jobs)
    df_summary = pd.DataFrame(summary['jobs'])
    drops = [c for c in ['schedule', 'parents', 'disabled'] if c in df_jobs.columns]
    df_jobs.drop(columns=drops, inplace=True)
    # print(df_jobs)
    # print(df_summary)
    df_jobs = df_jobs.merge(df_summary, on='name')
    def find_env(envs, key):
        for env in envs:
            if env['name'] == key:
                return env['value']
        else:
            return None
    df_jobs['monitor_flag'] = df_jobs['environmentVariables'].map(lambda _: find_env(_, 'NAGIOS_CONTACT'))
    # logging.critical(isinstance(df_jobs[df_jobs.name=='rmpse_campaign_controller'].container.iloc[0], dict))
    df_jobs['image'] = df_jobs.container.map(lambda _: _.get('image') if isinstance(_, dict) else '//')
    df_jobs['image_short'] = df_jobs.image.map(lambda _: _.split('/', 3)[-1])
    df_jobs.drop(columns=['container', 'environmentVariables', 'parents'], inplace=True)
    selected_cols = [
        'name', 'disabled', 'status', 'state', 'description',
        'image_short', 'monitor_flag',
        'ownerName', 'owner',
        'schedule',
        'cpus', 'disk', 'mem',
        'command', 'lastSuccess', 'lastError',
    ]
    df_jobs = df_jobs[selected_cols]
    # df_jobs.sort_values('image_short', inplace=True)

    return df_jobs

viewer = html.Div(
    [
        html.H5('nosos jobs'),
        html.Hr(),
        dbc.Row([
            dbc.Col(nosos_options, width=3, style={"width": "15rem", "padding": "0rem 0.5rem"}),
            dbc.Col(dcc.Link('Link', target='_blank', id='link-to-nosos', href=''))
        ]),
        html.Hr(),
        html.Div(id='nosos-jobs-content'),
        dcc.Interval(
            id='interval-component',
            interval=10*60*1000, # in milliseconds
            n_intervals=0
        ),
    ]
)

CELL_COLOR_MAP = [
    {
    'if': {
        'column_id': 'status',
        'filter_query': '{status} = success'
    },
    'backgroundColor': '#badbcc',
    },
    {
    'if': {
        'column_id': 'status',
        'filter_query': '{status} = failure || {status} = failure'
    },
    'backgroundColor': '#f5c2c7'
    },
    {
    'if': {
        'column_id': 'state',
        'filter_query': '{state} contains "running"'
    },
    'backgroundColor': '#badbcc'
    },
    {
    'if': {
        'column_id': 'state',
        'filter_query': '{state} = queued'
    },
    'backgroundColor': '#b6d4fe'
    },
    {
    'if': {
        # 'column_id': 'disabled',
        'filter_query': '{disabled} contains "true"'
    },
    'backgroundColor': '#bfbfbf'
    },
]

@app.callback(
    Output('link-to-nosos', 'href'),
    Output('nosos-jobs-content', 'children'),
    [Input('interval-component', 'n_intervals'),
     Input('nosos-options', 'value'),
    ],
)
def render_job_content(n, nosos_url):
    df = get_job_df(nosos_url)
    df.sort_values('name', inplace=True)
    return nosos_url, html.Div([
            dash_table.DataTable(
                id='nosos-jobs-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                filter_action='native',
                sort_action="native",
                sort_mode=None,
                sort_by=[{'column_id':'image_short', 'direction': 'asc'}],
                row_selectable='multi',
                column_selectable='multi',
                style_table = {'minWidth': '100%', 'overflowY': 'auto'},
                style_as_list_view=False,
                style_cell={'textAlign': 'left'},
                fixed_columns={'headers': True, 'data': 1},
                style_data_conditional=CELL_COLOR_MAP)
            ],
            style = {'marginLeft': '1rem', 'marginRight': '1rem'}
        )
