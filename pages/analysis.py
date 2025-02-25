from datetime import date
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import collapsible_table
from utils import explain, create_notification, get_data_supa, get_supabase_client
import pandas as pd 
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
import re
from collections import Counter
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Initialize Dash app
dash.register_page(__name__, path='/discourse_analysis')

# Initialize Supabase client
supabase = get_supabase_client()

# Fetch data from the "reddit" table in Supabase
df = get_data_supa(supabase, "reddit")  # Pass the supabase client and table name

available_topics = df['Topic'].unique()

# Load stopwords
stop_words = set(stopwords.words("english"))

def simple_tokenize(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return [word for word in tokens if word not in stop_words and len(word) > 2]

def get_most_common_words(texts, n=7):
    all_tokens = [token for text in texts for token in simple_tokenize(str(text))]
    return Counter(all_tokens).most_common(n)


def create_rows(df_root, df_comments):
    def generate_rows(parent_id):
        subrows = []
        replies = df_comments[df_comments['Parent'] == parent_id].copy()

        for _, reply in replies.iterrows():
            subrow = {
                'id': reply['id'],
                'text': reply['text'],
                'date': reply['created_utc'],
                'stance': reply['Stance'],
                'sentiment': reply['Sentiment'],
                'num_replies': reply['No_of_comments'],
                'replies': []
            }
            
            # Check if there are nested replies
            if reply['No_of_comments'] > 0:
                subrow['replies'] = generate_rows(reply['id'])

            subrows.append(subrow)
        return subrows

    rows = []

    for _, root_post in df_root.iterrows():
        row = {
            'id': root_post['id'],
            'text': root_post['text'],
            'date': root_post['created_utc'],
            'stance': root_post['Stance'],
            'sentiment': root_post['Sentiment'],
            'num_replies': root_post['No_of_comments'],
            'replies': generate_rows(root_post['id'])
        }
        rows.append(row)
    return rows


def discourse_analysis_layout():
    layout = html.Div([
        dbc.Row([
                    dbc.Col([
                         create_notification("This is a demo showcasing an in-depth view of social media discourses, facilitating investigations by featuring stance and sentiment labels for each text within discourses. This is designed to support investigative efforts, such as uncovering the propagation and reasoning behind narratives.")
                    ]),
                ]),
        dbc.Row(
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody(
                                dbc.Row([
                                    dbc.Col([
                                        dmc.DatePickerInput(
                                            id="my-date-picker-range2",
                                            label="Date",
                                            description="Select a date range",
                                            minDate=df['created_utc'].min(),
                                            type="range",
                                            value=[date(2020, 4, 24), date(2021, 5, 6)],
                                        ),    
                                        dmc.Space(h=10),
                                        dmc.Text(id="selected-date-input-range-picker2"), 
                                        ],
                                    xs=12, sm=12, md=6, lg=4,
                                    ),
                                    dbc.Col([
                                        dmc.MultiSelect(
                                                label="Topic",
                                                description="Select your topic for investigation", 
                                                id="num-topics-picker",
                                                value=[available_topics[0]],
                                                data=[
                                                    {'label': topic, 'value': topic} for topic in available_topics
                                                ],
                                            
                                            ),
                                    ], xs=12, sm=12, md=12, lg=6),
                                    html.Div(id='output-container-date-picker-range2')
                                ], justify="between"
                                ),
                            ),
                            ],
                        ),
                        width=12, className="selectionrow"  # Full width for the card
                    ),
                ),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Div([
                                html.H5("Summary", className="card-title fw-bold"), 
                                html.H6("A zoomed-in view of stances and sentiments for topic(s) of interest, allowing the customisation for investigation into details and trends.", className="card-subtitle")
                            ],),
                            explain("Summary")
                        ], className="card-header-container")  
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                 dcc.Loading(dcc.Graph(id='table_keywords'))
                            ], xs=12, sm=12, md=12, lg=4),
                            dbc.Col([
                                dcc.Loading(dcc.Graph(id='stance_distribution'))
                            ], xs=12, sm=12, md=12, lg=4),
                            dbc.Col([
                                dcc.Loading(dcc.Graph(id='sentiment_distribution'))
                            ], xs=12, sm=12, md=12, lg=4)
                        ], align="center")
                    ])
                ]),
            ], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Div([
                                html.H5("Discourses", className="card-title fw-bold"),
                                html.H6("All detailed discourses that contributed to the visual analysis to support in-depth investigation.", className="card-subtitle")
                            ],),
                            explain("Discourses")      
                        ], className="card-header-container")  
                    ),
                    dbc.CardBody([
                        dcc.Loading(html.Div(id='table-container2'))
                    ]),
                ]),
            ]),
        ]),
        
    ], className="content")
    return layout

