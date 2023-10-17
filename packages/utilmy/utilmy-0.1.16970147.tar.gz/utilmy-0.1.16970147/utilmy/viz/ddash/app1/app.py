"""  Launch app
Docs::

    pip install fire dash dash_bootstrap_components dash_treeview_antd jsoncomment pandas
           
    Command to run
         cd utilmy/viz/ddash/app1

        python app.py main --content_layout assets/mixed_layout.json   
    
    File needed:
         assets/mixed_layout.json
         html    files to assets/html/
         dash_pages.py files to pages/ folder
    
    Doc:
    https://dash-bootstrap-components.opensource.faculty.ai/docs/components/form/


"""

app = None
try :
    import os, shutil, importlib
    from dash import Dash, html
    import dash_bootstrap_components as dbc    
    from dash.dcc import Store
    from dash.dependencies import ClientsideFunction, Input, Output
    from dash_treeview_antd import TreeView
    from jsoncomment import JsonComment

    app         = Dash( __name__, 
                        external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/jsoneditor.min.css'],
                        suppress_callback_exceptions=True
                    )
    app.title   = 'Template App html'
    pages       = {}
    json        = JsonComment()
except Exception as e :
    print(e)
    1/0


##########################################################################################
from utilmy import log,log2




##########################################################################################
def test_all():
    test1()

def test1():
    """  Test Mixed Render. command: python app.py test4
    Docs::    
    
        python app.py main --content_layout assets/mixed_layout.json
        
    """
    import utilmy as uu 
    dir_repo, _ = uu.dir_testinfo()
    cmd         = f"cd {dir_repo}/viz/ddash/app1/  && python app.py main --content_layout assets/mixed_layout.json & sleep 10 && curl -Is 127.0.0.1:8050 | head -n 1 && pkill -f 'python app.py' "
    os.system(cmd)


##########################################################################################
def export(name="app1", dirout=""):
    """  Export script dir to target dir. command: python app.py export
    Docs::    

        name (str, optional): _description_. Defaults to "app1".
        dirout (str, optional): _description_. Defaults to Current Working Directory.
    """
    import utilmy
    
    dirout      = dirout or os.getcwd()
    dirout      = dirout + '/' + name

    dir_repo, _ = utilmy.dir_testinfo()
    
    os.makedirs(dirout, exist_ok=True)
    shutil.copytree( dir_repo + "/viz/ddash/app1/", dirout, dirs_exist_ok=True )




##########################################################################################
################################# Callbacks ##############################################
### Callback validation in Javascript (assets/scripts.js)  ##################
""" Validate target file or url, Construct path to target file
    and Invoke page_render_html callback. 

"""
app.clientside_callback(
    ClientsideFunction(namespace       = 'clientside',
                       function_name   = 'render'), 
        Output('target-render', 'data')
    ,
    [   Input('input',    'selected'),
        Input('homepage', 'data')
    ]
)



### Callback Render   ######################################################
@app.callback(   Output('output',       'children'), 
                Input('target-render', 'data'), 
                prevent_initial_call   = True )
def page_render_html(data:str):
    """  Generate static HTML page via Iframe or Dash Layout
    Docs::

        data:    (str) path to target file
        Returns: (dash.html.Div) Iframe Layout or Dash Html Layout

    """
    
    if data.endswith('.py'):
        page    = data.split('/')[-1][:-len('.py')]
        return  pages[page].layout
    return html.Iframe(src=data, width='100%', height='100%')
        

##########################################################################################
def sidebar_v1(sidebar:dict):
    """ Compose Sidebar v1 layout component.
    Docs::

        sidebar      : (dict) Sidebar data and style

        Returns:  (dash.html.Div) Sidebar v1 Div Component
        Raises:   Raised if data or style is not exist in sidebar_content dict.
    """

    try:
        sidebar_content = html.Div([ 
                            TreeView(  id   = 'input',
                                multiple    = False,
                                checkable   = False,
                                checked     = False,
                                selected    = [],
                                expanded    = [],
                                data        = sidebar['data']
                            ), 
                            ],
                            style       = sidebar['style']
                        )
    except Exception as e:
        print(f'Sidebar issue. Details:\n {e}')
        raise ValueError('style or data key not found in json file') 
    else:
        return sidebar_content



##########################################################################################
def page_render_main(content_layout:dict):
    """  Will generate the Whole page of the App : Side Bar + main
    Docs::

        content : (dict) content layout
        Raises:   Raised if version, sidebar_content or homepage is not found in layout dict.
    
    """
    #### Sidebar Generator  #################
    # print(content_layout)
    SIDEBAR_VER        = { 1: sidebar_v1 } # Scalable sidebar
    try :    
       version         = content_layout['sidebar_content']['version'] 
       sidebar_content = SIDEBAR_VER[version](content_layout['sidebar_content'])
       homepage        = content_layout['sidebar_content']['data']['key']
    except Exception as e : 
        print(f'Content Layout issue. Details:\n {e}')
        print(f'{content_layout} \n')        
        raise ValueError("version, sidebar_content or homepage is not found in layout") 


    #### Main content  ####################
    main_content    = html.Div(id="output", style=content_layout['main_content'])

    #### All = Main + Sidebar
    app.layout      = html.Div([ sidebar_content, 
                                 main_content,
                                 Store(id='homepage', storage_type='session', data=homepage),
                                 Store(id='target-render')
                            ])


def main(content_layout="assets/mixed_layout.json", debug=True):
    """ Run main Server Dash App
    Docs::

        python app.py main --content_layout assets/mixed_layout.json   

        content_layout  : path to json layout file.  Content layout in JSON format. Default to 'assets/mixed_layout.json'.
        debug           : True/False.  Set dash debug options.    

    """
    global pages

    try:
        for page in [f for f in os.listdir('pages') if f.endswith('.py')]:
            page        = page[:-3]
            pages[page] = importlib.import_module('pages.' + page)
        
        content_layout  = json.loadf(content_layout)
    except Exception as e:
        print(f'Error importing dash page module or json. Details:\n {e}')
    
    page_render_main(content_layout)
    
    app.run_server(debug=debug)


##########################################################################################
if __name__ == '__main__':
     import fire
     fire.Fire()

