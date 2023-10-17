import pandas as pd
import dash_table
import dash_html_components as html

df = pd.read_parquet('/a/adigcb301/ipsvols05/pydata/WWQ_urlx_limited_word')
# df.columns = [c.decode('utf-8') for c in df.columns]
df.columns = ['_id', 'word', 'urlx_id']
df = df[['_id', 'urlx_id', 'word']]

total_keywords = df.shape[0]
unique_keywords = df.word.nunique()

_table = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        page_size=15,
        style_cell_conditional=[
            {'if': {'column_id': '_id'},
            'width': '10%'},
            {'if': {'column_id': 'urlx_id'},
            'width': '15%'},
        ],
        style_table = {'width': '100%'}
        )
    ],
    style = {'marginLeft': '2rem', 'marginRight': '2rem'}
)

urlx_limited_table = html.Div([
    html.H2('urlx-limited words'),
    html.P(f'total: {total_keywords} urlx-keywords, {unique_keywords} keywords'),
    _table
])