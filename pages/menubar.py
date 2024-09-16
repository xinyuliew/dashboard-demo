import dash_bootstrap_components as dbc
from dash import html

def menubar(title="NavbarSimple"):
    
    return dbc.NavbarSimple(
        
        brand=title,
        brand_href="#",
        color="primary",
        dark=True,
        className="menubar"
    )
