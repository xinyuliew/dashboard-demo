import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from pages.side_bar import sidebar
from pages.menubar import menubar
from pages.footer import footer


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, ], use_pages=True, 
                suppress_callback_exceptions=True)


server = app.server  # This is required for gunicorn

from pages.overview import overview_layout
from pages.analysis import discourse_analysis_layout
from pages.settings import settings_layout
from pages.account import account_layout
from pages.support import support_layout
from pages.sources import sources_layout
from pages.login import login_layout


dash.page_container = html.Div()

# Define the app layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # Handle URL changes
    sidebar(),  # Sidebar component
    html.Div(id="menubar-content"),  # Div for menubar content
    html.Div(id="page-content"),  # Div for main page content
    html.Div(id="login-page-container", style={"display": "none"}),  # Separate container for login page (hidden by default)
    html.Div(id="footer-container"),  # Footer container
    dash.page_container,  # Page container for dynamic page loading
])

# Callback to render content, menubar, and handle visibility of login page, sidebar, footer
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

    # For normal pages (non-login)
    if pathname == "/":
        content = overview_layout()
        menubar_content = menubar("Overview")
        footer_style = footer()
    elif pathname == "/discourse_analysis":
        content = discourse_analysis_layout()
        menubar_content = menubar("Discourse Analysis")
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
        login_page_content = login_layout()  # Custom login page layout
        login_page_style = {"display": "block"}  # Show login page layout
        menubar_content = None  # Hide the menubar on the login page
        footer_style = None  # Hide the footer on the login page
        sidebar_style = {"display": "none"}  # Hide the sidebar on the login page
    else:
        content = html.Div("Error 404 - Page not found")
        menubar_content = None
        footer_style = footer()

    return content, menubar_content, login_page_content, login_page_style, footer_style, sidebar_style

# Callback to toggle sidebar visibility (already handled in render_page_content)
@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"  # Collapse sidebar when toggled
    return ""

# Callback to toggle demo alert visibility
@app.callback(
    Output("demo-alert", "is_open"),
    [Input("alert-toggle", "n_clicks")],
    [State("demo-alert", "is_open")],
)
def toggle_alert(n, is_open):
    if n:
        return not is_open  # Toggle alert visibility
    return is_open

# Callback to toggle navbar collapse
@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open  # Toggle collapse state of navbar
    return is_open

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)