# Import Packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

#Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

#Initialize the app
app = Dash()

#App Layout
app.layout = [
    html.Div(children='From Hello World to my first Data App!'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
    ]


#Run the app
if __name__ == '__main__':
    app.run(debug=True)

#Dash charts https://plotly.com/python/?_gl=1*ncyatt*_gcl_au*MTk5NjY1MjU4My4xNzQ0NzUzMTMw*_ga*MTYyMDk4NTIyNC4xNzQ0NzUzMTMw*_ga_6G7EE0JNSC*czE3NDk3MjI4NzIkbzUkZzEkdDE3NDk3MjMyMzgkajYwJGwwJGgw 