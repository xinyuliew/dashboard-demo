import dash_bootstrap_components as dbc
from dash import html
from dash import Input, Output, html, callback
from dash_iconify import DashIconify
import dash_mantine_components as dmc

def menubar(title="NavbarSimple"):
    return html.Div(
            dbc.Navbar(
                dbc.Container(
                    [   
                        dbc.NavbarBrand(title, className="me-auto"),
                        dmc.Menu(
                            [
                                dmc.MenuTarget(dmc.Button("My account", rightSection=DashIconify(icon="icon-park-solid:down-one"))),
                                dmc.MenuDropdown(
                                    [   
                                        dmc.MenuItem(
                                            "My Account", leftSection=DashIconify(icon="tabler:user-circle"), 
                                        ),
                                        dmc.MenuItem("Settings", leftSection=DashIconify(icon="tabler:settings")),
                                        dmc.MenuItem("Messages", leftSection=DashIconify(icon="tabler:message")),
                                        dmc.MenuItem("Gallery", leftSection=DashIconify(icon="tabler:photo")),
                                        dmc.MenuItem("Search", leftSection=DashIconify(icon="tabler:search")),
                                        dmc.MenuDivider(),
                                        dmc.MenuItem("Transfer my data", leftSection=DashIconify(icon="tabler:arrows-left-right")),
                                        dmc.MenuItem(
                                            "Delete my account",
                                            leftSection=DashIconify(icon="tabler:trash"),
                                            color="red",
                                        ),
                                        dmc.MenuDivider(),
                                        dmc.MenuItem(
                                            "Logout", leftSection=DashIconify(icon="material-symbols:logout-rounded"), color="blue", href="/login"
                                        ),
                                    ]
                                ),
                            ],
                            trigger="click",
                            position="bottom-end",
                        ),
                    ]
                ),
            )
            
        )


@callback(
    Output("button-clicks", "children"), 
    [Input("button-link", "n_clicks")]
)
def show_clicks(n):
    return "Button clicked {} times".format(n)
    