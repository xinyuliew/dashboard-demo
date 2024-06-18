import dash_bootstrap_components as dbc
from dash import html

def menubar(title="NavbarSimple"):
    
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(html.I(className="bi bi-bell"), href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Welcome!", header=True),
                    dbc.DropdownMenuItem([html.I(className="bi bi-person-circle"), "My account"], href="#"),
                    dbc.DropdownMenuItem([html.I(className="bi bi-gear"), "Settings"], href="#"),
                    dbc.DropdownMenuItem([html.I(className="bi bi-globe"), "Support"], href="#"),
                    dbc.DropdownMenuItem([html.I(className="bi bi-box-arrow-in-right"), "Logout"], href="#"),
                ],
                nav=True,
                in_navbar=True,
                label=[html.Img(src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img (31).webp", height="25", alt="Avatar", className="profile_img"),"Judy Stevenson"],
                align_end=True
            ),
        ],
        brand=title,
        brand_href="#",
        color="primary",
        dark=True,
        className="menubar"
    )
