from dash import dcc, html, Input, Output, State, callback
from utils import get_supabase_client, add_user, verify_user
import dash
import dash_bootstrap_components as dbc

# Initialize Dash app
dash.register_page(__name__, path='/login')

# Initialize Supabase client
supabase = get_supabase_client()

# Define the login layout
def login_layout():
    layout = html.Div([
        dbc.Row([
            dbc.Col([
                 dbc.Card([
                    dbc.CardHeader(html.H2("DiscourseDash")),
                    dbc.CardBody(
                        dbc.Tabs([
                                dbc.Tab([
                                        # Form Inputs
                                        dcc.Input(
                                            id="login-email", 
                                            type="email", 
                                            placeholder="Enter your email", 
                                            className="form-control mb-3",
                                        ),
                                        dcc.Input(
                                            id="login-password", 
                                            type="password", 
                                            placeholder="Enter your password", 
                                            className="form-control mb-3",
                                        ),
                                        
                                        # Login Button
                                        html.Button(
                                            "Login", 
                                            id="login-button", 
                                            n_clicks=0, 
                                            className="button"
                                        ),
                                        
                                        # Feedback message (Error or Success)
                                        html.Div(
                                            id="login-feedback"
                                        )
                                ],
                                 label="Login"),
                                dbc.Tab([
                                        # Form Inputs for Registration
                                        dcc.Input(
                                            id="register-firstname", 
                                            type="text", 
                                            placeholder="Enter your first name", 
                                            className="form-control mb-3",
                                        ),
                                        dcc.Input(
                                            id="register-lastname", 
                                            type="text", 
                                            placeholder="Enter your last name", 
                                            className="form-control mb-3",
                                        ),
                                        dcc.Input(
                                            id="register-email", 
                                            type="email", 
                                            placeholder="Enter your email", 
                                            className="form-control mb-3",
                                        ),
                                        dcc.Input(
                                            id="register-password", 
                                            type="password", 
                                            placeholder="Enter your password", 
                                            className="form-control mb-3",
                                        ),
                                        dcc.Input(
                                            id="register-confirm-password", 
                                            type="password", 
                                            placeholder="Confirm your password", 
                                            className="form-control mb-3",
                                        ),
                                        
                                        # Register Button
                                        html.Button(
                                            "Register", 
                                            id="register-button", 
                                            n_clicks=0, 
                                            className="button"
                                        ),
                                        
                                        # Feedback message (Error or Success)
                                        html.Div(
                                            id="register-feedback"
                                        ),
                                    ], 
                                    label="Sign Up"),
                            ],
                        className="nav-fill"), 
                    ),
                 ]),
            ], xs=10, sm=10, md=8, lg=4),  # Center the form horizontally
        ], justify="center"),  # Center the row horizontally
    ], className="justify-content-center align-items-center", id="login")  # Vertically and horizontally center the page
    
    return layout
layout = login_layout

@callback(
    [Output("login-feedback", "children"),
     Output("register-feedback", "children")],
    [Input("login-button", "n_clicks"),
     Input("register-button", "n_clicks")],
    [State("login-email", "value"),
     State("login-password", "value"),
     State("register-firstname", "value"),
     State("register-lastname", "value"),
     State("register-email", "value"),
     State("register-password", "value"),
     State("register-confirm-password", "value")],
    prevent_initial_call=True,
)
def handle_login_or_register(n_clicks_login, n_clicks_register, email, password, firstname, lastname, register_email, register_password, confirm_password):
    # Initialize default values for both login and registration feedback
    login_message = ""
    register_message = ""

    # Handle login feedback
    if n_clicks_login > 0:
        if not email or not password:
            login_message = "Please provide both email and password."
        else:
            login_result = handle_login(email, password)
            login_message = login_result
            
    # Handle registration feedback
    if n_clicks_register > 0:
        if not register_email or not register_password or not confirm_password:
            register_message = "Please provide all fields to register."
        elif register_password != confirm_password:
            register_message = "Passwords do not match. Please try again."
        else:
            register_result = handle_register(firstname, lastname, register_email, register_password)
            register_message = register_result
            if "successful" in register_result:
                # After successful registration, log the user in and redirect to the dashboard
                login_result, login_redirect = handle_login(register_email, register_password)
                if login_redirect:
                    return login_result, register_message

    # Return feedback, no redirect on errors
    return login_message, register_message


def handle_register(firstname, lastname, email, password):
    try:
        # Add user with hashed password
        registration_result = add_user(supabase, firstname, lastname, email, password)

        # If registration is successful, directly log the user in
        if registration_result == "Registration successful!":
            # Now attempt to log the user in
            login_result = handle_login(email, password)
            return login_result  # Return login result directly to trigger redirection if login is successful
        else:
            return registration_result  # Return registration failure message
    except Exception as e:
        return f"An error occurred during registration: {str(e)}"


def handle_login(email, password):
    try:
        # Verify user with hashed password
        is_verified = verify_user(supabase, email, password)
        
        if is_verified:
            # Return success message and redirect component
            return (
                "Login successful",
                dcc.Location(pathname="/", id="redirect")  # Redirect to dashboard
            )
        else:
            # Return error message without redirecting
            return (
                "Invalid email or password. Please try again.",
                None  # Don't set redirect if login failed
            )
    except Exception as e:
        # Return error message without redirecting in case of an exception
        return (
            f"An error occurred during login: {str(e)}",
            None  # No redirect in case of an error
        )