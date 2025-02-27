import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

def get_icon(icon):
    return DashIconify(icon=icon, height=18)

def sidebar():
    return html.Div(
        [
            dcc.Location(id="side-url", refresh=False),  # Track URL changes
            sidebar_header,
            html.Div(id="blurb"),
            dmc.Flex(
                children=[
                    dmc.TextInput(
                        placeholder="Search", size="sm", style={"width": "100%"}
                    ),
                    dmc.ActionIcon(
                        size="input-sm", children=DashIconify(icon="bi:search")
                    ),
                ],
                align="center",
                justify="space-between",
                style={"width": "100%"}
            ),
         
            dbc.Collapse(
                dbc.Nav(
                    [
                        dmc.NavLink(
                            label="Overview", 
                            color="white", 
                            leftSection=get_icon("uis:analysis"), 
                            href="/", 
                            id="overview-link", 
                            active="exact",  # Only active when the path is exactly "/"
                            variant="filled", 
                            rightSection=DashIconify(icon="tabler-chevron-right")
                        ),
                        dmc.NavLink(
                            label="Detailed Analysis", 
                            color="white", 
                            leftSection=get_icon("ci:chat-conversation-circle"), 
                            href="/detailed_analysis", 
                            id="discourse-link", 
                            active="exact",  # Active only on exact match
                            variant="filled", 
                            rightSection=DashIconify(icon="tabler-chevron-right")
                        ),
                        dmc.NavLink(
                            label="Support", 
                            color="white", 
                            leftSection=get_icon("material-symbols:contact-support-outline"), 
                            href="/support", 
                            id="support-link", 
                            active="exact",  # Active only on exact match
                            variant="filled", 
                            rightSection=DashIconify(icon="tabler-chevron-right")
                        ),
                        dmc.NavLink(
                            label="Sources", 
                            color="white", 
                            leftSection=get_icon("material-symbols:frame-source"), 
                            href="/sources", 
                            id="sources-link", 
                            active="exact",  # Active only on exact match
                            variant="filled", 
                            rightSection=DashIconify(icon="tabler-chevron-right")
                        ),
                    ],
                    vertical=True,
                    pills=True
                ),
                id="collapse",
            ),
        ],
        id="sidebar",
    )

sidebar_header = dbc.Row(
    [
        dbc.Col(html.H2("DiscourseDash")),
        dbc.Col(
            [   
                html.Button(
                    html.I(className="bi bi-list"),
                    className="navbar-toggler",
                    id="navbar-toggle",
                ),
                html.Button(
                    html.I(className="bi bi-list"),
                    className="navbar-toggler",
                    id="sidebar-toggle",
                ),
            ],
            width="auto",
            align="center",
        ),
    ]
)