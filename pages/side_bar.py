import dash
from dash import html
import dash_bootstrap_components as dbc


def sidebar():
    return html.Div(
    [
        sidebar_header,
        html.Div(
            [
            ],
            id="blurb",
        ),
        dbc.InputGroup(
                [
                    dbc.Input(id="input", placeholder="Search", type="text", className="search_text"),
                    dbc.InputGroupText(html.I(className="bi bi-search"), className="search_icon"),
                ]
            ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink([html.I(className="bi bi-grid"), "   Overview"], href="/", id="page-1-link", active='exact'),
                    dbc.NavLink([html.I(className="bi bi-graph-up"), "   Discourse Analysis"], href="/discourse_analysis", id="page-2-link", active='exact'),
                    #dbc.NavLink([html.I(className="bi bi-gear"), "   Settings"], href="/settings", id="page-3-link", active='exact'),
                    dbc.NavLink([html.I(className="bi bi-chat-right-dots"), "   Support"], href="/support", id="page-5-link", active='exact'),
                    dbc.NavLink([html.I(className="bi bi-info-square"), "   Sources"], href="/sources", id="page-6-link", active='exact'),
                ],
                vertical=True,
                pills=True,
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
                    # use the Bootstrap navbar-toggler classes to style
                    html.I(className="bi bi-list"),
                    className="navbar-toggler",
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.I(className="bi bi-list"),
                    className="navbar-toggler",
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

