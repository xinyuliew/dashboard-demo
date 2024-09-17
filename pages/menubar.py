import dash_bootstrap_components as dbc
from dash import html

def menubar(title="NavbarSimple"):
    return html.Div(
        [
            dbc.Nav(
                [
                    html.Div(title, className="navbar-brand")
                ],
            ),
            
        ],
    )
