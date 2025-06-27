from dash import dash, html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
import random


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Computer Number Guessing Game"),
    html.P("You will try to guess the computer's number (1-100)!"),
    #storing random number
    dcc.Store(id='random_number', data=random.randint(1,100)),
    html.Button('Generate Random Number', id={'type': 'button-storage', 'index': 'memory'}),
    html.Br(),
    html.Br(),
    dbc.Input(id="user_number", placeholder="Enter a guess!", ),
    html.Br(),
    html.P(id="computer_response"),
])

@callback(
    Output(component_id='computer_response', component_property='children'),
    Input(component_id='user_number', component_property='value'),
    Input(component_id='random_number', component_property='data')
)
def guessing_game(input_value, input_data):
    if input_data is None:
        return f'Waiting for you to generate a random number'
    if input_value is None:
        return f'Waiting for you to enter a number!'
    try:
        random_num = int(input_data) 
        guess_value = int(input_value)
        if guess_value < random_num:
            return f'Your Guess of: {input_value} is too low!'
        elif guess_value > random_num:
            return f'Your Guess of: {input_value} is too high!'
        else:
            return f'Your Guess of: {input_value} is correct!'
    except ValueError:
        return f'You can only enter whole numbers in this game partner'
    

if __name__ == '__main__':
    app.run(debug=True)
    