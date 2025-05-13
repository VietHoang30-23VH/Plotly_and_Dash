import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_auth

# Load Titanic dataset
df = pd.read_csv('titanic.csv')

# Set up basic authentication
VALID_USERNAME_PASSWORD_PAIRS = {
    'user': 'testpassword'
}

# Initialize Dash app with suppress_callback_exceptions=True
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE], suppress_callback_exceptions=True)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.title = 'Titanic Dashboard'

# Navbar with custom hover effects
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("Titanic Dashboard", className="ms-2"),
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Data Overview", href="/data-overview")),
            dbc.NavItem(dbc.NavLink("Visualizations", href="/visualization")),
            dbc.NavItem(dbc.NavLink("Settings", href="/settings")),
        ], className="ml-auto", navbar=True)
    ]),
    className="navbar-custom mb-4"
)

# Home Page with Background Image and Centered Text
home_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H2("Welcome to the Titanic Dashboard", className="text-center text-light mt-3"),
            html.P("This dashboard allows you to explore the Titanic dataset and analyze various aspects of the tragic event. "
                   "Use the navigation bar to explore different features.", className="text-center text-light")
        ], style={'background-color': 'rgba(0, 0, 0, 0.6)', 'padding': '20px', 'border-radius': '10px'}))
    ], align="center", className="vh-100 d-flex justify-content-center align-items-center", style={
        'background-image': 'url(TITANICSS.jpg)',
        'background-size': 'cover',
        'background-position': 'center'
    })
])


data_overview_description = html.Div(children=[
    html.Div(children=[
        html.H2('Titanic Dataset Overview'),
        html.P("The sinking of the Titanic is one of the most infamous maritime disasters in history. "
               "On April 15, 1912, during her maiden voyage, the Titanic sank after colliding with an iceberg. "
               "While there was some element of luck involved in who survived, the ship's design, the weather, "
               "and human error all played a role."),
        html.Br(),
        html.P("On April 15, 1912, during her maiden voyage, the Titanic sank after colliding with an iceberg. "
               "There was some element of luck involved in who survived, but it is evident that some groups of "
               "people were more likely to survive than others.")
    ]),
    html.Div(children=[
        html.Br(),
        html.H2('Data Variables'),
        html.Br(),
        html.B('Survival: '), "0 = No, 1 = Yes",
        html.Br(),
        html.B('Pclass: '), "Ticket class (1 = 1st Class, 2 = 2nd Class, 3 = 3rd Class)",
        html.Br(),
        html.B('Sex: '), "Sex",
        html.Br(),
        html.B('Age: '), "Age in years",
        html.Br(),
        html.B('SibSp: '), "Number of siblings/spouses aboard",
        html.Br(),
        html.B('Parch: '), "Number of parents/children aboard",
        html.Br(),
        html.B('Ticket: '), "Ticket Number",
        html.Br(),
        html.B('Fare: '), "Passenger fare",
        html.Br(),
        html.B('Cabin: '), "Cabin number",
        html.Br(),
        html.B('Embarked: '), "Port of Embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)"
    ])
])

# data overview layout
data_overview_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H3("Data Overview", className="text-center text-primary mt-3")),
    ]),
    dbc.Row([
        dbc.Col(html.P("Explore the Titanic dataset in detail.", className="text-center")),
    ]),
    dbc.Row([
        dbc.Col(data_overview_description, width=12)  # This adds your new descriptive content
    ]),
    dbc.Row([
        dbc.Col(html.Div([
            dcc.Graph(id='data-table')
        ]), width=12)
    ])
])



@app.callback(
    Output('data-table', 'figure'),
    Input('url', 'pathname')
)
def update_table(pathname):
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[col] for col in df.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    return fig

# Visualization Page
advanced_viz_1_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H3("Survival Analysis by Class", className="text-center text-primary mt-3")),
        dbc.Col(dcc.Graph(
            id='survival-class-bar',
            figure=px.bar(df, x='Pclass', y='Survived', color='Sex', barmode='group', 
                          title='Survival Rate by Class and Gender')
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H3("Age Distribution of Passengers", className="text-center text-primary mt-5")),
        dbc.Col(dcc.Graph(
            id='age-distribution',
            figure=px.histogram(df, x='Age', nbins=30, title='Age Distribution')
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H3("Passenger Class Distribution", className="text-center text-primary mt-5")),
        dbc.Col(dcc.Graph(
            id='class-distribution',
            figure=px.pie(df, names='Pclass', title='Passenger Class Distribution')
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H3("Survival Rate by Age", className="text-center text-primary mt-5")),
        dbc.Col(dcc.Graph(
            id='survival-rate-age',
            figure=px.histogram(df, x='Age', y='Survived', histfunc='avg', title='Survival Rate by Age')
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H3("Survival Rate by Age and Class (Animated)", className="text-center text-primary mt-5")),
        dbc.Col(dcc.Graph(
            id='survival-rate-age-class-animated',
            figure=px.scatter(df, x='Age', y='Fare', animation_frame='Pclass', animation_group='Sex', 
                              size='Survived', color='Survived', hover_name='Name',
                              title='Survival Rate by Age and Class (Animated)')
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H3("Survival Over Time (Animated)", className="text-center text-primary mt-5")),
        dbc.Col(dcc.Graph(
            id='survival-over-time',
            figure=px.line(df, x='Age', y='Survived', animation_frame='Pclass', 
                           title='Survival Over Time (Animated)')
        ), width=12)
    ])
])

# Settings Page
settings_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H3("Dashboard Settings", className="text-center text-primary mt-3")),
    ]),
    dbc.Row([
        dbc.Col(html.Div([
            html.Label("Select Theme:"),
            dcc.Dropdown(
                id='theme-dropdown',
                options=[{'label': 'Bootstrap', 'value': dbc.themes.BOOTSTRAP},
                         {'label': 'Darkly', 'value': dbc.themes.DARKLY}],
                value=dbc.themes.BOOTSTRAP,
                clearable=False
            )
        ]), width=6)
    ]),
    dbc.Row([
        dbc.Col(dbc.Button("Apply Theme", id="apply-theme-button", color="primary", className="mt-3"), width=6),
    ])
])

@app.callback(
    Output('page-content', 'style'),
    Input('apply-theme-button', 'n_clicks'),
    State('theme-dropdown', 'value')
)
def update_theme(n_clicks, selected_theme):
    if n_clicks:
        app.external_stylesheets = [selected_theme]
    return {'backgroundColor': selected_theme}

# Main Layout with Multi-page Navigation
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
], fluid=True)

# Update page content based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home_layout
    elif pathname == '/data-overview':
        return data_overview_layout
    elif pathname == '/visualization':
        return advanced_viz_1_layout
    elif pathname == '/settings':
        return settings_layout
    else:
        return home_layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
