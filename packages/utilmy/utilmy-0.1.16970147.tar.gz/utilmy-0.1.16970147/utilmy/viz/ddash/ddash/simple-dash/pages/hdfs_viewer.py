import logging

import os

import datetime
import pytz

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL

import pandas as pd
import pyarrow
import humanize
import json

from app import app

nameservice_options = dbc.Select(
    id="ns-option",
    options=[
        {"label": "nameservice1", "value": "nameservice1"},
        {"label": "jpw1ns1", "value": "jpw1ns1"},
        {"label": "jpw1ns2", "value": "jpw1ns2"},
        {"label": "jpe2ns1", "value": "jpe2ns1"},
        {"label": "jpc1ns1", "value": "jpc1ns1"},
        {"label": "jpc1ns2", "value": "jpc1ns2"},
        {"label": "jpc1ns3", "value": "jpc1ns3"},
    ],
    value='nameservice1'
)
hdfs_path = dbc.Input(
    id='hdfs-path',
    type="text",
    debounce=True,
    autoFocus=True,
    value='/user/pppppp'
)

options = dbc.FormGroup(
    [
        dbc.Label("Options"),
        dbc.Checklist(
            options=[
                {"label": "Hide owner", "value": 'hide-owner'},
                {"label": "Human readable", "value": 'human-readable'},
                {"label": "Reverse sort", "value": 'reverse-sort'},
            ],
            value=['hide-owner'],
            id="options",
            inline=True,
            switch=True,
        ),
    ]
)

time_format = dbc.FormGroup(
    [
        dbc.Label("Time"),
        dbc.RadioItems(
            options=[
                {"label": "Unix", "value": 'unix'},
                {"label": "UTC", "value": 'utc'},
                {"label": "JST", "value": 'jst',}
            ],
            value='unix',
            id="time-format",
            inline=True,
        ),
    ]
)

limit_rows = dbc.FormGroup(
    [
        dbc.Label('Limit'),
        dbc.Input(
            id='file-display-limit',
            type="number",
            min=1,
            max=1000,
            step=1,
            bs_size="sm",
            value=1000,
        ),
    ]
)

hdfs_viewer = html.Div(
    [
        html.H5('HDFS browser'),
        dbc.Row([
            dbc.Col(options, width=6, style={"width": "11rem", "padding": "0rem 1rem"}),
            dbc.Col(time_format, width=3, style={"width": "11rem", "padding": "0rem 1rem"}),
            dbc.Col(limit_rows, width=2)
            ]),
        dbc.Row([
            dbc.Col(nameservice_options, width=2, style={"width": "15rem", "padding": "0rem 0.5rem"}),
            dbc.Col(dbc.Button('Home', n_clicks=0, id='goto-home', color='primary')),
            dbc.Col(dbc.Button('Back', n_clicks=0, id='back-dir', color='primary')),
            dbc.Col(hdfs_path, width=7),
            dbc.Col(dbc.Button('Go', color='info', id='go-clicked'))
            ]),
        html.Hr(),
        html.P(id='summary'),
        html.Div(id='hdfs-path-content'),
        html.Br(),
        html.Br(),
        dbc.Spinner(html.Div(id='hdfs-file-content')),
        dbc.Spinner(html.Div(id='hdfs-file-preview')),
        # html.Div(id='hdfs-file-content'),
        # html.Div(id='hdfs-file-preview')
    ]
)

def get_file_contents(ns, path):
    hdfs = pyarrow.hdfs.connect(host=ns)
    stats = hdfs.ls(path, detail=True)[0]
    return html.Div([
        html.Hr(),
        dbc.Card([
            dbc.CardHeader(
                html.H5(f'{path}', id={'type':'card-hdfs-file-name', 'index': 0})
            ),
            dbc.CardBody([
                dcc.Markdown(
                    (
                        "```javascript",
                        f"{json.dumps(stats, separators=(',', ':'), indent=2)}",
                        "```"
                    )
                ),
                dbc.Button('plain-text preview', color='info', id={'type': 'button-file-preview-plain-text', 'index':0}, style={"margin-left": "15px"}),
                dbc.Button('plain-json preview', color='info', id={'type': 'button-file-preview-plain-json', 'index':0}, style={"margin-left": "15px"}),
                dbc.Button('csv table preview', color='info', id={'type': 'button-file-preview-csv-table', 'index':0}, style={"margin-left": "15px"}),
                dbc.Button('json table preview', color='info', id={'type': 'button-file-preview-json-table', 'index':0}, style={"margin-left": "15px"}, disabled=True),
            ])
        ])
    ])

