import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
from datetime import date
import plotly.express as px
import dash_bootstrap_components as dbc
from utils import get_data
from utils import update_figure_style
dash.register_page(__name__, path='/')


df = get_data()

def overview_layout():
    layout = html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Choose a date range:"),
                        html.Br(),
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=df['created_utc'].min(),
                            max_date_allowed=df['created_utc'].max(),
                            initial_visible_month=df['created_utc'].max(),
                            start_date=df['created_utc'].min(),
                            end_date=df['created_utc'].max(),
                        ),
                        html.Div(id='output-container-date-picker-range')
                    ], width=5),
                    dbc.Col([
                        dbc.Label("Filter number of topics:"),
                        html.Br(),
                        dbc.RadioItems(
                            id='num-topics-slider',
                            options=[
                                {"label": "5", "value": 5},
                                {"label": "10", "value": 10},
                                {"label": "15", "value": 15},
                            ],
                            value=5,
                            inline=True
                        ),   
                    ], width=2)
                ], justify="between"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Top Discussed Topics"),
                            dbc.CardBody([
                                dcc.Loading(html.Div(id='table-container'))
                            ])
                        ])
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Stances"),
                            dbc.CardBody([
                                dcc.Loading(dcc.Graph(id='stances-chart'))
                            ])
                        ])
                    ], width=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Sentiments"),
                            dbc.CardBody([
                                dcc.Loading(dcc.Graph(id='sentiments-chart'))
                            ])
                        ])
                    ], width=6)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Popularity Insights"),
                            dbc.CardBody([
                                dcc.Graph(id='popularity-chart')
                            ])
                        ])
                    ], width=12)
                ])
        ], className="content")
    return layout

layout = overview_layout()

@callback(
    [Output('output-container-date-picker-range', 'children'),
    Output('table-container', 'children'),
    Output('stances-chart', 'figure'),
    Output('sentiments-chart', 'figure'),
    Output('popularity-chart', 'figure')],
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('num-topics-slider', 'value')]
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
        date_selection_string = 'Please select a date range to see it displayed here.'
    else:
        date_selection_string = string_prefix

    # Convert start_date and end_date to datetime.date objects for comparison
    start_date = date.fromisoformat(start_date) if start_date else None
    end_date = date.fromisoformat(end_date) if end_date else None

    if start_date and end_date:
        # Filter DataFrame based on date range
        filtered_df = df[(df['created_utc'] >= start_date) & (df['created_utc'] <= end_date)]

        # Count topics and replies
        post_counts = filtered_df.loc[filtered_df['Parent'] == '1', 'Topic'].value_counts()
        replies_counts = filtered_df.loc[filtered_df['Parent'] != '1', 'Topic'].value_counts()

        # Merge topic counts
        combined_counts = post_counts.combine_first(replies_counts).sort_values(ascending=False)

        # Assign unique IDs to topics
        sorted_topics = combined_counts.reset_index()
        sorted_topics.columns = ['Topics', 'Total number of post']
        sorted_topics['Topic_id'] = [str(i).zfill(3) for i in range(1, len(sorted_topics) + 1)]

        # Calculate replies count
        replies = [replies_counts.get(topic, 0) for topic in sorted_topics['Topics']]
        sorted_topics['Total number of replies'] = replies
        sorted_topics['Severity'] = ['High', 'High', 'Medium', 'Medium', 'Low']

        # Filter topics based on the number selected by the user
        sorted_topics = sorted_topics.head(value)
        
        # Table
        table = dash.dash_table.DataTable(
            data=sorted_topics[['Topic_id', 'Topics', 'Total number of post', 'Total number of replies', 'Severity']].to_dict('records'),
            columns=[{'name': col, 'id': col} for col in ['Topic_id', 'Topics', 'Total number of post', 'Total number of replies', 'Severity']],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'}
        )

        # Store the mapping between topics and topic IDs in a dictionary
        topic_id_mapping = dict(zip(sorted_topics['Topics'], sorted_topics['Topic_id']))

        # Filter DataFrame to include only the selected topics
        filtered_df_topic = filtered_df[filtered_df['Topic'].isin(sorted_topics['Topics'])]

        # Stance chart
        stance_counts = filtered_df_topic.groupby(['Topic', 'Stance']).size().unstack(fill_value=0)
        data_stance = pd.melt(stance_counts.reset_index(), id_vars=["Topic"])
        data_stance['Topic_id'] = data_stance['Topic'].map(topic_id_mapping)
        fig_stance = px.bar(data_stance, x='value', y='Topic_id', color='Stance', 
                    orientation='h', barmode='stack', 
                    color_discrete_map={'Favor': '#BFD1D9', 'None': '#DFE8EC', 'Against': '#5F8CA0'})
        # Apply style changes to stance chart
        fig_stance = update_figure_style(fig_stance)
        
        # Sentiment chart
        sentiment_counts = filtered_df_topic.groupby(['Topic', 'Sentiment']).size().unstack(fill_value=0)
        data_sentiment = pd.melt(sentiment_counts.reset_index(), id_vars=["Topic"])
        data_sentiment['Topic_id'] = data_sentiment['Topic'].map(topic_id_mapping)
        fig_sentiment = px.bar(data_sentiment, x='value', y='Topic_id', color='Sentiment', orientation='h',
                       barmode='stack', color_discrete_map={'Positive': '#BFD1D9', 'Neutral': '#DFE8EC', 'Negative': '#5F8CA0'})
        # Apply style changes to sentiment chart
        fig_sentiment = update_figure_style(fig_sentiment)

        # Create a list to store line plot data for each topic
        line_plot_data_list = []

        # Iterate over each topic in sorted_topics
        for topic in sorted_topics['Topics']:
            # Filter DataFrame for the current topic
            topic_df = filtered_df_topic[filtered_df_topic['Topic'] == topic]
            # Group by created_utc and sum the No_of_comments for the current topic
            line_plot_data = topic_df.groupby('created_utc')['No_of_comments'].sum().reset_index()
            # Add the topic as a new column to the line plot data
            line_plot_data['Topic'] = topic
            # Append the line plot data to the list
            line_plot_data_list.append(line_plot_data)
        # Concatenate line plot data for all topics into a single DataFrame
        combined_line_plot_data = pd.concat(line_plot_data_list)
        # Popularity line graph
        fig_popularity = px.line(combined_line_plot_data, x='created_utc', y='No_of_comments', color='Topic')
        # Apply style changes to popularity line graph
        fig_popularity = update_figure_style(fig_popularity)

        return dbc.Alert(date_selection_string), table, fig_stance, fig_sentiment, fig_popularity
    else:
        return dbc.Alert(date_selection_string, color="danger"), None, None, None, None
    

