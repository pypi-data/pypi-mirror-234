import logging

import os

import time
import datetime
import pytz
from functools import lru_cache

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
import requests

# Neil's CodeV16
from db.cass_queries import CassQueries

from YAW_common.helpers.utils import get_uncompressed_json
from YAW_common.helpers.couch_conn import CouchConn
from YAW_common.couchbase_query import SmartCouponControl, SmartCouponTop
from YAW_common.smart_coupon.utils import ABTestAPI

from app import app

## CONFIG, RESOURCES
abtest_api_url = 'http://100.78.10.1:10021'
abtest_api = ABTestAPI(abtest_api_url)
cb_hosts = 'acb201.YAW.jpe2b.dcnw.yyyyy,acb202.YAW.jpe2b.dcnw.yyyyy,acb203.YAW.jpe2b.dcnw.yyyyy'
couch_conn = CouchConn({
    'ca_top':{
        'hosts': cb_hosts,
        'bucket': 'top',
        'username': 'top',
        'password': '6e4IhzxbZQ8qPkrl',
        'timeout': 25.0},
    'ca_control':{
        'hosts': cb_hosts,
        'bucket': 'control',
        'username': 'control',
        'password': 'gWLN3L25FbSaOrTh',
        'timeout': 25.0},
})
cass_queries = CassQueries(config_file_path='/a/adigcb301/ipsvols05/pppppp/CodeV16/config/config_v16_pro.properties')

def get_recent_two_abtests(channel='top'):
    get_recent = 2
    smart_coupon_control = SmartCouponControl(couch_conn._get_bucket_conn('ca_control'))
    active_wcid = smart_coupon_control.get_active_weekly_campaign_id()
    pending_wcid = smart_coupon_control.get_pending_weekly_campaign_id()
    wcid_abtestid = []
    for wcid in sorted(set([pending_wcid, active_wcid]), reverse=True):
        try:
            # abtest_config = abtest_api.get_abtest_setting(active_wcid, channel, wcid)
            abtests = abtest_api.get_abtests(wcid, channel)
            for abtest_id in sorted(abtests, reverse=True):
                wcid_abtestid.append((wcid, abtest_id))
                if len(wcid_abtestid) >= get_recent:
                    break
        except Exception as e:
            logging.error(e)
        if len(wcid_abtestid) >= get_recent:
            break
    return wcid_abtestid

# https://stackoverflow.com/a/55900800
def get_ttl_60sec(seconds=60):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)

@lru_cache(maxsize=2)
def get_urlx_to_campaign_map(wcid, ttl=None):
    del ttl
    smart_coupon_control = SmartCouponControl(couch_conn._get_bucket_conn('ca_control'))
    urlx_id_campaign_id = smart_coupon_control.get_urlx_campaigns(wcid)
    return {urlx_id: campaign_id for urlx_id, campaign_id in urlx_id_campaign_id}

# selected_coupon_fields = ['urlx_mng_id', 'good_name', 'good_url', 'image_url']

def get_coupon_card(cpn_data):
    return dbc.Card(
            [
                dbc.CardImg(
                    src=cpn_data.get('image_url'),
                    top=True,
                    style={"width": "9rem", "height": "9rem"}
                ),
                dbc.CardBody([
                    html.P(cpn_data.get('urlx_mng_id'), className="card-text"),
                    # html.P(cpn_data.get('good_url'), className="card-text"),
                    # html.P(cpn_data.get('good_name'), className="card-text", style={'font-size': 10}),
                ]),
            ],
            outline=True,
            style={"width": "10rem"},
        )

def get_coupon_cards(cpn_ids):
    smart_coupon_control = SmartCouponControl(couch_conn._get_bucket_conn('ca_control'))
    results = smart_coupon_control.get_coupon_data_batch_with_cpnid(cpn_ids)
    cards = {k: get_coupon_card(v) for k, v in results.items()}
    return cards

