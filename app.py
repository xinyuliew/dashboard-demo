import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from pages.side_bar import sidebar
from pages.menubar import menubar


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], use_pages=True, 
                suppress_callback_exceptions=True)


server = app.server  # This is required for gunicorn

from pages.overview import overview_layout
from pages.analysis import discourse_analysis_layout

dash.page_container = html.Div()

app.layout = html.Div([dcc.Location(id="url", refresh=False), 
                       sidebar(),  
                       html.Div(id="menubar-content"),  # Div for menubar
 
                       html.Div(id="page-content"), dash.page_container])

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
    else:
        content = html.Div("404 - Page not found")
        title = "Page not found"

    menubar_content = menubar(title)  # Create the menubar with the appropriate title
    return content, menubar_content

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)