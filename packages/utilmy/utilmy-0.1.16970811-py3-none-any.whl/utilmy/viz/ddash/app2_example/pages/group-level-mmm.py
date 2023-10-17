import sys
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

dash.register_page(__name__)


params_dict = {
    'video_youtube_plan': [433.85386967741465, 5542733, 0.024049510820422164],
    'video_twitter_plan': [356.4030216262271, 4025057, 0.04840905588903231],
    'video_twitter_iphone': [327.86734798190736, 1272078, 2.8810718664620145],
    'video_google_yahoo_rt': [41.77618882047642, 2108359, 2.9949124411184282],
    'video_youtube_iphone': [980.7677211401996, 5628010, 4.573909849229719],
    'video_facebook_instagram': [22.74094808359279, 213042,  0.5059849923750473],
    'video_tiktok': [111.6019159869298, 975368, 7.520277993059972],
    'at_ydn': [7.728440908960495],
    'at_gdn': [1.8062211661603118],
    'at_smartNews': [1.0902017782951152],
    'at_line': [1.146792599035052],
    'at_facebook_instagram': [2.2315865972887057],
    'at_outbrain': [0.7039636884370557],
    'rt_ydn': [13.823593875678888],
    'rt_gdn': [6.423802079204775],
    'rt_criteo': [3.764051405516403],
    'rt_line': [1.3283604951997674],
    'rt_facebook_instagram_twitter': [2.6304146928402092],
    'tvcm_plan': [1950, 93806996.711751, 3.8052600563882635],
    'tvcm_time': [525, 21200042.487630907, 1.950512063816263],
    'tvcm_iphone': [1185, 57618879.067526296, 3.9941484141107035],
}

def hill(x, vmax, K, n):
    return vmax * (x**n / (K**n + x**n))


# 1. web page style configuration
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dash_bootstrap_components.themes.MINTY]
INGRESS_PATH = '/102531/mmm-dash/'

app = dash.Dash(
    __name__, 
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css", dbc.themes.MINTY],
    url_base_pathname=INGRESS_PATH
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


# 2. table and graph components
df_mmm = pd.read_csv('20220318_mmm.csv')
fig_mmm = px.bar(
    df_mmm, x='date', 
    y=['BASELINE', 'AT', 'RT', 'AFFILIATE', 'VIDEO', 'yyyyy_MEDIA', 'yyyyy_MAIL', 'COMPANY_MAIL', 'TVCM', 'RELEASE_PR', 'RELEASE_UNLIMIT5', 'RELEASE_CP'], 
    title='In-house MMM: Group-level Application',
    width=1800, height=600, color_discrete_sequence=px.colors.sequential.Turbo
)

df_cpa = pd.read_csv('20220318_cpa.csv')
fig_cpa = px.line(
    df_cpa, x='date', 
    y=['VIDEO', 'AT', 'RT', 'AFFILIATE', 'TVCM'], 
    title='In-house MMM: Group-level CPA',
    width=1800, height=600, color_discrete_sequence=px.colors.diverging.Portland
)

df_bub = pd.read_csv('20220318_bubble.csv')
fig_bub = px.scatter(
    df_bub, x='cpa', y='contribution of application', size="cost", color="media", hover_name="media", size_max=150,
    title='In-house MMM: Group-level CPA-Application',
    width=1800, height=600, color_discrete_sequence=px.colors.diverging.Portland
)

#'video_youtube_plan': [433.85386967741465, 5542733, 0.024049510820422164]
df_video_youtube_plan = pd.DataFrame()
df_video_youtube_plan['impression'] = np.random.uniform(low=0, high=1.2*1e7, size=10000)
df_video_youtube_plan['application'] = df_video_youtube_plan['impression'].apply(lambda x: hill(x, *params_dict['video_youtube_iphone']))
fig_video_youtube_plan = px.line(
    df_video_youtube_plan.sort_values('impression'), x='impression', y='application', 
    title='video_youtube_plan',
    width=1800, height=600, color_discrete_sequence=px.colors.qualitative.Set2
)

# 3. table and graph layout
app.layout = html.Div(children=[
    navbar,
    #html.H1(children='Columbus: in-house marketing mix modeling application'),
    dcc.Graph(id='mmm_plot', figure=fig_mmm),
    dcc.Graph(id='cpa_plot', figure=fig_cpa),
    dcc.Graph(id='bub_plot', figure=fig_bub),
    dcc.Graph(id='video_youtube_plan_plot', figure=fig_video_youtube_plan),
])


# .4 run application
if __name__ == '__main__':
    DEBUG_MODE = False
    if len(sys.argv) > 1 and sys.argv[1] == 'dev':
        DEBUG_MODE = True
    app.run_server(host='0.0.0.0', debug=DEBUG_MODE, port=5000, use_reloader=True)