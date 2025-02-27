import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from pages.side_bar import sidebar
from pages.menubar import menubar
from pages.footer import footer
import dash_mantine_components as dmc
from dash import Dash, _dash_renderer
_dash_renderer._set_react_version("18.2.0")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, dmc.styles.ALL, dmc.styles.DATES], use_pages=True, 
                suppress_callback_exceptions=True)


server = app.server  

from pages.overview import overview_layout
from pages.analysis import discourse_analysis_layout
from pages.settings import settings_layout
from pages.account import account_layout
from pages.support import support_layout
from pages.sources import sources_layout
from pages.login import login_layout

dash.page_container = html.Div()

app.layout = dmc.MantineProvider(
    html.Div([
    dcc.Location(id="url", refresh=False),  
    sidebar(),  
    html.Div(id="menubar-content"),  
    html.Div(id="page-content"),  
    html.Div(id="login-page-container", style={"display": "none"}),  
    html.Div(id="footer-container"), 
    dash.page_container,  
])
)

@app.callback(
    [Output("page-content", "children"),
     Output("menubar-content", "children"),
     Output("login-page-container", "children"),
     Output("login-page-container", "style"),
     Output("footer-container", "children"),
     Output("sidebar", "style")],
    [Input("url", "pathname")],
)
def render_page_content(pathname):
    content, menubar_content, login_page_content, login_page_style, footer_style, sidebar_style = None, None, None, {"display": "none"}, None, {"display": "block"}
    if pathname == "/":
        content = overview_layout()
        menubar_content = menubar("Overview")
        footer_style = footer()
    elif pathname == "/detailed_analysis":
        content = discourse_analysis_layout()
        menubar_content = menubar("Detailed Analysis")
        footer_style = footer()
    elif pathname == "/account":
        content = account_layout()
        menubar_content = menubar("My account")
        footer_style = footer()
    elif pathname == "/support":
        content = support_layout()
        menubar_content = menubar("Support")
        footer_style = footer()
    elif pathname == "/sources":
        content = sources_layout()
        menubar_content = menubar("Sources")
        footer_style = footer()
    elif pathname == "/login":
        login_page_content = login_layout() 
        login_page_style = {"display": "block"} 
        menubar_content = None
        footer_style = None  
        sidebar_style = {"display": "none"} 
    else:
        content = html.Div("Error 404 - Page not found")
        menubar_content = None
        footer_style = footer()

    return content, menubar_content, login_page_content, login_page_style, footer_style, sidebar_style

@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"  
    return ""

@app.callback(
    Output("demo-alert", "is_open"),
    [Input("alert-toggle", "n_clicks")],
    [State("demo-alert", "is_open")],
)
def toggle_alert(n, is_open):
    if n:
        return not is_open 
    return is_open

@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open  
    return is_open

@app.callback(
    [
        Output("overview-link", "active"),
        Output("discourse-link", "active"),
        Output("support-link", "active"),
        Output("sources-link", "active"),
    ],
    [Input("side-url", "pathname")],
)
def update_active_link(pathname):
    return (
        pathname == "/",
        pathname == "/detailed_analysis",
        pathname == "/support",
        pathname == "/sources",
    )

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)