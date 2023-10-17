import sys
#sys.path.append('/Users/akira.takezawa/miniconda3/lib/python3.9/site-packages')
#import flask_compress
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json

params_dict_json = open('data/20220908_params_dict.json', 'r')
params_dict = json.load(params_dict_json)

def hill(x, alpha, beta):
    return alpha * (x * beta)

def log1p(x, alpha):
    return alpha * np.log(x + 1)

# 0. web page style configuration
app = dash.Dash(
    __name__, 
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css", dbc.themes.MINTY],
    url_base_pathname='/102531/mmm-dash/'
)
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Group-level MMM", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Media-level MMM", href="#"),
                dbc.DropdownMenuItem("Media-level Optimization of Bduget Combination", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Columbus: in-house marketing mix modeling application",
    brand_href="#",
    color="secondary",
    dark=True,
)

# 1. Group-level Monthly MMM chart
df_mmm = pd.read_csv('data/20220908_mmm_group_level.csv')
df_mmm['year'] = pd.DatetimeIndex(df_mmm['date']).year
df_mmm['month'] = pd.DatetimeIndex(df_mmm['date']).month
df_mmm['date'] = df_mmm['year'].astype(str) + '/' + df_mmm['month'].astype(str)
fig_mmm = px.bar(
    df_mmm, x='date', y=['BASELINE', 'RELEASE_PR', 'RELEASE_UNLIMIT5', 'RELEASE_CP', 'yyyyy_MEDIA', 'yyyyy_MAIL', 'COMPANY_MAIL', 'SEM', 'AFFILIATE', 'AT', 'RT', 'VIDEO', 'TVCM'], 
    title='Group-level: Contribution to Monthly New Applications', width=1800, height=600, color_discrete_sequence=px.colors.sequential.Turbo
)

"""
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df_mmm.to_csv, "mmm_group_level.csv")
"""

# 2. Group-level Monthly CPA chart
df_cpa = pd.read_csv('data/20220909_cpa_total.csv')
df_cpa['year'] = pd.DatetimeIndex(df_cpa['date']).year
df_cpa['month'] = pd.DatetimeIndex(df_cpa['date']).month
df_cpa['date'] = df_cpa['year'].astype(str) + '/' + df_cpa['month'].astype(str)
fig_cpa = px.line(
    df_cpa, x='date', y=['TVCM', 'VIDEO', 'RT', 'AT', 'AFFILIATE', 'SEM'], 
    title='Group-level: CPA(Total Group Cost/Total Group Contribution)', width=1800, height=600, color_discrete_sequence=px.colors.diverging.Portland
)

# 3. Group-level Monthly CPA, Application, Cost chart
df_bub = pd.read_csv('data/20220910_bubble_total.csv')
fig_bub = px.scatter(
    df_bub, x='CPA', y='Contribution of application', size="Cost", color="Media", hover_name="Media", size_max=150,
    title='Group-level: CPA, Total Group Contribution, Total Group Cost', width=1800, height=600, color_discrete_sequence=px.colors.diverging.Portland
)

# 4. Media-level Monthly MMM table
df_med = pd.read_csv('data/20220908_media_level_contrib.csv')
fig_med = go.Figure(
    data=[
        go.Table(
            header=dict(values=list(df_med.columns), fill_color='#78c2ad', align='center', font=dict(color='white')),
            cells=dict(values=df_med.transpose().values.tolist(), fill_color='#f8f9fa', align='right', font=dict(color='black'))
        )
    ]
)
fig_med.update_layout(height = 770, width = 1500, title_text = 'Media-level: Contribution to Monthly New Applications',)

# 5. Media-level Daily Imp-App Curve chart
df_tvcm_plan = pd.DataFrame()
df_tvcm_plan['impression'] = np.random.uniform(low=0, high=2.0*1e8, size=10000)
df_tvcm_plan['application'] = df_tvcm_plan['impression'].apply(lambda x: hill(x, *params_dict['tvcm_plan']))
fig_tvcm_plan = px.line(
    df_tvcm_plan.sort_values('impression'), x='impression', y='application', title='tvcm_plan', width=600, height=400, color_discrete_sequence=px.colors.qualitative.Pastel1
)
fig_tvcm_plan.update_layout(font=dict(size=12,))