def get_top_logic_results(easy_id, logic_options):
    smart_coupon_top = SmartCouponTop(couch_conn._get_bucket_conn('ca_top'))
    distinct_cpnids = set()
    logic_to_result = {}
    for logic_option in logic_options:
        logic_id, wcid = logic_option.split('@')
        urlx_to_campaign_map = get_urlx_to_campaign_map(wcid, get_ttl_60sec())
        urlx_items = smart_coupon_top.get_user_targeting(wcid, logic_id, easy_id) or []
        # Strange to find invalid item
        cpn_ids = [f'{wcid}_{urlx_to_campaign_map.get(int(urlx_id), 0)}_{urlx_id}_{good_id}' for urlx_id, good_id in urlx_items]
        logic_to_result[logic_id] = cpn_ids
        distinct_cpnids.update(cpn_ids)
    coupon_cards = get_coupon_cards(distinct_cpnids)
    logic_widget_rows = []
    for logic_id, cpn_ids in logic_to_result.items():
        logic_widget_rows.append(dbc.Label(f'{logic_id}: {len(cpn_ids)} items'))
        # TODO: warning box for missing item
        logic_row = html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        coupon_cards.get(cpn_id, '')
                        , width="auto"
                        # , fluid=True # need upgrade dbc to v1
                        # , style={"width": "0rem", "padding": "0rem 0rem", "margin-left": "0rem"}
                    ) for cpn_id in cpn_ids
                ]
                , style={'overflowX': 'scroll', 'width': '400rem'}
            )
            , style={'overflowX': 'scroll', 'width': '100rem'}
        ) # To scroll independently
        logic_widget_rows.append(logic_row)
        logic_widget_rows.append(html.Br())
    body = html.Div(logic_widget_rows)
    return body

### User behaviours
urlx_idx = 1
good_idx = 2
def get_user_history(source, easy_id):
    easy_id = int(easy_id)
    result = cass_queries.get_customer_history(source, [easy_id])
    history = result.get(easy_id, [])
    siid = [f'{d[urlx_idx]}_{d[good_idx]}' for d in history]
    return siid

@lru_cache(maxsize=1)
def get_product_master_schema():
    return cass_queries.product_master_schema

def get_history_card(siid_data):
    schema = get_product_master_schema()
    urlx_url = siid_data[schema['urlx_url']]
    good_url = siid_data[schema['good_url']]
    image_url = siid_data[schema['image_url']].split(' ')[0]
    good_page_link = f'https://item.yyyyy.co.jp/{urlx_url}/{good_url}/'
    return dbc.Card(
            [
                dbc.CardImg(
                    src=image_url,
                    top=True,
                    style={"width": "9rem", "height": "9rem"}
                ),
                dbc.CardBody([
                    html.P(urlx_url, className="card-text"),
                    dbc.CardLink("ItemPage", href=good_page_link, target="_blank"),
                ]),
            ],
            style={"width": "10rem"},
        )

def get_history_cards(siids):
    results = cass_queries.get_si_im_data(siids)
    cards = {k: get_history_card(v) for k, v in results.items()}
    return cards

def get_history_result(easy_id):
    brw_siids = get_user_history('brw', easy_id)
    pur_siids = get_user_history('pur', easy_id)
    distinct_siids = set(brw_siids + pur_siids)
    history_cards = get_history_cards(distinct_siids)
    history_widget_rows = []
    for event_label, siids in [('Purchase', pur_siids), ('Browsing', brw_siids)]:
        history_widget_rows.append(dbc.Label(f'{event_label}: {len(siids)} items'))
        # TODO: warning box for missing item
        history_row = html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        history_cards.get(siid, '')
                        , width="auto"
                        # , fluid=True # need upgrade dbc to v1
                        # , style={"width": "0rem", "padding": "0rem 0rem", "margin-left": "0rem"}
                    ) for siid in siids
                ]
                # , style={'overflowX': 'scroll', 'width': f'{12*len(siids)}rem'} # browsing is too long
                , style={'overflowX': 'scroll', 'width': f'100rem'}
            )
            , style={'overflowX': 'scroll', 'width': '100rem', 'height': '16rem'}
        ) # To scroll independently
        history_widget_rows.append(history_row)
        history_widget_rows.append(html.Br())
    body = html.Div(history_widget_rows)
    return body


## contents

viz_modes = html.Div(
    [
        dbc.Label("Mode"),
        dbc.RadioItems(
            options=[
                {"label": "Imp Stream", "value": 'imp', "disabled": True},
                {"label": "Clk Stream", "value": 'clk', "disabled": True},
                {"label": "Pch Stream", "value": 'pch', "disabled": True},
                {"label": "Custom", "value": 'custom'},
            ],
            value='custom',
            id="mode-input",
        ),
        dbc.Input(
            id='easyid-input',
            # type="number",
            debounce=True,
            bs_size="sm",
            disabled=False,
            # value=None,
            value=48525011, # TODO: debug
        ),
    ]
)

logic_sets = html.Div(
    [
        dbc.Label("Logic Sets"),
        dbc.Checklist(
            options=[],
            value='',
            id="logic-set-options",
        ),
    ]
)

logic_options = html.Div(
    [
        dbc.Label("Logic Options"),
        dbc.Checklist(
            options=[],
            value='',
            id="logic-options",
        ),
    ]
)

debug_info = html.Div(
    [
        dcc.Markdown("", id='debug-info')
    ]
)

