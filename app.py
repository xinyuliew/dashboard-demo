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


dash.page_container = html.Div()

app.layout = html.Div([
                       dcc.Location(id="url", refresh=False),            
                       sidebar(),
                       html.Div(id="menubar-content"),  # Div for menubar
                       html.Div(id="page-content"), 
                       dash.page_container,
                       footer()
                       ])

@app.callback(
    [Output("page-content", "children"),
     Output("menubar-content", "children")],  # Update menubar content
    [Input("url", "pathname")],
)
def render_page_content(pathname):
    if pathname == "/":
        content = overview_layout()
        title = "Overview"
    elif pathname == "/discourse_analysis":
        content = discourse_analysis_layout()
        title = "Discourse Analysis"
    #elif pathname == "/settings":
    #    content = settings_layout()
    #    title = "Settings"
    elif pathname == "/account":
        content = account_layout()
        title = "My account"
    elif pathname == "/support":
        content = support_layout()
        title = "Support"
    elif pathname == "/sources":
        content = sources_layout()
        title = "Sources"
    else:
        content = html.Div("Error 404 - Page not found")
        title = "Page not found"

    menubar_content = menubar(title)  # Create the menubar with the appropriate title
    return content, menubar_content

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

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)