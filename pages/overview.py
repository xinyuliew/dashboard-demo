import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
from datetime import date
import plotly.express as px
import dash_bootstrap_components as dbc
from utils import explain, create_notification, get_data_supa, get_supabase_client
dash.register_page(__name__, path='/')
import plotly.graph_objects as go

# Initialize Supabase client
supabase = get_supabase_client()
df = get_data_supa(supabase, "reddit")


def overview_layout():
    layout = html.Div([
                dbc.Row([
                    dbc.Col([
                        create_notification(
                            "This is a demo showcasing an overview analysis of social media discourses to navigate prioritisation of narratives."
                        ),
                    ]),
                ]),
                dbc.Row(
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody(
                                    dbc.Row([
                                        dbc.Col([
                                                dbc.Label("Choose a date range:"),
                                                html.Br(),
                                                dcc.DatePickerRange(
                                                    id='my-date-picker-range',
                                                    clearable=True,
                                                    display_format="DD-MM-YY",
                                                    min_date_allowed=df['created_utc'].min(),
                                                    max_date_allowed=df['created_utc'].max(),
                                                    initial_visible_month=df['created_utc'].max(),
                                                    start_date=df['created_utc'].min(),
                                                    end_date=df['created_utc'].max(),
                                                ),
                                            ],
                                            xs=12, sm=12, md=6, lg=6,
                                        ),
                                        dbc.Col([
                                                dbc.Label("Filter number of topics:"),
                                                html.Br(),
                                                dbc.RadioItems(
                                                    id='num-topics-slider',
                                                    options=[{"label": str(i), "value": i} for i in range(1, 6)],
                                                    value=5,
                                                    inline=True,
                                                ),
                                            ],
                                            xs=12, sm=12, md=6, lg=6),
                                            html.Div(id='output-container-date-picker-range')
                                        ],
                                    justify="between", 
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
                                        "Top Discussed Topics",
                                        explain("Top")
                                    ], className="card-header-container")  
                                ),
                            dbc.CardBody([
                                dcc.Loading(html.Div(id='table-container'))
                            ])
                        ])
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(
                                html.Div([
                                    "Stance Analysis",
                                    explain("Stance")
                                ], className="card-header-container")  
                            ),
                            dbc.CardBody([
                                dcc.Loading(dcc.Graph(id='stances-chart'))
                            ])
                        ])
                    ], xs=12, sm=12, md=12, lg=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(
                                html.Div([
                                    "Sentiment Analysis",
                                    explain("Sentiment")
                                ], className="card-header-container")  
                            ),
                            dbc.CardBody([
                                dcc.Loading(dcc.Graph(id='sentiments-chart'))
                            ])
                        ])
                    ], xs=12, sm=12, md=12, lg=6),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(
                                 html.Div([
                                    "Popularity Insights",
                                    explain("Popularity")
                                ], className="card-header-container")  
                            ),
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
    Output('num-topics-slider', 'options'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)

