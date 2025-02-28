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
from itertools import chain
from nltk.corpus import stopwords
from functools import lru_cache

@lru_cache(maxsize=128)
def get_most_common_words_cached(text):
    all_tokens = text.lower().split()  
    filtered_tokens = [word for word in all_tokens if word not in stop_words and len(word) > 2]
    return Counter(filtered_tokens).most_common(7)

try:
    stop_words = frozenset(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = frozenset(stopwords.words("english"))

TOKEN_PATTERN = re.compile(r'\b\w+\b')

dash.register_page(__name__, path='/detailed_analysis')
supabase = get_supabase_client()
df = get_data_supa(supabase, "reddit") 
available_topics = df['Topic'].unique()

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
                         create_notification("This is a demo showcasing an in-depth view of social media conversations, facilitating investigations by featuring stance and sentiment labels for each text within discourses. This is designed to support investigative efforts, such as uncovering the propagation and reasoning behind narratives.")
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
                                            value=[date(2020, 11, 20), date(2021, 5, 6)],
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
                                html.H6("A focused view of key keywords, stances, and sentiments for selected topics of interest. This allows users to customise their analysis in detailed view", className="card-subtitle")
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
                                html.H6("All resulting conversations that contributed to the visual analysis to support in-depth investigation.", className="card-subtitle")
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
    Output("output-container-date-picker-range2", "children"),
    Output("stance_distribution", "figure"),
    Output("sentiment_distribution", "figure"),
    Output("table_keywords", "figure"),
    Output("table-container2", "children"),
    Input("my-date-picker-range2", "value"),
    Input("num-topics-picker", "value")
)
def update_output(dates, selected_topics):
    if not dates or not selected_topics:
        raise PreventUpdate

    start_date, end_date = map(date.fromisoformat, dates)
    selected_df = df.query("created_utc >= @start_date & created_utc <= @end_date & Topic in @selected_topics")

    if selected_df.empty:
        return f"No data available for {start_date} to {end_date}", px.bar(title="No Data"), px.bar(title="No Data"), px.bar(title="No Data"), html.Div("No data available")

    all_text = " ".join(selected_df["text"].dropna())
    most_common_words = get_most_common_words_cached(all_text)  # Cached function call
    key_df = pd.DataFrame(most_common_words, columns=["Word", "Frequency"])

    wordcount_chart = px.bar(
        key_df, y="Word", x="Frequency", title="Top Keywords",
        labels={"Word": "Words", "Frequency": "Count"}, color="Frequency",
        color_continuous_scale="blues", orientation="h"
    ).update_layout(
        xaxis_title="Count", yaxis_title="Words",
        margin=dict(l=0, r=0, t=30, b=30), height=300
    )

    def compute_proportions(column_name):
        counts = selected_df[column_name].value_counts(normalize=True).mul(100).reset_index()
        counts.columns = [column_name, "Proportion"]
        return counts

    stance_proportions = compute_proportions("Stance")
    sentiment_proportions = compute_proportions("Sentiment")

    stance_chart = px.bar(
        stance_proportions, x="Proportion", y="Stance", color="Stance", title="Stance Distribution",
        color_discrete_map={"Against": "#FF6F6F", "Favor": "#6FDF6F", "None": "#C0C0C0"}
    ).update_layout(
        xaxis_title="Proportions (%)", yaxis_title="Stances", showlegend=False,
        xaxis=dict(range=[0, 100]), margin=dict(l=0, r=0, t=30, b=30), height=300
    )

    sentiment_chart = px.bar(
        sentiment_proportions, x="Proportion", y="Sentiment", color="Sentiment", title="Sentiment Distribution",
        color_discrete_map={"Positive": "#4CAF50", "Negative": "#F44336", "Neutral": "#9E9E9E"}
    ).update_layout(
        xaxis_title="Proportions (%)", yaxis_title="Sentiments", showlegend=False,
        xaxis=dict(range=[0, 100]), margin=dict(l=0, r=0, t=30, b=30), height=300
    )

    df_root = selected_df[selected_df["Parent"] == "1"]
    df_comments = selected_df[selected_df["Parent"] != "1"]
    rows = create_rows(df_root, df_comments)

    discourse_table = html.Div(
        collapsible_table.ReactTable(id="table-container2", rows=rows),
        className="table-discourse"
    )

    return f"You have selected from {start_date} to {end_date}", stance_chart, sentiment_chart, wordcount_chart, discourse_table