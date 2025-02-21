import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from dotenv import load_dotenv
import os
from supabase import create_client, Client
import bcrypt
from typing import Optional

def get_supabase_client() -> Client:
    """
    Initializes and returns the Supabase client.

    :return: Supabase client instance.
    :raises ValueError: If required environment variables are missing.
    """
    # Load environment variables
    load_dotenv()

    # Retrieve the API keys
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Missing required Supabase environment variables.")

    # Create and return the Supabase client
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_data_supa(supabase: Client, table_name: str, filters: dict = None) -> pd.DataFrame:
    """
    Fetches data from a specified Supabase table and returns it as a Pandas DataFrame.

    :param supabase: The initialized Supabase client.
    :param table_name: Name of the Supabase table to query.
    :param filters: (Optional) A dictionary of filters to apply (e.g., {"column": "value"}).
    :return: Pandas DataFrame containing the table data, or an empty DataFrame on failure.
    """
    try:
        query = supabase.table(table_name).select("*")
        
        # Apply filters if provided
        if filters:
            for column, value in filters.items():
                query = query.eq(column, value)

        # Execute the query
        response = query.execute()

        if not response.data:
            raise Exception(f"No data returned or error occurred: {response}")

        # Convert the response to a DataFrame
        df = pd.DataFrame(response.data)
        
        # Convert 'created_utc' to datetime, if it exists
        if 'created_utc' in df.columns:
            df['created_utc'] = pd.to_datetime(df['created_utc']).dt.date
        
        return df

    except Exception as e:
        print(f"Error fetching data from table '{table_name}': {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
    
def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.
    
    :param password: Plain text password.
    :return: Hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(stored_hash: str, password: str) -> bool:
    """
    Verifies if the provided password matches the stored hashed password.
    
    :param stored_hash: The stored hashed password.
    :param password: The plain text password.
    :return: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))


def add_user(supabase, firstname, lastname, email, password):
    try:
        # Hash the password before storing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Store user in Supabase
        response = supabase.table("users").insert({
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": hashed_password.decode('utf-8')
        }).execute()
        
        # Check if the response has no error and data is returned
        if response.data:
            return "Registration successful!"
        else:
            return f"Error occurred during registration: {response.error_message}"
    except Exception as e:
        return f"An error occurred during registration: {str(e)}"


def verify_user(supabase: Client, email: str, password: str) -> bool:
    """
    Verifies if a user exists with the given email and password.
    
    :param supabase: Supabase client.
    :param email: User's email.
    :param password: User's plain text password.
    :return: True if user exists and password matches, False otherwise.
    """
    try:
        response = supabase.table("users").select("email", "password").eq("email", email).execute()
        
        if response.data:
            stored_hash = response.data[0]['password']
            return verify_password(stored_hash, password)
        else:
            return False
    except Exception as e:
        print(f"Error verifying user: {e}")
        return False
    
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

def barchart_layout(figure, topic_order):
    return figure.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.45),
                                     xaxis=dict(range=[0, 100]),
                                     modebar=dict(remove=['lasso2d', 'select2d', 'reset', 'hover', 'zoom', 'autoscale']),
                                     yaxis=dict(categoryorder='array', categoryarray=topic_order), 
                                     margin=dict(l=0, r=0), 
                                    )
    
def stats_count(filtered_df_topic, item, topic_id_mapping):
    counts = filtered_df_topic.groupby(['Topic', item]).size().unstack(fill_value=0)
    proportions = (counts.div(counts.sum(axis=1), axis=0) * 100).round(0).astype(int)
    data = pd.melt(proportions.reset_index(), id_vars=["Topic"])
    data['TOPIC_ID'] = data['Topic'].map(topic_id_mapping)
    data = data.rename(columns={'value': 'Percentage proportions (%)'})
    data[item] = data[item].str.upper()
    return data