def get_file_content_preview(ns, path, view_type='csv-table', sep=',', chunksize=10):
    hdfs = pyarrow.hdfs.connect(host=ns)
    assert view_type in ('csv-table', 'json-table', 'plain-json', 'plain-text')
    def get_table_preview():
        if view_type == 'csv-table':
            with pd.read_csv(path, sep=sep, chunksize=chunksize) as reader:
                for df in reader:
                    return df
        elif view_type=='json-table':
            with pd.read_json(path, lines=True, chunksize=chunksize) as reader:
                for df in reader:
                    return df
    def get_text_preview():
        with pd.read_csv(path, names=['value'], chunksize=chunksize, sep='\n') as reader:
            for df in reader:
                rows = df.to_dict('list')['value']
                if view_type == 'plain-text':
                    return rows
                elif view_type == 'plain-json':
                    return [json.loads(_) for _ in rows]
    if view_type in ('csv-table', 'json-table'):
        df = get_table_preview()
        # print(df)
        return html.Div([
            dash_table.DataTable(
                id='table-file-preview',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                filter_action='none',
                sort_action='none',
                sort_mode=None,
                row_selectable=False,
                # style_table = {'minWidth': '100%', 'overflowY': 'auto'},
                style_as_list_view=True,
                )
            ],
            style = {'marginLeft': '1rem', 'marginRight': '1rem'}
        )
    elif view_type in ('plain-json', 'plain-text'):
        lines = get_text_preview()
        if view_type == 'plain-text':
            newline = '\n'
            content = f"{newline.join(lines)}"
        else:
            content = f"{json.dumps(lines, separators=(',', ':'), indent=2, ensure_ascii=False)}"
        return html.Div([
            html.Hr(),
            dbc.Card([
                dbc.CardBody([
                    dcc.Markdown(
                        (
                            "```javascript",
                            content,
                            "```"
                        )
                    ),
                ])
            ])
        ])

def get_hdfs_table(ns, path, option_values, ts_format, limit):
    human_readable = 'human-readable' in option_values
    reverse_sort = 'reverse-sort' in option_values

    columns = ['kind', 'owner', 'group', 'size', 'last_modified_time', 'name']
    jst_timezone = pytz.timezone('Asia/Tokyo')
    def get_dir_info(dir_info):
        dir_info['kind'] = 'd' if dir_info['kind'] == 'directory' else '-'
        if human_readable:
            dir_info['size'] = humanize.naturalsize(dir_info['size'], gnu=True)
        if ts_format != 'unix':
            ts = datetime.datetime.utcfromtimestamp(dir_info['last_modified_time'])
            if ts_format == 'jst':
                ts = ts.astimezone(jst_timezone)
            dir_info['last_modified_time'] = ts.strftime('%Y-%m-%d %H:%M:%S')
        return dir_info

    hdfs = pyarrow.hdfs.connect(host=ns)
    try:
        if not hdfs.exists(path):
            return False, 0, 0, None
    except Exception as e:
        logging.exception(e)
        # maybe no permission
        return None, 0, 0, None
    try:
        sub_dirs = hdfs.ls(path, detail=True)
    except Exception as e:
        logging.exception(e)
        # maybe no permission
        return None, 0, 0, None

    if reverse_sort:
        sub_dirs = sorted(sub_dirs, key=lambda _: _.get('name'), reverse=True)
    sub_dirs = [get_dir_info(_) for _ in sub_dirs]
    [_.update(id=i) for i, _ in enumerate(sub_dirs)] # append 'id'
    total_count = len(sub_dirs)
    sub_dirs = sub_dirs[:limit]
    display_count = len(sub_dirs)


    out_table = html.Div([
            dash_table.DataTable(
                id={'type': 'file-table', 'index': 0},
                columns=[{"name": i, "id": i} for i in columns],
                data=sub_dirs,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_selectable=False,
                page_size=15,
                style_cell_conditional=[
                    {'if': {'column_id': 'owner'}, 'width': '5rem'},
                    {'if': {'column_id': 'group'}, 'width': '5rem'},
                    {'if': {'column_id': 'kind'}, 'width': '4rem'},
                    {'if': {'column_id': 'size'}, 'width': '4rem'},
                    {'if': {'column_id': 'last_modified_time'}, 'width': '12rem'},
                    {'if': {'column_id': 'name'},
                        'text-align': 'left',
                        'white-space': 'nowrap',
                        'border-spacing': '20px',
                        'padding': '0px 20px',
                        },
                ],
                fixed_columns={'headers': True, 'data': 3},
                style_table = {'minWidth': '100%', 'overflowY': 'auto'},
                hidden_columns=['owner', 'group'],
                style_as_list_view=True,
                )
            ],
            style = {'marginLeft': '1rem', 'marginRight': '1rem'}
        )
    return True, total_count, display_count, out_table

