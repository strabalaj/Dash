from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
import pandas as pd
import os 

#set columns and initialize DataFrame
columns = ['Date Applied', 'Company', 'Position', 'Status', "Notes"]
data_path = "jobs.csv"
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    df = pd.DataFrame(columns = columns)


app = Dash(__name__)

def get_table_data(df):
    data = df.to_dict('records')
    for i, row in enumerate(data):
        data[i]['Edit'] = f'Edit-{i}'
    return data

app.layout = html.Div([
    html.H1('Job Application Tracker', style={
        'textAlign': 'center',
        'color': '#2c3e50',
        'marginTop': '30px'
    }),
    html.Div([
        html.Div([
            dcc.Input(id="date-applied", type='text', placeholder='Date Applied', style={'width': '120px', 'padding': '8px'}),
            dcc.Input(id='input-company', type='text', placeholder='Company', style={'width': '120px', 'padding': '8px'}),
            dcc.Input(id='input-position', type='text', placeholder='Position', style={'width': '120px', 'padding': '8px'}),
            dcc.Dropdown(
                ['Applied', 'Interview', 'Offer', 'Rejected'],
                'Applied',
                id='input-status',
                style={'width': '120px'}
            ),
            dcc.Input(id='input-notes', type='text', placeholder='Notes', style={'width': '120px', 'padding': '8px'}),
            html.Button('Add Job', id='add-job-btn', n_clicks=0, style={
                'backgroundColor': '#2980b9',
                'color': 'white',
                'border': 'none',
                'padding': '10px 20px',
                'borderRadius': '5px',
                'cursor': 'pointer'
            })
        ], style={
            'display': 'flex',
            'gap': '15px',
            'justifyContent': 'center',
            'alignItems': 'center',
            'padding': '20px',
            'backgroundColor': '#f4f6f7',
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px rgba(44,62,80,0.07)'
        }),
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '20px'}),
    html.Div([
        dash_table.DataTable(
            id='jobs-table',
            columns=[{'name': col, 'id': col} for col in columns],
            data=get_table_data(df),
            row_deletable=True,
            style_table={'margin': '20px auto', 'width': '90%'},
            style_header={
                'backgroundColor': '#2980b9',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_cell={
                'textAlign': 'center',
                'padding': '10px',
                'backgroundColor': '#f9f9f9',
                'fontFamily': 'Arial'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f2f6fa'
                }
            ]
        )
    ], style={'marginTop': '30px'})
], style={'backgroundColor': '#ecf0f1', 'minHeight': '100vh', 'paddingBottom': '40px'})


app._jobs = df.copy()

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
