import yfinance as yf
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
from datetime import datetime, timedelta

dashboard_layout = html.Div([
    html.H1("Market Scope", className="main-heading"),
    html.Div([
        html.Label("Stock Symbol:"),
        dcc.Input(
            id="stock-symbol-input",
            type="text",
            value="AAPL",  # Default symbol
            placeholder="Enter symbol (e.g., AAPL, MSFT)",
            style={"marginRight": "10px"}
        ),
        html.Label("Select desired time range:"),
        dcc.Dropdown(
            id="time-range-dropdown",
            options=[
                {'label': '1 Day', 'value': '1d'},
                {'label': '5 Days', 'value': '5d'},
                {'label': '1 Month', 'value': '30d'},
            ],
            value='1d',
            clearable=False,
            style={"width": "150px", "display": "inline-block", "marginLeft": "10px"}
        ),
    ], style={"marginBottom": "20px"}),
    dcc.Graph(id='stock-price-graph'),
])

def register_callbacks(app):
    @app.callback(
        Output('stock-price-graph', 'figure'),
        [Input('stock-symbol-input', 'value'),
         Input('time-range-dropdown', 'value')]
    )
    def update_graph(symbol, selected_time_range):
        end_date = datetime.now()
        if selected_time_range == '1d':
            start_date = end_date - timedelta(days=1)
        elif selected_time_range == '5d':
            start_date = end_date - timedelta(days=5)
        elif selected_time_range == '30d':
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=30)

        # Fetch stock data
        try:
            stock_data = yf.download(symbol, start=start_date, end=end_date)
            if stock_data.empty:
                raise ValueError("No data found for symbol.")
            figure = go.Figure(data=[
                go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines+markers')
            ])
            figure.update_layout(
                title=f'{symbol.upper()} Stock Price Over Time',
                xaxis_title='Date',
                yaxis_title='Price (USD)'
            )
        except Exception as e:
            figure = go.Figure()
            figure.update_layout(
                title=f"Error: {str(e)}",
                xaxis_title='Date',
                yaxis_title='Price (USD)'
            )
        return figure