@app.callback(
    Output({'type': 'file-table', 'index': ALL}, 'hidden_columns'),
    [Input('options', 'value')]
)
def set_pre_options(option_values):
    if 'hide-owner' not in option_values:
        return [[]]
    return [['owner', 'group']]


@app.callback(
    Output('hdfs-path', 'invalid'),
    Output('summary', 'children'),
    Output('hdfs-path-content', 'children'),

    [Input('ns-option', 'value'),
     Input('hdfs-path', 'value'),
     Input('hdfs-path', 'n_submit'),
     Input('go-clicked', 'n_clicks'),
     Input('options', 'value'),
     Input('time-format', 'value'),
     Input('file-display-limit', 'value')
    ]
)
def get_hdfs_path_contents(ns, path, path_submit, clicked, option_values, ts_format, limit):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    try:
        event_types = ['go-clicked', 'hdfs-path', 'ns-option',
                       'options', 'time-format', 'file-display-limit']
        for e in event_types:
            if e in changed_id:
                exists, total_count, display_count, table = get_hdfs_table(ns, path, option_values, ts_format, limit)
                logging.info(exists)
                error = exists is None
                invalid = (error) | (not exists)
                if error:
                    summary = dbc.Alert("maybe no permission", color="warning")
                    table = dash.no_update
                elif invalid:
                    summary = dbc.Alert("path does not exist", color="warning")
                    table = dash.no_update
                else:
                    summary = f'total: {total_count} items, displaying {display_count} items'

                return invalid, summary, table
        else:
            return dash.no_update
    except Exception as e:
        logging.exception(e)
        return dash.no_update

@app.callback(
    Output('hdfs-path', 'value'),
    Output('hdfs-file-content', 'children'),
    [Input('goto-home', 'n_clicks'),
     Input('back-dir', 'n_clicks'),
     Input('ns-option', 'value'),
     Input({'type':'file-table', 'index': ALL}, 'active_cell'),
     Input('hdfs-path', 'value'),
    ],
    State({'type':'file-table', 'index': ALL}, 'data')
)
def chdir(_1, _2, ns, active_cell, current_path, data):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'goto-home' in changed_id:
        return '/user/pppppp', html.Div()
    elif 'ns-option' in changed_id:
        return '/user/pppppp', html.Div()
    elif 'back-dir' in changed_id:
        return os.path.dirname(current_path), html.Div()
    elif ('file-table' in changed_id) and (active_cell[0] is not None):
        selected_path = active_cell[0]
        # print(selected_path)
        if selected_path['column_id'] == 'name':
            row_id = selected_path['row_id']
            selected_row = data[0][row_id]
            path_type = selected_row['kind']
            path_name = selected_row['name']
            if path_type == 'd':
                return path_name, html.Div()
            else: # '-'
                content = get_file_contents(ns, path_name)
                return dash.no_update, content
        else:
            return dash.no_update, dash.no_update
    else:
        return current_path, html.Div()

@app.callback(
    Output('hdfs-file-preview', 'children'),
    [Input({'type': 'button-file-preview-csv-table', 'index': ALL}, 'n_clicks'),
     Input({'type': 'button-file-preview-json-table', 'index': ALL}, 'n_clicks'),
     Input({'type': 'button-file-preview-plain-json', 'index': ALL}, 'n_clicks'),
     Input({'type': 'button-file-preview-plain-text', 'index': ALL}, 'n_clicks'),
     Input('ns-option', 'value'),
     Input({'type': 'card-hdfs-file-name', 'index': ALL}, 'children'),
     Input('hdfs-path', 'value')
    ],
)
def update_file_preview(_1, _2, _3, _4, ns, filename, current_path):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    # print(changed_id)
    try:
        if (filename is None) or (len(filename)==0):
            return html.Div([])
        filename = filename[0]
        if 'button-file-preview-csv-table' in changed_id:
            sep = '\n'
            if 'csv' in filename:
                sep = ','
            elif 'tsv' in filename:
                sep = '\t'
            return get_file_content_preview(ns, filename, view_type='csv-table', sep=sep, chunksize=10)
        elif 'button-file-preview-json-table' in changed_id:
            return get_file_content_preview(ns, filename, view_type='json-table', sep=None, chunksize=10)
        elif 'button-file-preview-plain-json' in changed_id:
            return get_file_content_preview(ns, filename, view_type='plain-json', sep=None, chunksize=10)
        elif 'button-file-preview-plain-text' in changed_id:
            return get_file_content_preview(ns, filename, view_type='plain-text', sep=None, chunksize=10)
        else:
            return html.Div([])
    except Exception as e:
        logging.exception(e)
        return dbc.Alert(f"We don't do that here!   Exception {e}", color="warning")