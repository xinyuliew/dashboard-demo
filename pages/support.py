import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from utils import create_notification
# Initialize Dash app
dash.register_page(__name__, path='/support')

def support_layout():
    layout = html.Div([
        dbc.Container([
            dbc.Row([
                    dbc.Col([
                         create_notification("This is a demo version of a settings page.")
                    ]),
                ]),
            # Contact Information Card
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("Contact Information")),
                        dbc.CardBody([
                            html.Label("Email", className="form-label"),
                            dbc.Input(type="email", id="support-email", placeholder="Enter your email", className="mb-3"),
                            
                            html.Label("Phone", className="form-label"),
                            dbc.Input(type="text", id="support-phone", placeholder="Enter your phone number (optional)", className="mb-3"),
                            
                            html.Label("Preferred Contact Method", className="form-label"),
                            dcc.Dropdown(
                                id="contact-method-dropdown",
                                options=[
                                    {"label": "Email", "value": "email"},
                                    {"label": "Phone", "value": "phone"},
                                ],
                                value="email",
                                className="mb-3"
                            ),
                        ]),
                    ])
                ], width=12),
            ], className="mb-4"),
            
            # Issue Reporting Card
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("Report an Issue")),
                        dbc.CardBody([
                            html.Label("Issue Category", className="form-label"),
                            dcc.Dropdown(
                                id="issue-category-dropdown",
                                options=[
                                    {"label": "Bug", "value": "bug"},
                                    {"label": "Feature Request", "value": "feature"},
                                    {"label": "Other", "value": "other"},
                                ],
                                value="bug",
                                className="mb-3"
                            ),
                            
                            html.Label("Describe the Issue", className="form-label"),
                            dbc.Textarea(
                                id="issue-description",
                                placeholder="Describe your issue or request in detail",
                                className="mb-3"
                            ),
                        ]),
                    ])
                ], width=12),
            ], className="mb-4"),
            
            # Feedback Card
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("Feedback")),
                        dbc.CardBody([
                            html.Label("Rate Your Experience", className="form-label"),
                            dcc.Slider(
                                id="feedback-rating",
                                min=1,
                                max=5,
                                step=1,
                                value=3,
                                marks={i: str(i) for i in range(1, 6)},
                                className="mb-3"
                            ),
                            
                            html.Label("Additional Comments", className="form-label"),
                            dbc.Textarea(
                                id="feedback-comments",
                                placeholder="Share any additional feedback",
                                className="mb-3"
                            ),
                        ]),
                    ])
                ], width=12),
            ], className="mb-4"),
            
            # Submit Button Row
            dbc.Row(
                dbc.Col(
                    dbc.Button("Submit", id="submit-support", color="primary", className="mt-4"),
                    width="auto",  # Adjust width so the button is only as wide as needed
                ), className="d-flex justify-content-end"
            ),
        ], fluid=True),
    ])
    
    return layout

layout=support_layout