layout = discourse_analysis_layout()

@callback(
    Output('output-container-date-picker-range2', 'children'),
    Output('stance_distribution', 'figure'),
    Output('sentiment_distribution', 'figure'),
    Output('table_keywords', 'figure'),
    Output('table-container2', 'children'),
    Input('my-date-picker-range2', 'value'),
    Input('num-topics-picker', 'value'),
)

def update_output(dates, value):
    if None in dates:
        raise PreventUpdate
   
    start_date, end_date = map(date.fromisoformat, dates)
    # Filter DataFrame based on date range
    filtered_df = df[(df['created_utc'] >= start_date) & (df['created_utc'] <= end_date)]

    # Filter root posts by topics of interest
    selected_df = filtered_df[filtered_df['Topic'].isin(value)]

    # Put every data in selected_df that their "parent" is 1 into df_root
    df_root = selected_df[selected_df['Parent'] == '1']

    # Put every data in selected_df that their "parent" is not 1 into df_comments
    df_comments = selected_df[selected_df['Parent'] != '1']

    # Generate most common words
    most_common_words = get_most_common_words(selected_df['text'])
    key_df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])

    wordcount_chart = px.bar(
                        key_df, y='Word', x='Frequency', title="Top keywords",
                        labels={"Word": "Words", "Frequency": "Count"}, color='Frequency',
                        color_continuous_scale='blues', orientation='h'
                        ).update_layout(
                            xaxis_title="Count", 
                            yaxis_title="Words", 
                            margin=dict(l=10, r=10, t=40, b=40), 
                            height=300
                        )

    # Group by 'Stance' and count occurrences
    stance_counts = selected_df['Stance'].value_counts().reset_index()
    stance_counts.columns = ['Stance', 'Count']

    # Calculate proportions as percentages
    stance_proportions = stance_counts.copy()
    stance_proportions['Proportion'] = (stance_proportions['Count'] / stance_proportions['Count'].sum()) * 100

    # Create the bar chart with proportions
    stance_chart = px.bar(stance_proportions, x='Proportion', y='Stance', color='Stance', title='Stance distribution', color_discrete_map={
                        'Against': '#FF6F6F',
                        'Favor': '#6FDF6F',
                        'None': '#C0C0C0'
    }).update_layout(xaxis_title="Proportions (%)", yaxis_title="Stances", showlegend=False, 
                     xaxis=dict(range=[0, 100]), margin=dict(l=10, r=10, t=40, b=40), height=300)
    
    # Group by 'Sentiment' and count occurrences
    sentiment_counts = selected_df['Sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    sentiment_proportions = sentiment_counts.copy()
    sentiment_proportions['Proportion'] = (sentiment_proportions['Count'] / sentiment_proportions['Count'].sum()) * 100

    sentiment_chart = px.bar(sentiment_proportions, x='Proportion', y='Sentiment', color='Sentiment', title='Sentiment distribution', color_discrete_map={
            'Positive': '#4CAF50',
            'Negative': '#F44336',
            'Neutral': '#9E9E9E'
    }).update_layout(xaxis_title="Proportions (%)", yaxis_title="Sentiments", showlegend=False, modebar=dict(remove=['lasso2d', 'select2d', 'reset', 'hover', 'zoom', 'autoscale']), 
                     xaxis=dict(range=[0, 100]), margin=dict(l=10, r=10, t=40, b=40), height = 300)
    
    
    rows = create_rows(df_root, df_comments)
    discourse_table = html.Div(collapsible_table.ReactTable(id='table-container2', rows=rows), className="table-discourse")

    return f"You have selected from {start_date} to {end_date}", stance_chart, sentiment_chart, wordcount_chart,discourse_table