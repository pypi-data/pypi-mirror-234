import flask
from dash import Dash
import dash_bootstrap_components as dbc
from layout.layout import layout
import requests
from dash import html, Input, Output, dash_table
import pandas as pd
import os
from config import Config
import pytz
from datetime import datetime

host = os.uname()[1]

if 'mesos' in host:
  file_name = 'prod.yaml'
else:
  file_name = 'dev.yaml' 

config = Config(file_name).get_config()

# Create Flask server
server = flask.Flask(__name__)

# Create Dash app
app = Dash(
  "__name__",
  server = server,
  external_stylesheets=[dbc.themes.JOURNAL],
  use_pages=True
  )

# Title
app.title = "YAW Dashboard"

# Layout
app.layout = layout

FRAMEWORKS_URL = 'http://zzzzzzzzz.local:10097/frameworks?d=' #d=1
HTTP_PROXY = "http://stb-dev-proxy.db.yyyyy.co.jp:9502"
HTTPS_PROXY = "https://stb-dev-proxy.db.yyyyy.co.jp:9502"

proxies = {
  "http": config['k8s_frameworks']['proxy']['http'],
  "https": config['k8s_frameworks']['proxy']['https']
}

class SimpleBackendQuery:
  def __init__(self):
    self.cache_frameworks_df = None
    pass
  def fetch_data_cache(self, value):
    r = requests.get(FRAMEWORKS_URL+str(value), proxies=proxies)
    frameworks_df = pd.DataFrame(r.json())

    def mapper(data):
      return '\n'.join([f'{k}: {v}' for k, v in data.items()])
    frameworks_df['status'] = frameworks_df['status'].map(mapper)

    frameworks_df['min_start_time'] = self.convert_to_datetime(frameworks_df, 'min_start_time')
    frameworks_df['max_heartbeat'] = self.convert_to_datetime(frameworks_df, 'max_heartbeat')

    frameworks_sel_df = frameworks_df[['framework', 'max_heartbeat', 'min_start_time', 'status']]
    self.cache_frameworks_df = frameworks_df
    return frameworks_sel_df

  def convert_to_datetime(self, df, col):
    jp_tzinfo = pytz.timezone('Asia/Tokyo')
    datetime_format = '%Y-%m-%d %H:%M:%S'
    return df[col].apply(lambda t: datetime.strftime(datetime.utcfromtimestamp(t).astimezone(jp_tzinfo), datetime_format))
    

  def get_workers_from_cache(self, framework_id):
    if self.cache_frameworks_df is None:
      return None
    selected_data = self.cache_frameworks_df[self.cache_frameworks_df.framework==framework_id].iloc[0]
    selected_worker = selected_data['workers']
    selected_worker_df = pd.DataFrame(selected_worker)
    selected_worker_columns = ['worker_id', 'task_id', 'status', 'heartbeat', 'start_time', 'server', 'monitor']
    selected_worker_df = selected_worker_df[selected_worker_columns]
    selected_worker_df['heartbeat'] = self.convert_to_datetime(selected_worker_df, 'heartbeat')
    selected_worker_df['start_time'] = self.convert_to_datetime(selected_worker_df, 'start_time')
    return selected_worker_df

simple_query = SimpleBackendQuery()

@app.callback(
    Output( component_id='workers-table-output', component_property='children' ),
  [Input(component_id='frameworks_table', component_property='data'),
   Input(component_id='frameworks_table', component_property='selected_rows')]
)
def show_workers(data, selected_rows):
  if selected_rows is None:
    return ''
  selected_data = data[selected_rows[0]]
  framework_id = selected_data['framework']
  selected_worker_df = simple_query.get_workers_from_cache(framework_id)

  return html.Div(
    [
      dash_table.DataTable(
        id='workers_table',
        columns=[{"name": i, "id": i} for i in selected_worker_df.columns],
        data=selected_worker_df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_size=5,
        row_selectable=False,
        fixed_columns={'headers': True, 'data': 1},
        style_table={'minWidth': '100%', 'overflowY': 'auto'},
        style_cell= {
          'overflow': 'hidden',
          'textOverflow': 'ellipsis',
          'textAlign': 'left'
        },
        style_cell_conditional=[
          {'if': {'column_id': 'status'}, 'width': '5%'},
          {'if': {'column_id': 'server'}, 'width': '5%'},
          {'if': {'column_id': 'monitor'}, 'width': '5%'},
          {'if': {'column_id': 'task_id'}, 'width': '25%'},
          {'if': {'column_id': 'heartbeat'}, 'width': '15%'},
          {'if': {'column_id': 'start_time'}, 'width': '15%'},
          {'if': {'column_id': 'worker_id'}, 'width': '10%'}
        ],
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_data_conditional=[
          {
            'if': { 
              'column_id': 'status',
              'filter_query': '{status} = done'
            },
            'backgroundColor': 'Green'
          },
          {
            'if': { 
              'column_id': 'status',
              'filter_query': '{status} = running'
            },
            'backgroundColor': 'Yellow'
          },
          {
            'if': { 
              'column_id': 'status',
              'filter_query': '{status} = killed || {status} = stop || {status} = failed'
            },
            'backgroundColor': 'Red'
          }
        ]
      )
    ],
    style = {'marginLeft': '2rem', 'marginRight': '2rem'}
  )

@app.callback(
  Output( component_id='days-dropdown-output', component_property='children' ),
  Input( component_id='days-dropdown', component_property='value' ),
  log=True # To Inject logger using dash-extensions [ TODO ]
)
def update_result(value):
  frameworks_sel_df = simple_query.fetch_data_cache(value)
  
  return html.Div(
    [
      dash_table.DataTable(
        id='frameworks_table',
        columns=[{"name": i, "id": i} for i in frameworks_sel_df.columns],
        data=frameworks_sel_df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        style_cell= {
          'overflow': 'hidden',
          'textOverflow': 'ellipsis',
          'height': 'auto',
          'maxWidth': 0,
          'textAlign': 'left',
          'whiteSpace': 'pre-line'
        },
        style_cell_conditional=[
          {'if': {'column_id': 'status'}, 'width': '10%'},
          {'if': {'column_id': 'max_heartbeat'}, 'width': '20%'},
          {'if': {'column_id': 'min_start_time'}, 'width': '20%'}
        ],
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_table={'width': '100%', 'padding-bottom': '2rem'},
        page_size=4,
        row_selectable='single'
      )
    ], style = {'marginLeft': '2rem', 'marginRight': '2rem'}
  )

# Main
if __name__ == '__main__':
  app.server.run(
    debug=True,
    host='0.0.0.0',
    port=7000
  )