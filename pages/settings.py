import dash
from dash import html, dcc

import dash_bootstrap_components as dbc
# Initialize Dash app
dash.register_page(__name__, path='/settings')


def settings_layout():
    layout = html.Div([
        dbc.Container([
            # General Settings Card
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("General Settings")),
                        dbc.CardBody([
                            html.Label("Dashboard Title", className="form-label"),
                            dbc.Input(type="text", id="dashboard-title", placeholder="Enter dashboard title", className="mb-3"),
                            
                            html.Label("Theme", className="form-label"),
                            dcc.Dropdown(
                                id="theme-dropdown",
                                options=[
                                    {"label": "Light", "value": "light"},
                                    {"label": "Dark", "value": "dark"},
                                ],
                                value="light",
                                className="mb-3"
                            ),
                        ]),
                    ])
                ], width=12),
            ], className="mb-4"),
            
            # Display Settings Card
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("Display Settings")),
                        dbc.CardBody([
                            html.Label("Show Notifications", className="form-label"),
                            dbc.Checklist(
                                options=[
                                    {"label": "Enable notifications", "value": "notifications"}
                                ],
                                id="notifications-checklist",
                                inline=True,
                                className="mb-3"
                            ),
                            
                            html.Label("Refresh Interval", className="form-label"),
                            dcc.Slider(
                                id="refresh-interval-slider",
                                min=1,
                                max=60,
                                step=1,
                                value=10,
                                marks={i: str(i) + "s" for i in range(1, 61)},
                                className="mb-3"
                            ),
                        ]),
                    ])
                ], width=12),
            ], className="mb-4"),
            
            # Advanced Settings Card
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("Advanced Settings")),
                        dbc.CardBody([
                            html.Label("API Key", className="form-label"),
                            dbc.Input(type="text", id="api-key", placeholder="Enter API key", className="mb-3"),
                            
                            html.Label("Language", className="form-label"),
                            dcc.Dropdown(
                                id="language-dropdown",
                                options=[
                                    {"label": "English", "value": "en"},
                                    {"label": "Spanish", "value": "es"},
                                    {"label": "French", "value": "fr"},
                                ],
                                value="en",
                                className="mb-3"
                            ),
                        ]),
                    ])
                ], width=12),
            ], className="mb-4"),
            
            # Save Button Row
            dbc.Row(
                dbc.Col(
                    dbc.Button("Save Settings", id="save-settings", color="primary", className="mt-4"),
                    width="auto",  # Adjust width so the button is only as wide as needed
                ), className="d-flex justify-content-end"
            ),
        ], fluid=True),
    ])
    
    return layout

layout = settings_layout()