ca_qa_content = html.Div(
    [
        html.H5('CA Targeting UI'),
        dbc.Row(
            [
                dbc.Col(viz_modes, width=2, style={"width": "0rem", "padding": "0rem 1rem", "margin-left": "1rem"}, className="me-2"),
                dbc.Col(logic_sets, width=2, style={"width": "0rem", "padding": "0rem 1rem", "margin-left": "1rem"}),
                dbc.Col(logic_options, width=4, style={"width": "0rem", "padding": "0rem 1rem", "margin-left": "1rem"}),
                dbc.Col(dbc.Button('Query', color='info', id='query-clicked'))
            ],
            # className="g-2", # useless before upgrade
        ),
        # dbc.Row(
        #     [
        #     # dbc.Col(dbc.Button('Home', n_clicks=0, id='goto-home', color='primary')),
        #     # dbc.Col(dbc.Button('Back', n_clicks=0, id='back-dir', color='primary')),
        #     # dbc.Col(hdfs_path, width=7),
        #     # dbc.Col(dbc.Button('Go', color='info', id='go-clicked'))
        #     ]
        # ),
        html.Hr(),
        # html.Div(debug_info),
        html.H6('Logics', id='Logics'),
        html.Div(id='logic-contents'),
        html.H6('History', id='History'),
        html.Div(id='history-contents'),
        dcc.Interval(
            id='short-interval-component',
            interval=1*60*1000, # in milliseconds
            n_intervals=0
        ),
    ]
)


## Callbacks

@app.callback(
    Output('easyid-input', 'disabled'),
    [Input('mode-input', 'value')]
)
def disable_custom_input(mode_value):
    if mode_value == 'custom':
        return False
    return True


@app.callback(
    Output('logic-set-options', 'options'),
    Output('logic-set-options', 'value'),
    Output('short-interval-component', 'interval'),
    [Input('short-interval-component', 'n_intervals')
    ],
)
def update_logic_sets(n):
    wcid_abtests = get_recent_two_abtests()
    options = [{'label': abtest_id, 'value': f'{wcid}-{abtest_id}'} for wcid, abtest_id in wcid_abtests]
    value = [_['value'] for _ in options]
    return options, value, 10*60*1000 # change the initial load status


@app.callback(
    Output('logic-options', 'options'),
    Output('logic-options', 'value'),
    [
        Input('logic-set-options', 'value'),
        Input('query-clicked', 'n_clicks'),
    ],
)
def update_logic_options(wcid_abtestid_set, query_clicked):
    options = []
    values = []
    channel = 'top'
    for value in sorted(wcid_abtestid_set, reverse=True):
        wcid, abtest_id = value.split('-')
        logic_configs = abtest_api.get_abtest_setting(wcid, channel, abtest_id)
        logics = logic_configs['logics']
        for logic in logics:
            value = f'{logic}@{wcid}'
            options.append({'label': logic, 'value': value})
            values.append(value)
    return options, values

@app.callback(
    Output("logic-contents", "children"),
    [
        Input('logic-options', 'value'),
        Input('easyid-input', 'value'),
        Input('easyid-input', 'n_submit'),
        Input('query-clicked', 'n_clicks'),
    ]
)
def show_logic_contents(logic_options, easy_id, easy_id_n_submit, query_clicked):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    event_types = ['logic-options', 'easyid-input', 'query-clicked']
    try:
        for e in event_types:
            if e in changed_id:
                cards = get_top_logic_results(easy_id, logic_options)
                return cards
        else:
            return dash.no_update
    except Exception as e:
        logging.exception(e)
        return dash.no_update

@app.callback(
    Output("history-contents", "children"),
    [
        Input('easyid-input', 'value'),
        Input('easyid-input', 'n_submit'),
        Input('query-clicked', 'n_clicks'),
    ]
)
def show_history_contents(easy_id, easy_id_n_submit, query_clicked):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    event_types = ['easyid-input', 'query-clicked']
    try:
        for e in event_types:
            if e in changed_id:
                cards = get_history_result(easy_id)
                return cards
        else:
            return dash.no_update
    except Exception as e:
        logging.exception(e)
        return dash.no_update


@app.callback(
    Output("debug-info", "children"),
    [Input('short-interval-component', 'n_intervals'),
    ],
)
def get_debug_info(n):
    smart_coupon_control = SmartCouponControl(couch_conn._get_bucket_conn('ca_control'))
    wcid_abtests = get_recent_two_abtests()
    content = (
        "```javascript",
        'active',
        smart_coupon_control.get_active_weekly_campaign_id(),
        'pending',
        smart_coupon_control.get_pending_weekly_campaign_id(),
        f"{json.dumps(wcid_abtests, separators=(',', ': '), indent=2)}",
        "```"
    )
    return content