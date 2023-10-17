
import dash
import dash_auth
import dash_bootstrap_components as dbc

from layout.layout import layout

VALID_USERNAME_PASSWORD_PAIRS = {
    'kyle': 'youdontknowthis2',
    'komoda': 'forkomodasan'
}

# title is the title on html title
extra = 'https://use.fontawesome.com/releases/v5.15.3/css/all.css'

app = dash.Dash(title='YAW-Kyle', external_stylesheets=[dbc.themes.BOOTSTRAP, extra])
app.config.suppress_callback_exceptions = True

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server = app.server # flask app

app.layout = layout
