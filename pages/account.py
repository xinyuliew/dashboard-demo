import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from utils import create_notification
# Initialize Dash app
dash.register_page(__name__, path='/account')

def account_layout():
    layout = html.Div([
        dbc.Container([
            dbc.Row([
                    dbc.Col([
                         create_notification("This is a demo version of an account page.")
                    ]),
                ]),
            dbc.Row([
                dbc.Col([
                    # User Information Card
                    dbc.Card([
                        dbc.CardHeader(html.H4("User Information")),
                        dbc.CardBody([
                            html.Label("Username", className="form-label"),
                            dbc.Input(type="text", id="username", placeholder="Enter your username", className="mb-3"),
                            html.Label("Email", className="form-label"),
                            dbc.Input(type="email", id="email", placeholder="Enter your email address", className="mb-3"),
                        ])
                    ], className="mb-4"),  # Add margin-bottom between cards

                    # Change Password Card
                    dbc.Card([
                        dbc.CardHeader(html.H4("Change Password")),
                        dbc.CardBody([
                            html.Label("Current Password", className="form-label"),
                            dbc.Input(type="password", id="current-password", placeholder="Enter your current password", className="mb-3"),
                            html.Label("New Password", className="form-label"),
                            dbc.Input(type="password", id="new-password", placeholder="Enter your new password", className="mb-3"),
                            html.Label("Confirm New Password", className="form-label"),
                            dbc.Input(type="password", id="confirm-new-password", placeholder="Confirm your new password", className="mb-3"),
                        ])
                    ], className="mb-4"),  # Add margin-bottom between cards

                    # Account Settings Card
                    dbc.Card([
                        dbc.CardHeader(html.H4("Account Settings")),
                        dbc.CardBody([
                            html.Label("Preferred Language", className="form-label"),
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
                            html.Label("Timezone", className="form-label"),
                            dcc.Dropdown(
                                id="timezone-dropdown",
                                options=[
                                    {"label": "GMT", "value": "GMT"},
                                    {"label": "EST", "value": "EST"},
                                    {"label": "PST", "value": "PST"},
                                    # Add more timezones as needed
                                ],
                                value="GMT",
                                className="mb-3"
                            ),
                        ])
                    ]),

                    # Save Changes Button Outside the Cards
                    dbc.Row(
                        dbc.Col(
                            dbc.Button("Save Changes", id="save-account-settings", color="primary", className="mt-4"),
                            width="auto",  # Adjust width so the button is as wide as its content
                        ), className="d-flex justify-content-end"
                    )
                ], width=12),  # Full width for the single column
            ]),
        ], fluid=True),
    ])
    
    return layout

layout = account_layout()