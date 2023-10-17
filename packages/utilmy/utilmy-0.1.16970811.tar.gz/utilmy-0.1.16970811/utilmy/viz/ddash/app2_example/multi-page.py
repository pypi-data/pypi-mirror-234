import sys
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

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
                dbc.DropdownMenuItem(page["name"], href=page["path"], header=True)
                for page in dash.page_registry.values()
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


# .4 run application
if __name__ == '__main__':
    DEBUG_MODE = False
    if len(sys.argv) > 1 and sys.argv[1] == 'dev':
        DEBUG_MODE = True
    app.run_server(host='0.0.0.0', debug=DEBUG_MODE, port=5000, use_reloader=True)


df_tvcm_plan = pd.DataFrame()
df_tvcm_plan['impression'] = np.random.uniform(low=0, high=7*1e8, size=10000)
df_tvcm_plan['application'] = df_tvcm_plan['impression'].apply(lambda x: hill(x, *params_dict['tvcm_plan']))
fig_video_youtube_plan = px.line(
    df_tvcm_plan.sort_values('impression'), x='impression', y='application', title='video_youtube_plan', width=600, height=400, color_discrete_sequence=px.colors.qualitative.Set2
)
fig_tvcm_plan.update_layout(font=dict(size=12))