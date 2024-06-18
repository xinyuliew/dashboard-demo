import sys
sys.path.append("/Users/trixieliew/dash/collapsible_table")
from datetime import date
import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import spacy
from collections import Counter
import plotly.express as px
import collapsible_table
from utils import get_data
from utils import update_figure_style
import pandas as pd

# Initialize Dash app
dash.register_page(__name__, path='/discourse_analysis')

# Load data once
df = get_data()
available_topics = df['Topic'].unique()

# Load and configure spaCy model once
nlp = spacy.load("en_core_web_sm")
nlp.disable_pipes(["ner", "parser"])
custom_stopwords = {'nt', 'm', 'like'}
stopwords = nlp.Defaults.stop_words | custom_stopwords
stopwords = {word.lower() for word in stopwords}

# Define a function to normalize text using spaCy
def normalize_text(text):
    text = str(text)
    text = text.lower()
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if token.text not in stopwords and not token.is_punct and not token.is_space]
    return lemmas

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
                dbc.Label("Choose a date range:"),
                html.Br(),
                dcc.DatePickerRange(
                    id='my-date-picker-range2',
                    min_date_allowed=df['created_utc'].min(),
                    max_date_allowed=df['created_utc'].max(),
                    initial_visible_month=df['created_utc'].max(),
                    start_date=df['created_utc'].min(),
                    end_date=df['created_utc'].max(),
                ),
                html.Div(id='output-container-date-picker-range2')
            ], width=5),
            dbc.Col([
                dbc.Label("Choose a topic:"),
                html.Br(),
                dcc.Dropdown(
                    id='num-topics-picker',
                    options=[{'label': topic, 'value': topic} for topic in available_topics],
                    multi=True,
                    value=[available_topics[0]]
                )
            ], width=5)
        ], justify="between"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Summary"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dcc.Loading(dash_table.DataTable(id='table_keywords'))
                             ], width=4, className="keywords-table"),
                            dbc.Col([
                                dcc.Loading(dcc.Graph(id='stance_distribution'))
                            ], width=4, className="chart"),
                            dbc.Col([
                                dcc.Loading(dcc.Graph(id='sentiment_distribution'))
                            ], width=4, className="chart")
                        ], align="center")
                    ])
                ]),
            ], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Discourses"),
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
    Output('table_keywords', 'data'),
    Output('table-container2', 'children'),
    Input('my-date-picker-range2', 'start_date'),
    Input('my-date-picker-range2', 'end_date'),
    Input('num-topics-picker', 'value'),
)

def update_output(start_date, end_date, value):
    
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        date_selection_string = 'Select a date to see it displayed here'
    else:
        date_selection_string = string_prefix

    # Convert start_date and end_date to datetime.date objects for comparison
    start_date = date.fromisoformat(start_date) if start_date else None
    end_date = date.fromisoformat(end_date) if end_date else None

    if start_date and end_date:
        # Filter DataFrame based on date range
        filtered_df = df[(df['created_utc'] >= start_date) & (df['created_utc'] <= end_date)]
        # Separate root posts (Parent == '1') and other posts (Parent != '1')
        root_posts = filtered_df[filtered_df['Parent'] == '1']
        other_posts = filtered_df[filtered_df['Parent'] != '1']

        # Filter root posts by topics of interest
        selected_root_posts = root_posts[root_posts['Topic'].isin(value)]

        # Merge selected_root_posts with other_posts based on common columns
        selected_df = pd.concat([selected_root_posts, other_posts])
        
        # Normalize each row in the DataFrame and concatenate the results
        normalized_text = selected_df['text'].apply(normalize_text)

        # Flatten the list of lists
        all_normalized_tokens = [token for sublist in normalized_text for token in sublist]

        # Use Counter to get the 10 most common words
        word_counter = Counter(all_normalized_tokens)

        # Get the most common words and frequencies
        most_common_words = word_counter.most_common(7)
        # Convert to Pandas DataFrame
        key_df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])

        # Group by 'Stance' and count occurrences
        stance_counts = selected_df['Stance'].value_counts().reset_index()
        stance_counts.columns = ['Stance', 'Count']
        stance_chart = px.bar(stance_counts, x='Count', y='Stance', color='Stance', title='Stance Distribution',
                              color_discrete_map={'Favor': '#BFD1D9', 'None': '#DFE8EC', 'Against': '#5F8CA0'})
        stance_chart = update_figure_style(stance_chart)

        # Group by 'Sentiment' and count occurrences
        sentiment_counts = selected_df['Sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        sentiment_chart = px.bar(sentiment_counts, x='Count', y='Sentiment', color='Sentiment', title='Sentiment Distribution',
                                 color_discrete_map={'Positive': '#BFD1D9', 'Neutral': '#DFE8EC', 'Negative': '#5F8CA0'})
        sentiment_chart = update_figure_style(sentiment_chart)
        # Put every data in selected_df that their "parent" is 1 into df_root
        df_root = selected_df[selected_df['Parent'] == '1']
        # Put every data in selected_df that their "parent" is not 1 into df_comments
        df_comments = selected_df[selected_df['Parent'] != '1']

        rows = create_rows(df_root, df_comments)
        return dbc.Alert(date_selection_string), stance_chart, sentiment_chart, key_df.to_dict('records'), html.Div(collapsible_table.ReactTable(id='table-container2', rows=rows), className="table-discourse")
    else:
        return dbc.Alert(date_selection_string, color="danger"), None, None, None, None
  