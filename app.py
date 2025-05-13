import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = dash.Dash(__name__)

# Define the layout using html.Div with additional styles
app.layout = html.Div(className='container', children=[
    html.H1('My Interactive Dashboard', style={'textAlign': 'center', 'color': '#0074D9'}),
    html.Div('Welcome to my interactive Dash dashboard.', className='center-text', style={'fontSize': '20px'}),
    html.Div([
        html.Label('Dropdown:', className='bold-label'),
        dcc.Dropdown(
            id='my-dropdown',
            options=[
                {'label': 'Option 1', 'value': 'opt1'},
                {'label': 'Option 2', 'value': 'opt2'}
            ],
            value='opt1',  # Default value
            style={'marginBottom': '20px'}
        )
    ]),
    html.Div(id='output-div', className='center-text', style={'fontSize': '20px'}),
    html.Div([
        html.Label('Graph:', className='bold-label'),
         dcc.Graph(id='example-graph')
    ], style={'marginTop': '20px'})
])
# Define the callback to update the output text
@app.callback(
    Output('output-div', 'children'),
    [Input('my-dropdown', 'value')]
)
def update_output_div(selected_value):
    return f'You have selected {selected_value}'

# Define the callback to update the graph
@app.callback(
    Output('example-graph', 'figure'),
    [Input('my-dropdown', 'value')]
)
def update_graph(selected_value):
    if selected_value == 'opt1':
        data = [
            go.Bar(x=[1, 2, 3], y=[4, 1, 2], name='Option 1 Data')
        ]
    else:
        data = [
            go.Bar(x=[1, 2, 3], y=[2, 4, 5], name='Option 2 Data')
        ]
    
    return {
        'data': data,
        'layout': go.Layout(title='Example Graph')
    }
if __name__ == '__main__':
    app.run_server(debug=True, port = 8053)