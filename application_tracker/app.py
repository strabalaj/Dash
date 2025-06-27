from dash import dash, html, dcc, callback, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import os 

#set columns and initialize DataFrame
columns = ['Date Applied', 'Company', 'Position', 'Status', "Notes"]
data_path = "jobs.csv"
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    df = pd.DataFrame(columns = columns)



app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])
app._jobs = df.copy()

def get_table_data(df):
    data = df.to_dict('records')
    for i, row in enumerate(data):
        data[i]['Edit'] = f'Edit-{i}'
    return data

app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="Navbar",
        brand_href="#",
        color="primary",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Linkedin", href="#")),
            dbc.NavItem(dbc.NavLink("Resume", href="#")),
            dbc.NavItem(dbc.NavLink("CV", href="#")),
            dbc.NavItem(dbc.NavLink("About", href="#")),
            dbc.DropdownMenu(
                label="Dropdown",
                children=[
                    dbc.DropdownMenuItem("Action", href="#"),
                    dbc.DropdownMenuItem("Another action", href="#"),
                    dbc.DropdownMenuItem("Something else here", href="#"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Separated link", href="#"),
                ],
                nav=True,
                in_navbar=True,
            ),
        ],
    ),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Input(id='date-applied', size="md", type='text', placeholder='Date Applied'),
            dbc.Input(id='input-company', size="md", type='text', placeholder='Company'),
            dbc.Input(id='input-position', size="md", type='text', placeholder='Position'),
            dbc.Input(id='input-status', size="md", type='text', placeholder='Status'),
            dbc.Input(id='input-notes', size="md", type='text', placeholder='Notes'),
            dbc.Button('Add Job', id='add-job-btn', color='info', className="me-1", n_clicks=0),
        ], width=12)
    ]),
    html.Br(),
    dash_table.DataTable(
        id='jobs-table',
        columns=[{"name": i, "id": i} for i in columns],
        data=df.to_dict('records'),
        editable=True,
        row_selectable='single',
        row_deletable=True,
        style_table={'overflowX': 'auto'},
        style_cell={
            'color': 'black',
            'backgroundColor': 'white',
            'textAlign': 'center',
            'padding': '10px',
            'border': '1px solid #ddd',
            'fontSize': '14px',
            'fontFamily': 'Arial, sans-serif'
        }
    )
])


@callback(
    Output('jobs-table', 'data'),
    Input('add-job-btn', 'n_clicks'),
    State('date-applied', 'value'),
    State('input-company', 'value'),
    State('input-position', 'value'),
    State('input-status', 'value'),
    State('input-notes', 'value'),
    
    prevent_initial_call=True
)

def add_job(n_clicks, date_applied, company, position, status, notes):
    if not company or not position or not status:
        return app._jobs.to_dict('records')
    new_row = {
        'Date Applied': date_applied,
        'Company' : company, 
        'Position': position, 
        'Status': status,
        'Notes': notes}
    app._jobs = pd.concat([app._jobs, pd.DataFrame([new_row])], ignore_index=True)
    #add to CSV
    app._jobs.to_csv(data_path, index=False)
    return app._jobs.to_dict('records')

def update_job_status(n_clicks, row_index, new_status):
    if n_clicks > 0 and row_index is not None:
        app._jobs.at[row_index, 'Status'] = new_status
    return app._jobs.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)