def update_num_topics_options(start_date, end_date):
    # Convert start_date and end_date to datetime.date objects for comparison
    start_date = date.fromisoformat(start_date) if start_date else None
    end_date = date.fromisoformat(end_date) if end_date else None

    if start_date and end_date:
        filtered_df = df[(df['created_utc'] >= start_date) & (df['created_utc'] <= end_date)]
        num_topics = filtered_df['Topic'].nunique()
        options = [{"label": str(i), "value": i} for i in range(1, min(num_topics, 5) + 1)]
        return options
    return [{"label": "1", "value": 1}, {"label": "2", "value": 2}, {"label": "3", "value": 3}, {"label": "4", "value": 4}, {"label": "5", "value": 5}]


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

        if filtered_df.empty:
            date_selection_string = "No data available for the selected date range."
            return date_selection_string, None, None,None,None
        
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

        # Dynamically generate severity values based on the number of topics
        severity_values = ['High'] * 2 + ['Medium'] * 2 + ['Low']
        severity_values = severity_values[:len(sorted_topics)]
        sorted_topics['Harmfulness'] = severity_values

        # Filter topics based on the number selected by the user
        sorted_topics = sorted_topics.head(value)
        
        # Table
        table = dash.dash_table.DataTable(
            data=sorted_topics[['Topic_id', 'Topics', 'Total number of post', 'Total number of replies', 'Harmfulness']].to_dict('records'),
            columns=[{'name': col, 'id': col} for col in ['Topic_id', 'Topics', 'Total number of post', 'Total number of replies', 'Harmfulness']],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            sort_action='native'
        )

        # Store the mapping between topics and topic IDs in a dictionary
        topic_id_mapping = dict(zip(sorted_topics['Topics'], sorted_topics['Topic_id']))

        # Filter DataFrame to include only the selected topics
        filtered_df_topic = filtered_df[filtered_df['Topic'].isin(sorted_topics['Topics'])]
        topic_order = sorted(topic_id_mapping.values())

        # Stance chart
        stance_counts = filtered_df_topic.groupby(['Topic', 'Stance']).size().unstack(fill_value=0)
        # Calculate the proportions
        stance_proportions = stance_counts.div(stance_counts.sum(axis=1), axis=0) * 100
        # Melt the DataFrame for Plotly
        data_stance = pd.melt(stance_proportions.reset_index(), id_vars=["Topic"])
        data_stance['TOPIC_ID'] = data_stance['Topic'].map(topic_id_mapping)
        data_stance = data_stance.rename(columns={'value': 'Percentage proportions (%)'})
        # Convert the 'Stance' column to uppercase
        data_stance['STANCES'] = data_stance['Stance'].str.upper()

        # Create the bar plot using Plotly
        fig_stance = px.bar(data_stance, x='Percentage proportions (%)', y='TOPIC_ID', color='STANCES', 
                            orientation='h', barmode='stack', color_discrete_map={
                                'AGAINST': '#bd1f36',  # Bold red
                                'FAVOR': '#40916c',    # Bold green
                                'NONE': '#cfcdc9'      # Bold grey
                            })
        fig_stance.update_layout(
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="bottom",  # Position legend at the bottom
                y=1.05,  # Slightly above the chart
                xanchor="center",  # Center horizontally
                x=0.45  # Center horizontally
            ),
            modebar=dict(
                remove=['lasso2d', 'select2d', 'reset', 'hover', 'zoom', 'autoscale'],  # Remove Lasso and Box Select
            ),
            xaxis=dict(
                range=[0, 100]  # Custom range for the x-axis (0 to 100%)
            ),
            yaxis=dict(
                categoryorder='array',
                categoryarray=topic_order  # Ensure 'topic_order' is defined
            ),
            margin=dict(l=0, r=0),  # Small adjustment to bottom margin
            height = 300
            )
        
        # Sentiment chart

        sentiment_counts = filtered_df_topic.groupby(['Topic', 'Sentiment']).size().unstack(fill_value=0)
        # Calculate the proportions
        sentiment_proportions = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0) * 100
        data_sentiment = pd.melt(sentiment_proportions.reset_index(), id_vars=["Topic"])
        
        data_sentiment['TOPIC_ID'] = data_sentiment['Topic'].map(topic_id_mapping)
        data_sentiment = data_sentiment.rename(columns={'value': 'Percentage proportions (%)'})
        # Convert the 'Stance' column to uppercase
        data_sentiment['SENTIMENTS'] = data_sentiment['Sentiment'].str.upper()

        fig_sentiment = px.bar(data_sentiment, x='Percentage proportions (%)', y='TOPIC_ID', color='SENTIMENTS', orientation='h',
                       barmode='stack', color_discrete_map={
                'POSITIVE': '#4CAF50',
                'NEGATIVE': '#F44336',
                'NEUTRAL': '#9E9E9E'
    })
        
        fig_sentiment.update_layout(
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="bottom",  # Position legend at the bottom
                y=1.05,  # Slightly above the chart
                xanchor="center",  # Center horizontally
                x=0.45  # Center horizontally
            ),
            xaxis=dict(
                range=[0, 100]  # Custom range for the x-axis (0 to 100%)
            ),
            modebar=dict(
                remove=['lasso2d', 'select2d', 'reset', 'hover', 'zoom', 'autoscale'],  # Remove Lasso and Box Select
            ),
            yaxis=dict(
                categoryorder='array',
                categoryarray=topic_order  # Ensure 'topic_order' is defined
            ),
            margin=dict(l=0, r=0),  # Small adjustment to bottom margin
            height = 300
            )

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
        # Rename the columns to upper case
        combined_line_plot_data = combined_line_plot_data.rename(columns={
            'created_utc': 'DATE',
            'No_of_comments': 'NO. OF ENGAGEMENTS',
            'Topic': 'TOPICS'
        })
        fig_popularity = px.line(combined_line_plot_data, x='DATE', y='NO. OF ENGAGEMENTS', color='TOPICS')
        # Apply style changes to popularity line graph
        fig_popularity.update_layout(
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="bottom",  # Position legend at the bottom
                y=1.05,  # Slightly above the chart
                xanchor="center",  # Center horizontally
                x=0.45  # Center horizontally
            ),
            legend_title_text=None,  # Remove legend title
            modebar=dict(
                remove=['lasso2d', 'select2d', 'reset', 'hover', 'zoom', 'autoscale'],  # Remove Lasso and Box Select
            ),
            yaxis=dict(
                categoryorder='array',
                categoryarray=topic_order  # Ensure 'topic_order' is defined
            ),
            margin=dict(l=0, r=0),  # Small adjustment to bottom margin
            )

        return dbc.Alert(date_selection_string, dismissable=True), table, fig_stance, fig_sentiment, fig_popularity
    else:
        return dbc.Alert(date_selection_string, color="danger", dismissable=True), None, None, None, None
    

