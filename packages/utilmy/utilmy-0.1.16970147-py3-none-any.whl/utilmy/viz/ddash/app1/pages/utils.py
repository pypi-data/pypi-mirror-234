import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, callback, ctx


############################################################################################
#from dash_bootstrap_components.dbc import Row as RR
def test1(classname="mb-3", width=4):
    #### Generate the code automatically
    grid = [
        ["Baseline  CTR level :",       dbc.Input(id= "ctr",          type = "number", placeholder = "CTR in %"),  ],
        ["Minimal Detection Effect :",  dbc.Input(id= "min_effect",   type = "number", placeholder = "CTR in %"),  ],
        ["Daily Traffic :",             dbc.Input(id= "daily_effect", type = "number", placeholder = "CTR in %"),  ],
        ["N Variants :",                dbc.Input(id= "n_variant",    type = "number", placeholder = "CTR in %"),  ],   


        ["",                            dbc.Button(id = "calc",         color = "primary", children  = "Calc" ), ],   

        [ html.H5("Nsample required ( 95% Confidence, 80% Power) :", ),  html.P(id = "result"),   ]



    ]


##########################################################################################
def generate_grid(grid, classname='mb-3'):
  lall = []
  for ri in grid : 
    lli = []
    for cj in ri :
       if isinstance(cj, str):  
          lli.append( dbc.Label( cj ) )
       else :
          lli.append(cj  )

    lall.append( dbc.Row(lli, classname = classname) )





################################# Callbacks ##############################################
def input_get(*s):
    ilist = []
    for si in s :
        if isinstance(si, str): 
            ilist.append(Input(si, "value"))
        elif isinstance(si, tuple):
            ilist.append(Input(si[0], si[1]))
    return ilist


##########################################################################################
# ### Modular Dash Html Part
# title   = html.H1("AB Test:  N-Sample calculator     ")

# ctr     = dbc.Row([ dbc.Label("Baseline  CTR level :",     width = 3),    
#                     dbc.Col( dbc.Input(id= "ctr", type = "number", placeholder = "CTR in %"),            width= 4)],      className   = "mb-3")

# mde     = dbc.Row([ dbc.Label("Minimal Detection Effect :", width = 3),    
#                     dbc.Col( dbc.Input(id= "min_effect",    type = "number", placeholder = "MDE in %"),  width= 4)],      className   = "mb-3")

# traffic = dbc.Row([ dbc.Label("Daily Traffic :",  width = 3),    
#                     dbc.Col( dbc.Input(id= "daily_traffic", type = "number", placeholder = "15000"),     width= 4)],      className   = "mb-3")

# nvariant= dbc.Row([ dbc.Label("N Variants :", width = 3),    
#                     dbc.Col( dbc.Input(id= "n_variant", type = "number", placeholder = "2"),             width= 4)],      className   = "mb-3")


# calc    = dbc.Row([ dbc.Label("",width = 3),    
#                     dbc.Col(dbc.Button(id = "calc",         color = "primary", children  = "Calc" ),     width = 4)],     className   = "mb-3")

# result  = dbc.Row([ html.H5("Nsample required ( 95% Confidence, 80% Power) :", ),  html.P(id = "result"),   
#                     html.H5("Ndays required:", ),   html.P(id = "result2")])


# ### Constructing Layout
# layout = dbc.Form([title, ctr, mde, traffic, nvariant, calc, result], style={'padding'  : '20px'})



##########################################################################################
#@callback( Output("result",           "children"),
#[Input("ctr",   "value"),       Input("min_effect",  "value"),  Input("n_variant",   "value"),    Input("calc",   "n_clicks")],  prevent_initial_callback=  True)
#input_get("ctr",  "min_effect", "n_variant",  ("calc",   "n_clicks") ),  prevent_initial_callback=  True)


