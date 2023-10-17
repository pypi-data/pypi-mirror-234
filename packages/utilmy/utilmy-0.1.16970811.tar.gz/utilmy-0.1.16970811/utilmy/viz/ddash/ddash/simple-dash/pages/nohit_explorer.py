import logging

import os

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL

import pandas as pd
import pyarrow
import json

from YAW_common.helpers.utils import get_uncompressed_json
from YAW_common.helpers.couch_conn import CouchConn

from app import app




NOHIT_ROOT = 'hdfs://nameservice1/user/pppppp/WWQ/rt_summary/prod/nohit_query'
NOHIT_NS = 'nameservice1'
cb_hosts = ''

couch_conn = CouchConn({
    'WWQ_search':{
        'hosts': cb_hosts,
        'bucket': 'search',
        'username': 'cpc_user',
        'password': 'ZTY0YjQ1NzczOGVk',
        'timeout': 25.0},
    'WWQ_control':{
        'hosts': cb_hosts,
        'bucket': 'control',
        'username': 'cpc_user',
        'password': 'ZTY0YjQ1NzczOGVk',
        'timeout': 25.0},
})


def get_nohit_subpaths():
    hdfs = pyarrow.hdfs.connect(host=NOHIT_NS)
    return sorted([os.path.basename(x) for x in hdfs.ls(NOHIT_ROOT) if not x.endswith('progress')], reverse=True)[:24]

def get_nohit_files(partition):
    path = f'{NOHIT_ROOT}/{partition}'
    hdfs = pyarrow.hdfs.connect(host=NOHIT_NS)
    return hdfs.ls(path)

def get_nohit_table(path, option_values):
    include_ng = 'include-ng' in option_values
    include_sl = 'include-urlx-limit' in option_values
    include_un = 'include-unknown' in option_values

    hdfs = pyarrow.hdfs.connect(host=NOHIT_NS)
    df = pd.read_parquet(path)
    if not include_un:
        df = df[df.is_nohit==True]
    if not include_ng:
        df = df[df.is_ng==False]
    if not include_sl:
        df = df[df.is_urlx_limited==False]
    df = df.sample(frac=1).head(50) # TODO:
    data = df.to_dict('records')
    [_.update(id=i) for i, _ in enumerate(data)] # append 'id'
    out_table = html.Div([
            dash_table.DataTable(
                id={'type': 'nohit-table', 'index': 0},
                columns=[{"name": i, "id": i} for i in df.columns],
                data=data,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_selectable=False,
                page_size=15,
                style_cell_conditional=[
                    {'if': {'column_id': 'genre'}, 'width': '5rem'},
                    {'if': {'column_id': 'is_ng'}, 'width': '5rem'},
                    {'if': {'column_id': 'is_urlx_limited'}, 'width': '6rem'},
                    {'if': {'column_id': 'is_nohit'}, 'width': '6rem'},
                    # {'if': {'column_id': 'last_modified_time'}, 'width': '12rem'},
                    {'if': {'column_id': 'sq'},
                        'text-align': 'left',
                        'white-space': 'nowrap',
                        'border-spacing': '20px',
                        'padding': '0px 20px',
                        },
                ],
                hidden_columns=['url', 'WWQ_items', 'nohit_logics', 'hsq', 'eligible_urlxs'],
                style_as_list_view=True,
                )
            ],
            style = {'marginLeft': '1rem', 'marginRight': '1rem'}
        )
    return out_table

def get_good_widget(siids):
    control_bucket = couch_conn._get_bucket_conn('WWQ_control')
    version = control_bucket.get('WWQ_cfg_active').value
    # search_bucket = couch_conn._get_bucket_conn('WWQ_search')
    cards = []
    for siid in siids:
        cad_result = control_bucket.get(f'cad_{version}_{siid}').value
        if cad_result is None:
            continue
        cad_data = get_uncompressed_json(cad_result)
        # print(cad_data)
        good_card = dbc.Card(
            [
                dbc.CardImg(
                    src=cad_data.get('image_url'),
                    top=True,
                    style={"width": "10rem", "height": "10rem"}
                ),
                dbc.CardBody([
                    html.P(cad_data.get('urlx_id'), className="card-text"),
                    html.P(cad_data.get('good_id'), className="card-text"),
                    html.P(cad_data.get('good_name'), className="card-text",
                        style = {'font-size': 10})
                ]),
            ],
            style={"width": "12rem"},
        )
        cards.append(good_card)
    widget = dbc.Row([
        dbc.Col(card, width="auto") for card in cards
    ])
    return widget


nohit_input_groups = dbc.InputGroup([
    dbc.InputGroupAddon(NOHIT_ROOT + '/', addon_type="prepend"),
    dbc.Select(
        id='nohit-folder-options',
        options=[],
        value='',
        style={"width": "1rem"}
    ),
    dbc.Select(
        id='nohit-file-options',
        options=[],
        value='',
        style={"width": "2rem"},
        placeholder='Please select',
    ),
],
    # style={"width": "10rem"},
)

