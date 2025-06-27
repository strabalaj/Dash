# Import Packages
from dash import dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from components.gemini import ask_gemini
from components.dashboard import dashboard_layout, register_callbacks

#Initialize the app
app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB], suppress_callback_exceptions=True)
register_callbacks(app)  # Register the dashboard callbacks

#App Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Div(children='Welcome Power Users!'),

    # --- Dashboard Section ---
    dbc.Nav(
            [
                dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
                dbc.NavLink("Button", id="button-link", n_clicks=0),
            ]
        ),
        html.Br(),
        html.P(id="nav-clicks"),
        html.Div(id='page-content'), # holds page content

    # --- Gemini Chatbot Section ---
    html.Div([
        "Input: ",
        dcc.Input(id='gemini-input', value='', type='text'),
        dbc.Button("Ask Gemini", id='gemini-button', n_clicks=0, color="primary", className="ms-2")
    ]),
    html.Div(id='gemini-output')
])


@callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
)


def display_dashboard_page(pathname):
    if pathname == '/dashboard':
        return dashboard_layout
    elif pathname == '/button':
        return html.Div("Button Page")

@callback(
    Output(component_id='nav-clicks', component_property='children'),
    Input(component_id='button-link', component_property='n_clicks')
)
def update_nav_clicks(n_clicks):
    if n_clicks > 0:
        return f"Button clicked {n_clicks} times"
    return "Button not clicked yet"

@callback(
    Output(component_id='gemini-output', component_property='children'),
    Input(component_id='gemini-button', component_property='n_clicks'),
    State(component_id='gemini-input', component_property='value'),
    #avoid running on page load.
    prevent_initial_call=True
)
# order of arguments matters, n_clicks first then input_value, Input then state decorator
def gemini_query(n_clicks, input_value):
    if not input_value:
        return "Please enter a query."
    response = ask_gemini(input_value)
    return dbc.Card(
        dbc.CardBody(
        [
                html.H4("Gemini Response", className="card-title"),
                dcc.Markdown(response, className="card-text", style={"whiteSpace": "pre-line"}),
        ]),
        color="grey",
        inverse=True,
    )

#Run the app
if __name__ == '__main__':
    app.run(debug=True)
