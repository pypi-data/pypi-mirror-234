import json
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html, callback, clientside_callback, ClientsideFunction, callback_context


##########################################################################################
file_saved_location         = 'assets/'
default_filename            = 'default_layout.json'

layout = html.Div([
            html.H1("  JSON Config Check / uploader   "),
            html.Div(id='alert-auto'),
            html.Div(id='jsoneditor', style={'width':'75vw', 'height':'70vh'}),
            dcc.Upload(id  = 'upload-data',
                children    = html.Div(
                            [ 'Drag and Drop or ',   html.A('Select Files') ]),
                style       = { 'width'         : '100%', 'height'        : '60px', 'lineHeight'    : '60px', 'borderWidth'   : '1px', 'borderStyle'   : 'dashed', 'borderRadius'  : '5px', 'textAlign'     : 'center', 'marginTop'     : '10px' },
                multiple    = False
            ),

            dbc.Button(
                'Submit', 
                id          = 'submit-button',
                className   = 'me-1',
                color       = 'primary',
                style={ 'width'         : '100%', 'height'        : '60px', 'textAlign'     : 'center', 'verticalAlign' : 'middle', 'marginTop'     : '5px'
                }
            ),

            dcc.Store(id='uploaded'),
            dcc.Store(id='alert-toggle-auto'),
            dcc.Store(id='temp-filename', data="default_layout.json"),
            dcc.Store(id='temp-json')
    ], style={ 'verticalAlign'      : 'middle', 
                'margin'            : 'auto', 
                'horizontalAlign'   : 'middle' 
})


##########################################################################################
################################# Callbacks ##############################################
##### Upload Json file to Live text Editor
clientside_callback(
    ClientsideFunction(namespace      = 'clientside',   function_name   = 'liveEditor' ), 
        Output('temp-filename',    'data'),
        Input('upload-data',  'contents'),
        [State('upload-data',  'filename')]
)


#### Fetch Json string formatted from live text editor
clientside_callback(
    ClientsideFunction(namespace       = 'clientside',  function_name   = 'saveJSON'), 
        Output('temp-json',     'data'),
        Input('submit-button',  'n_clicks'),  prevent_initial_callback= True
)


#### Write Json to assets/ folder
@callback(Output('alert-toggle-auto',    'data'),
          [Input('temp-json',            'data'), Input('temp-filename',  'data')],  prevent_initial_callback        = True )
def save_json(data, filename):
    if callback_context.triggered_id == 'temp-json':
        content     = json.dumps(data, indent=4)

        filename    = filename or default_filename
        with open(f'{file_saved_location}{filename}', 'w') as f:
            f.write(content)


####  Show alert info 
@callback(Output('alert-auto',        'children'),
          [Input('alert-toggle-auto', 'data'), Input('temp-filename',  'data')], prevent_initial_callback    = True )
def toggle_alert(_, filename):
    if callback_context.triggered_id == 'alert-toggle-auto':
        filename = filename or default_filename
        return  dbc.Alert( f'File Json saved to {file_saved_location}{filename}',
                    id      = 'alert-auto',
                    is_open = True,
                    duration= 3000,
                    color   = 'primary',)














