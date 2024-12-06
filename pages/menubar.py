import dash_bootstrap_components as dbc
from dash import html
from dash import Input, Output, html, callback


def menubar(title="NavbarSimple"):
    return html.Div(
            dbc.Navbar(
                dbc.Container(
                    [
                        # Left-aligned item (e.g., a title or logo)
                        dbc.NavbarBrand(title, className="me-auto"),
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem(
                                    dbc.NavLink(
                                        [html.I(className="bi bi-person-circle"), "   My account"], 
                                        href="/account"
                                    )
                                ),
                                dbc.DropdownMenuItem(
                                    dbc.NavLink(
                                        [html.I(className="bi bi-box-arrow-right"), "   Logout"], 
                                        href="/logout"
                                    )
                                ),
                            ],
                            label="My Account",  # Label for the dropdown menu
                            align_end=True
                        )
                    ]
                ),
            )
            
        )


@callback(
    Output("button-clicks", "children"), [Input("button-link", "n_clicks")]
)
def show_clicks(n):
    return "Button clicked {} times".format(n)