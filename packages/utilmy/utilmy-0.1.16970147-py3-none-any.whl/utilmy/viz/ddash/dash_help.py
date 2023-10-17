# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Dash Different Examples'),

    html.H4(children='''
        Bar Graph.
    '''),
    dcc.Graph(
        id='bar',
        figure= fig
    ),

    html.H4(children='''
        Bar Graph.
    '''),
    dcc.Graph(
        id='scatter',
        figure= px.scatter(px.data.iris(), x="sepal_width", y="sepal_length", color="species",
                 size='petal_length', hover_data=['petal_width'])
    ),

    html.H4(children='''
        line Graph.
    '''),
    dcc.Graph(
        id='line',
        figure=px.line(px.data.gapminder().query("continent=='Oceania'"), x="year", y="lifeExp", color='country')
    ),

    html.H4(children='''
        pie Graph.
    '''),
    dcc.Graph(
        id='pie',
        figure= px.pie(px.data.tips(), values='tip', names='day')
    ),

    html.H4(children='''
        histogram Graph.
    '''),
    dcc.Graph(
        id='histogram',
        figure= px.histogram(px.data.tips(), x="total_bill")
    ),

    html.H4(children='''
        density_heatmap Graph.
    '''),
    dcc.Graph(
        id='density_heatmap',
        figure= px.density_heatmap(px.data.tips(), x="total_bill", y="tip")
    ),

    html.H4(children='''
        species_id Graph.
    '''),
    dcc.Graph(
        id='species_id',
        figure= px.parallel_coordinates(px.data.iris(), color="species_id", labels={"species_id": "Species",
                "sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
                "petal_width": "Petal Width", "petal_length": "Petal Length", },
                             color_continuous_scale=px.colors.diverging.Tealrose,
                             color_continuous_midpoint=2)
    ),

    html.H4(children='''
        scatter_ternary Graph.
    '''),
    dcc.Graph(
        id='scatter_ternary',
        figure= px.scatter_ternary(px.data.election(), a="Joly", b="Coderre", c="Bergeron")
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
