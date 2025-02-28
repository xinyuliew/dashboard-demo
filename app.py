import dash
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from flask_compress import Compress

# Importing components
from pages.side_bar import sidebar
from pages.menubar import menubar
from pages.footer import footer
from dash import Dash, _dash_renderer
_dash_renderer._set_react_version("18.2.0")

# Enable compression
app = dash.Dash(
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
        dbc.icons.BOOTSTRAP,
        dmc.styles.DATES
    ],
    use_pages=True,
    suppress_callback_exceptions=True
)
server = app.server
Compress(app.server)  # Enables gzip compression

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
    footer_style = footer()  

    if pathname == "/login":
        return None, None, login_layout(), {"display": "block"}, None, {"display": "none"}

    page_map = {
        "/": ("Overview", overview_layout),
        "/detailed_analysis": ("Detailed Analysis", discourse_analysis_layout),
        "/account": ("My Account", account_layout),
        "/support": ("Support", support_layout),
        "/sources": ("Sources", sources_layout),
    }

    if pathname in page_map:
        menubar_text, layout_func = page_map[pathname]
        return layout_func(), menubar(menubar_text), None, {"display": "none"}, footer_style, {"display": "block"}

    return html.Div("Error 404 - Page not found"), None, None, {"display": "none"}, footer_style, {"display": "block"}


app.clientside_callback(
    """
    function(n, classname) {
        return n && classname === '' ? 'collapsed' : '';
    }
    """,
    Output("sidebar", "className"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar", "className"),
)

app.clientside_callback(
    """
    function(n, is_open) {
        return n ? !is_open : is_open;
    }
    """,
    Output("collapse", "is_open"),
    Input("navbar-toggle", "n_clicks"),
    State("collapse", "is_open"),
)

app.clientside_callback(
    """
    function(pathname) {
        return [
            pathname === "/",
            pathname === "/detailed_analysis",
            pathname === "/support",
            pathname === "/sources"
        ];
    }
    """,
    [
        Output("overview-link", "active"),
        Output("discourse-link", "active"),
        Output("support-link", "active"),
        Output("sources-link", "active"),
    ],
    Input("side-url", "pathname"),
)
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)