import pandas as pd
import dash_bootstrap_components as dbc
from dash import html

def get_data():
    df_csv = pd.read_csv('dataset/reddit_vaccine_discourse.csv')
    df_csv['created_utc'] = pd.to_datetime(df_csv['created_utc']).dt.date
 
    df_csv['Stance'] = df_csv['Stance'].astype(str)
    df_csv['Stance'] = df_csv['Stance'].str.replace('nan','None')
    df_csv['id'] = df_csv['id'].astype(str)
    df_csv['Parent'] = df_csv['Parent'].astype(str)
    df_csv['Link'] = df_csv['Link'].astype(str)
    df_csv['id'] = df_csv['id'].str.strip()
    df_csv['Parent'] = df_csv['Parent'].str.strip()
    df_csv['Link'] = df_csv['Link'].str.strip()
    df_csv['Sentiment'] = df_csv['Sentiment'].astype(str)
    
    return df_csv

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
            make_tooltip("Shows the distribution of opinions, 'Against', 'Favour', or 'None'. This helps to understand different viewpoints within discourses by topic.", tooltip_id)
        ], className="help-icon")
    elif item == "Sentiment":
        return html.Div([
            make_button(tooltip_id),  # Unique ID for the button
            make_tooltip("Displays the distribution of emotional tone, 'Positive', 'Negative', or 'Neutral'. This reveals the overall mood within discourses by topic.", tooltip_id)
        ], className="help-icon")
    elif item == "Popularity":
        return html.Div([
            make_button(tooltip_id),  # Unique ID for the button
            make_tooltip("Popularity insights reflect the level of engagement or interest in topics over time. This helps identify trends providing an understanding of how each topic of discourse is gaining or losing traction.", tooltip_id)
        ], className="help-icon")
    elif item == "Top":
        return html.Div([
            make_button(tooltip_id),  # Unique ID for the button
            make_tooltip("Clusters the resulting discourses into topics to help identify areas that are currently the most prominent or relevant.", tooltip_id)
        ], className="help-icon")
    elif item == "Summary":
        return html.Div([
            make_button(tooltip_id),  # Unique ID for the button
            make_tooltip("Provides a zoomed-in view of stances and sentiments for a specific topic, customising investigation into finer details and trends.", tooltip_id)
        ], className="help-icon")
    elif item == "Discourses":
        return html.Div([
            make_button(tooltip_id),  # Unique ID for the button
            make_tooltip("Displays all detailed discourse data that reflects all visual analysis to support in-depth investigation.", tooltip_id)
        ], className="help-icon")