nohit_options = dbc.FormGroup(
    [
        dbc.Label("Options"),
        dbc.Checklist(
            options=[
                {"label": "Include NG", "value": 'include-ng'},
                {"label": "Include urlx Limited", "value": 'include-urlx-limit'},
                {"label": "Unknown Reason", "value": 'include-unknown'},
            ],
            value=[],
            id="nohit-options",
            inline=True,
            switch=True,
        ),
    ]
)

current_active_logic_info = html.Div(
            [
                dbc.Button(
                    "Show current logics",
                    id="collapse-button",
                    className="mb-3",
                    color="info",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody(
                        dcc.Markdown("", id="logic-config")
                    )),
                    id="collapse",
                    is_open=False,
                ),
            ]
        )

WWQnohit_content = html.Div([
    html.H5('WWQ nohit queries'),
    nohit_input_groups,
    html.Br(),
    nohit_options,
    html.Div(id='path-name-result'),
    html.Hr(),
    html.Div(id='nohit-file-content'),
    html.Br(),
    html.Br(),
    html.Hr(),
    html.H5('Available contents'),
    html.Div(id='WWQ-items-on-gsp'),
    html.Hr(),
    html.Div(id='nohit-query-detail'),
    current_active_logic_info,
    dcc.Interval(
            id='interval-component',
            interval=15*60*1000, # in milliseconds
            n_intervals=0
        ),
])

@app.callback(
    Output('nohit-folder-options', 'options'),
    Output('nohit-folder-options', 'value'),
    [Input('interval-component', 'n_intervals'),
    ],
)
def update_partitions(n):
    partitions = get_nohit_subpaths()
    options = [{'label': _, 'value': _} for _ in partitions]
    value = partitions[0]
    return options, value

@app.callback(
    Output('nohit-file-options', 'options'),
    [Input('nohit-folder-options', 'value'),
    ],
)
def update_file_options(partition):
    result = []
    # part = ''
    if partition is None:
        return result
    for f in get_nohit_files(partition):
        if f.endswith('parquet'):
            basename = os.path.basename(f)
            label = basename[:10]
            result.append({'label': label, 'value': f})
    return result

@app.callback(
    Output('path-name-result', 'children'),
    [Input('nohit-file-options', 'value'),
    ],
)
def update_final_path(path):
    if path is None:
        return dash.no_update
    # return os.path.basename(path)
    return path

@app.callback(
    Output('nohit-file-content', 'children'),
    [Input('nohit-file-options', 'value'),
     Input('nohit-options', 'value'),
    ],
)
def update_nohit_file_content(path, option_values):
    if path is None or path=='':
        return dash.no_update
    table = get_nohit_table(path, option_values)
    return table

@app.callback(
    Output('nohit-query-detail', 'children'),
    Output('WWQ-items-on-gsp', 'children'),
    [
     Input({'type':'nohit-table', 'index': ALL}, 'active_cell'),
    ],
    State({'type':'nohit-table', 'index': ALL}, 'data')
)
def show_nohit_detail(active_cell, data):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if ('nohit-table' in changed_id) and (active_cell[0] is not None):
        selected = active_cell[0]
        print(selected)
        if selected['column_id'] == 'sq':
            row_id = selected['row_id']
            selected_row = data[0][row_id]
            selected_row['WWQ_items'].sort()
            WWQ_items = ['_'.join(siid.split('/')) for _, siid in selected_row['WWQ_items']]
            selected_row['WWQ_items'] = WWQ_items
            selected_detail = {
                k: v for k, v in selected_row.items()
                if k in ('url', 'hsq','eligible_urlxs', 'nohit_logics', 'WWQ_items')
            }
            detail = dbc.CardBody([
                dcc.Markdown(
                    (
                        "```javascript",
                        f"{json.dumps(selected_detail, separators=(',', ':'), indent=2)}",
                        "```"
                    )
                ),
            ],
                style={'card-height': '20rem'}
            )
            widget = get_good_widget(WWQ_items)

            return detail, widget
    return dash.no_update, dash.no_update

@app.callback(
    Output("collapse", "is_open"),
    Output("logic-config", "children"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        if not is_open: # click to open
            control_bucket = couch_conn._get_bucket_conn('WWQ_control')
            version = control_bucket.get('WWQ_cfg_active').value
            logic_map_value = control_bucket.get(f'WWQ_cfg_search_logic_{version}').value
            logic_map = get_uncompressed_json(logic_map_value)
            logic_content = (
                "```javascript",
                f"{json.dumps(logic_map, separators=(',', ': '), indent=2)}",
                "```"
            )
            return True, logic_content
        return False, ''
    return is_open, ''