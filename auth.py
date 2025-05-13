import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_auth

# Sample users
VALID_USERNAME_PASSWORD_PAIRS = {
    'testuser': 'testpassword'
}

# Initialize Dash
app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    html.H1('User Authentication Example'),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8070)