df_video_youtube_plan = pd.DataFrame()
df_video_youtube_plan['impression'] = np.random.uniform(low=0, high=1.2*1e7, size=10000)
df_video_youtube_plan['application'] = df_video_youtube_plan['impression'].apply(lambda x: hill(x, *params_dict['video_youtube_plan']))
fig_video_youtube_plan = px.line(
    df_video_youtube_plan.sort_values('impression'), x='impression', y='application', title='video_youtube_plan', width=600, height=400, color_discrete_sequence=px.colors.qualitative.Set2
)
fig_video_youtube_plan.update_layout(font=dict(size=12,))

df_video_twitter_plan = pd.DataFrame()
df_video_twitter_plan['impression'] = np.random.uniform(low=0, high=9*1e6, size=10000)
df_video_twitter_plan['application'] = df_video_twitter_plan['impression'].apply(lambda x: hill(x, *params_dict['video_twitter_plan']))
fig_video_twitter_plan = px.line(
    df_video_twitter_plan.sort_values('impression'), x='impression', y='application', title='video_twitter_plan', width=600, height=400, color_discrete_sequence=px.colors.qualitative.Set2
)
fig_video_twitter_plan.update_layout(font=dict(size=12,))

"""
df_video_facebook_instagram = pd.DataFrame()
df_video_facebook_instagram['impression'] = np.random.uniform(low=0, high=450000, size=10000)
df_video_facebook_instagram['application'] = df_video_facebook_instagram['impression'].apply(lambda x: hill(x, *params_dict['video_facebook_instagram']))
fig_video_facebook_instagram = px.line(
    df_video_facebook_instagram.sort_values('impression'), x='impression', y='application', title='video_facebook_instagram', width=600, height=400, color_discrete_sequence=px.colors.qualitative.Set2
)
fig_video_facebook_instagram.update_layout(font=dict(size=12,))
"""

df_video_tiktok = pd.DataFrame()
df_video_tiktok['impression'] = np.random.uniform(low=0, high=3*1e6, size=10000)
df_video_tiktok['application'] = df_video_tiktok['impression'].apply(lambda x: hill(x, *params_dict['video_tiktok']))
fig_video_tiktok = px.line(
    df_video_tiktok.sort_values('impression'), x='impression', y='application', title='video_tiktok', width=600, height=400, color_discrete_sequence=px.colors.qualitative.Set2
)
fig_video_tiktok.update_layout(font=dict(size=12,))

df_video_google_rt = pd.DataFrame()
df_video_google_rt['impression'] = np.random.uniform(low=0, high=6*1e6, size=10000)
df_video_google_rt['application'] = df_video_google_rt['impression'].apply(lambda x: hill(x, *params_dict['video_google_rt']))
fig_video_google_rt = px.line(
    df_video_google_rt.sort_values('impression'), x='impression', y='application', title='video_google_rt', width=600, height=400, color_discrete_sequence=px.colors.qualitative.Set2
)
fig_video_google_rt.update_layout(font=dict(size=12,))

df_video_yahoo_rt = pd.DataFrame()
df_video_yahoo_rt['impression'] = np.random.uniform(low=0, high=6*1e6, size=10000)
df_video_yahoo_rt['application'] = df_video_yahoo_rt['impression'].apply(lambda x: hill(x, *params_dict['video_yahoo_rt']))
fig_video_yahoo_rt = px.line(
    df_video_yahoo_rt.sort_values('impression'), x='impression', y='application', title='video_yahoo_rt', width=600, height=400, color_discrete_sequence=px.colors.qualitative.Set2
)
fig_video_yahoo_rt.update_layout(font=dict(size=12,))

df_at_ydn = pd.DataFrame()
df_at_ydn['impression'] = np.random.uniform(low=0, high=0.01*1e7, size=10000)
df_at_ydn['application'] = df_at_ydn['impression'].apply(lambda x: hill(x, *params_dict['at_ydn']))
fig_at_ydn = px.line(
    df_at_ydn.sort_values('impression'), x='impression', y='application', title='at_ydn', width=600, height=400, color_discrete_sequence=px.colors.qualitative.Safe
)
fig_at_ydn.update_layout(font=dict(size=12,))

