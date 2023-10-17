import pandas as pd
import dash_table
import dash_html_components as html

df = pd.read_parquet('/a/adigcb301/ipsvols05/pydata/WWQ_ng_word')
# df.columns = [c.decode('utf-8') for c in df.columns]
df.columns = ['_id', 'word']

total_keywords = df.shape[0]

_ng_table = html.Div([
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
        ],
        style_table = {'width': '100%'}
        )
    ],
    style = {'marginLeft': '2rem', 'marginRight': '2rem'}
)

ng_table = html.Div([
    html.H2('NG words'),
    html.P(f'total: {total_keywords} keywords'),
    _ng_table
])