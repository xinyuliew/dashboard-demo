import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from utils import create_notification
import dash_mantine_components as dmc
# Initialize Dash app
dash.register_page(__name__, path='/support')

def support_layout():
    layout = html.Div([
            dbc.Row([
                    dbc.Col([
                         create_notification("This is a demo version of a support page.")
                    ]),
                ]),
            # Contact Information Card
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("Contact Information")),
                        dbc.CardBody([
                            dmc.Stack(
                                children=[
                                    dmc.TextInput(label="Your Name"),
                                    dmc.TextInput(label="Email Address"),
                                    dmc.TextInput(label="Phone Number"),
                                    ],
                            ),
                        ]),
                    ])
                ], width=12),
            ]),
            
            # Issue Reporting Card
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("Report an Issue")),
                        dbc.CardBody([
                            dmc.Stack(
                                children=[
                                    dmc.Select(
                                        label="Issue Category",
                                        data=[
                                            {"label": "Bug", "value": "bug"},
                                            {"label": "Feature Request", "value": "feature"},
                                            {"label": "Other", "value": "other"},
                                        ],
                                        value="bug",
                                    ),
                                    dmc.TextInput(
                                        label="Describe the Issue",
                                        placeholder="Describe your issue or request in detail",
                                    ),
                                    ],
                            ),
                        ]),
                    ])
                ], width=12),
            ]),
            
            # Feedback Card
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("Feedback")),
                        dbc.CardBody([
                             dmc.Stack(
                                children=[
                                    dmc.Text("Rate Your Experience", size="md"),
                                    dmc.Slider(
                                        label="Rate",
                                        value=[1, 5],  # This defines a range from 1 to 5
                                        marks=[
                                            {"value": 1, "label": "1"},
                                            {"value": 2, "label": "2"},
                                            {"value": 3, "label": "3"},
                                            {"value": 4, "label": "4"},
                                            {"value": 5, "label": "5"}
                                        ],
                                        step=1,  # Allows movement only between integer values
                                        min=1,  # Minimum value
                                        max=5,  # Maximum value
                                    ),
                                    # add a break here
                                    html.Br(),
                                    dmc.TextInput(
                                        label="Additional Comments",
                                        placeholder="Share any additional feedback",
                                    ),
                                    ],
                            ),
                        ]),
                    ])
                ], width=12),
            ], className="mb-4"),
            
            # Submit Button Row
            dbc.Row(
                dbc.Col(
                    dbc.Button("Submit", id="submit-support", color="primary", className="button"),
                    width="auto",  # Adjust width so the button is only as wide as needed
                ), className="d-flex justify-content-end"
            ),
    ])
    
    return layout

layout=support_layout