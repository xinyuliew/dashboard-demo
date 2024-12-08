import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API keys from the environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing required environment variables")
    
from supabase import create_client, Client

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_data_supa(table_name):
    try:
        # Fetch data from Supabase
        response = supabase.table(table_name).select("*").execute()

        # Check if the data is None or an error occurred
        if not response.data:
            raise Exception(f"Error fetching data: {response}")

        # Convert the data to a Pandas DataFrame
        df = pd.DataFrame(response.data)
        df['created_utc'] = pd.to_datetime(df['created_utc']).dt.date
        return df

    except Exception as e:
        print(f"Error fetching data from table '{table_name}': {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
    

# Function to filter DataFrame based on date range
def filter_by_date(df, start_date, end_date):
    mask = (df['created_utc'] >= start_date) & (df['created_utc'] <= end_date)
    return df.loc[mask]


def make_button(id):
    return dbc.Button(
        html.I(className="bi bi-question-circle"),  # Using a help icon
        id=id,
        n_clicks=0,
        color="link",  # Link color to keep the icon subtle
        style={"fontSize": "1.5rem", "padding": "0"}  # Adjust size if needed
    )

def make_tooltip(text, id):
    return dbc.Tooltip(
        text,
        target=id,
        placement="right",  # Tooltip on the right
    )

def explain(item):
    tooltip_id = f"tooltip-{item.lower()}"
    if item == "Stance":
        return html.Div([
            make_button(tooltip_id),  # Unique ID for the button
            make_tooltip("The percentage distribution of opinions, 'Against', 'Favour', or 'None', within discourses by topic ID.", tooltip_id)
        ], className="help-icon")
    elif item == "Sentiment":
        return html.Div([
            make_button(tooltip_id),  # Unique ID for the button
            make_tooltip("T he percentage distribution of emotional tone, 'Positive', 'Negative', or 'Neutral', within discourses by topic ID.", tooltip_id)
        ], className="help-icon")
    elif item == "Popularity":
        return html.Div([
            make_button(tooltip_id),  # Unique ID for the button
            make_tooltip("The level of engagement or interest in topics over time.", tooltip_id)
        ], className="help-icon")
    elif item == "Top":
        return html.Div([
            make_button(tooltip_id),  # Unique ID for the button
            make_tooltip("Topic clustering to bring forward the most prominent or relevant discussion.", tooltip_id)
        ], className="help-icon")
    elif item == "Summary":
        return html.Div([
            make_button(tooltip_id),  # Unique ID for the button
            make_tooltip("A zoomed-in view of stances and sentiments for topic(s) of interest, allowing the customisation for investigation into details and trends.", tooltip_id)
        ], className="help-icon")
    elif item == "Discourses":
        return html.Div([
            make_button(tooltip_id),  # Unique ID for the button
            make_tooltip("All detailed discourses that contributed to the visual analysis to support in-depth investigation.", tooltip_id)
        ], className="help-icon")

def create_notification(description):
    return html.Div(
        [
            dbc.Button(
                "Page Description",  # Initial button text when the alert is open
                id="alert-toggle",
                n_clicks=0,
                className="button"
            ),
            dbc.Alert(
                description,
                id="demo-alert",
                is_open=True,  # Alert is initially open
                className="notification-card",  # Apply the transition class
                color="light",
            ),
        ],
        className="notification-container"
    )