df_at_gdn = pd.DataFrame()
df_at_gdn['impression'] = np.random.uniform(low=0, high=0.02*1e7, size=10000)
df_at_gdn['application'] = df_at_gdn['impression'].apply(lambda x: hill(x, *params_dict['at_gdn']))
fig_at_gdn = px.line(
    df_at_gdn.sort_values('impression'), x='impression', y='application', title='at_gdn', width=600, height=400, color_discrete_sequence=px.colors.qualitative.Safe
)
fig_at_gdn.update_layout(font=dict(size=12,))

# 6. Monthly Optimization table
df_opt = pd.read_csv('data/20220908_recommendation.csv')
#df_opt = df_opt[['Group', 'Media', 'Budget_Before_Optimization', 'Budget_After_Optimization', 'Rate_of_Change(%)', 'Budget_of_Change']]
fig_opt = go.Figure(
    data=[
        go.Table(
            header=dict(values=list(df_opt.columns), fill_color='#f3969a', align='center', font=dict(color='white')),
            cells=dict(values=df_opt.transpose().values.tolist(), fill_color='#f8f9fa', align='right', font=dict(color='black'))
        )
    ]
)
fig_opt.update_layout(height = 700, width = 1500, title_text = 'Media-level: Optimal Allocation of Monthly Budget',)

# 7. Display all the components
app.layout = html.Div(children=[
    navbar,
    #html.H1('1. Monthly MMM Attribution Result'),
    #html.H3('This plot shows the number of contributed applications in yyyyy Mobile for each month. The granularrity of segment is advertisement groups i.e. TVCM(plan and time, iphone), Video(instagram and tiktok, youtube)'),
    #html.H4('I am akira takezawa'),
    dcc.Graph(id='mmm_plot', figure=fig_mmm),
    #html.H4('This plot shows the number of contributed applications in yyyyy Mobile for each month. The granularrity of segment is advertisement groups i.e. TVCM(plan and time, iphone), Video(instagram and tiktok, youtube)'),
    #html.Button("Download Monthly Group-level MMM CSV", id="btn_csv"),
    #dcc.Download(id="download-dataframe-csv"),
    dcc.Graph(id='cpa_plot', figure=fig_cpa),
    dcc.Graph(id='bub_plot', figure=fig_bub),
    dcc.Graph(id='med_table', figure=fig_med),
    dcc.Graph(id='tvcm_plan_plot', figure=fig_tvcm_plan, style={'display': 'inline-block'}),
    dcc.Graph(id='video_youtube_plan_plot', figure=fig_video_youtube_plan, style={'display': 'inline-block'}),
    dcc.Graph(id='video_twitter_plan_plot', figure=fig_video_twitter_plan, style={'display': 'inline-block'}),
    #dcc.Graph(id='video_tiktok_plot', figure=fig_video_tiktok, style={'display': 'inline-block'}),
    #dcc.Graph(id='video_facebook_instagram_plot', figure=fig_video_facebook_instagram, style={'display': 'inline-block'}),
    dcc.Graph(id='video_google_rt_plot', figure=fig_video_google_rt, style={'display': 'inline-block'}),
    #dcc.Graph(id='video_yahoo_rt_plot', figure=fig_video_yahoo_rt, style={'display': 'inline-block'}),
    dcc.Graph(id='at_ydn_plot', figure=fig_at_ydn, style={'display': 'inline-block'}),
    dcc.Graph(id='at_gdn_plot', figure=fig_at_gdn, style={'display': 'inline-block'}),
    dcc.Graph(id='opt_table', figure=fig_opt),
])

# 8. Run application
if __name__ == '__main__':
    DEBUG_MODE = False
    if len(sys.argv) > 1 and sys.argv[1] == 'dev':
        DEBUG_MODE = True
    app.run_server(host='0.0.0.0', debug=True, port=5000, use_reloader=True)