import dash
from dash import html
import dash_bootstrap_components as dbc

# Define footer function
def footer():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.P("DiscourseDash", className="text-center text-md-start")
            ], xs=12, sm=12, md=12, lg=3),

            dbc.Col([
                dbc.Nav(
                    [
                        dbc.NavLink("Overview", href="/", active='exact'),
                        dbc.NavLink("Discourse Analysis", href="/discourse_analysis", active='exact'),
                        dbc.NavLink("Support", href="/support", active='exact'),
                        dbc.NavLink("My account", href="/account", active='exact'),
                    ],
                    className="footer-nav d-flex flex-column flex-md-row justify-content-center justify-content-md-end"
                )
            ], xs=12, sm=12, md=12, lg=9),
        ], className="text-center text-md-start mx-auto"),  # Center content on small screens
    ], id="footer", className="py-3")