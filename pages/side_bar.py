import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc


def sidebar():
    return html.Div(
    [
        html.H2([html.I(className="bi bi-clipboard-data"), "   Dashboard"], className="display-6"),
        html.Hr(className="sidebar-divider"),
        dbc.InputGroup(
                [
                    dbc.Input(id="input", placeholder="Search", type="text", className="search_text"),
                    dbc.InputGroupText(html.I(className="bi bi-search"), className="search_icon"),
                ]
            ),
        html.Br(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="bi bi-grid"), "  Overview",], 
                        href="/", 
                        active="exact"),
                dbc.NavLink(
                    [html.I(className="bi bi-graph-up"), "  Discourse Analysis"], 
                    href="/discourse_analysis", 
                    active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)
