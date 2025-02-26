import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, State
from utils import get_supabase_client, create_notification
import dash_mantine_components as dmc
import re  

supabase = get_supabase_client()

def support_layout():
    layout = html.Div([
        dbc.Container([
            dbc.Row([
                    dbc.Col([
                         create_notification("This allows users to provide feedback on the analysis or the dashboard."),
                    ]),
                ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                         dbc.CardHeader(html.H4("Contact us", className="card-title fw-bold")),
                         dbc.CardBody([
                            # Input Fields
                            dmc.TextInput(label="Name", id="name-input", required=True, placeholder="First Last"),
                            dmc.TextInput(label="Email", id="email-input", required=True, placeholder="example@email.com"),
                            dmc.TextInput(label="Phone", id="phone-input", required=False, placeholder="Optional"),

                            dmc.Select(
                                label="Issue Category",
                                id="issue-category",
                                data=["Incorrect labels", "Data Issue", "Bug Report", "Feature Request", "General Inquiry", "Other"],
                                placeholder="Select an option",
                                searchable=True,
                            ),
                            dmc.Textarea(label="Issue Description", id="issue-description", required=True, placeholder="Please describe the issue in detail"),
                            dmc.Textarea(label="Additional Comments", id="additional-comments"),
                            # add some gap here
                            dmc.Space(h=20),
                            # Submit Button
                            dmc.Button("Submit", id="open-modal-button", color="blue"),

                            # Modal for Submission Status
                            dmc.Modal(
                                title="Submission Status",
                                id="submission-modal",
                                centered=True,
                                children=[
                                    dmc.Text(id="modal-message", className="mb-3"),
                                    dmc.Space(h=20),
                                    dmc.Button("Close", color="red", variant="outline", id="close-modal-button"),
                                ],
                            ),
                        ]),
                    ])
                ], width=12),
            ], className="mb-4"),
        ])
        ]
    )
    return layout

layout = support_layout()

# Helper function to validate email format
def is_valid_email(email):
    email_regex = r"^[^@]+@[^@]+\.[^@]+$"
    return re.match(email_regex, email)

# Callback to handle form submission and modal interaction
@callback(
    Output("submission-modal", "opened"),
    Output("modal-message", "children"),
    Input("open-modal-button", "n_clicks"),
    State("name-input", "value"),
    State("email-input", "value"),
    State("phone-input", "value"),
    State("issue-category", "value"),
    State("issue-description", "value"),
    State("additional-comments", "value"),
    prevent_initial_call=True
)
def handle_submission(n_clicks, name, email, phone, category, issue, comments):
    # Ensure values are not None
    name = name or ""
    email = email or ""
    issue = issue or ""

    # Check for missing required fields
    missing_fields = []
    if not name.strip():
        missing_fields.append("Name")
    if not email.strip():
        missing_fields.append("Email")
    elif not is_valid_email(email):  # Validate email format
        return True, "⚠️ Please enter a valid email address."

    if not issue.strip():
        missing_fields.append("Issue Description")

    if missing_fields:
        return True, f"⚠️ Please fill in the required fields: {', '.join(missing_fields)}."

    # Save to Supabase
    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "category": category,
        "issue_description": issue,
        "additional_comments": comments
    }

    try:
        response = supabase.table("support_requests").insert(data).execute()
        if response.data:
            return True, "✅ Your request has been successfully submitted!"
        else:
            return True, "⚠️ Submission failed. Please try again."
    except Exception as e:
        return True, f"❌ Error: {str(e)}"

# Callback to close the modal
@callback(
    Output("submission-modal", "opened", allow_duplicate=True),
    Input("close-modal-button", "n_clicks"),
    prevent_initial_call=True
)
def close_modal(n_clicks):
    return False