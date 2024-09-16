import dash_bootstrap_components as dbc
from dash import html

def menubar(title="NavbarSimple"):
    return html.Div(
        [
            dbc.Nav(
                [
                    html.Div(title, className="navbar-brand")
                ],
                className="menubar"
            ),
            html.Div(id="navbar-toggler-placeholder")  # Placeholder to ensure no toggler
        ],
        className="menubar-container"
    )
