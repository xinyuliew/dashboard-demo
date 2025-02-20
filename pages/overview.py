import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
from datetime import date
import plotly.express as px
import dash_bootstrap_components as dbc
from utils import explain, create_notification, get_data_supa, get_supabase_client
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate

# Register Page
dash.register_page(__name__, path='/')

# Initialize Supabase client
supabase = get_supabase_client()
df = get_data_supa(supabase, "reddit")

# Assign unique IDs and Harmfulness to topics once
topic_counts = df['Topic'].value_counts()
sorted_topics = pd.DataFrame({'Topics': topic_counts.index, 'Total number of post': topic_counts.values})
sorted_topics['Topic_id'] = [str(i).zfill(3) for i in range(1, len(sorted_topics) + 1)]
sorted_topics['Harmfulness'] = (['High'] * 2 + ['Medium'] * 2 + ['Low'])[:len(sorted_topics)]

# Store Topic-ID mapping globally
topic_id_mapping = dict(zip(sorted_topics['Topics'], sorted_topics['Topic_id']))

# ------------------------------------
# Layout Function
# ------------------------------------
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
                                                dmc.DatePickerInput(
                                                    id="my-date-picker-range",
                                                    label="Date",
                                                    description="Select a date range",
                                                    minDate=df['created_utc'].min(),
                                                    type="range",
                                                    value=[date(2020, 4, 24), date(2021, 5, 6)],
                                                ),    
                                                dmc.Space(h=10),
                                                dmc.Text(id="selected-date-input-range-picker"), 
                                                ],
                                            xs=12, sm=12, md=6, lg=4,
                                        ),
                                        dbc.Col([
                                            dmc.MultiSelect(
                                                label="Channel",
                                                description="Select your source",
                                                id="framework-multi-select",
                                                value=["reddit"],
                                                data=[
                                                    {"value": "reddit", "label": "Reddit"},
                                                    {"value": "twitter", "label": "X(Twitter)"},
                                                    {"value": "facebook", "label": "Facebook"},
                                                ],
                                                w=400,
                                                mb=10,
                                            ),
                                            ],
                                            xs=12, sm=12, md=6, lg=4,
                                        ),
                                        dbc.Col([
                                            dmc.NumberInput(
                                                id='num-topics-slider',
                                                label="Filter Topics",
                                                placeholder="From 1-5",
                                                description="Select number of topics to cluster",
                                                min=1,
                                                max=5,
                                                w=250,
                                            ),
                                            ],
                                            xs=12, sm=12, md=6, lg=4),
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

# ------------------------------------
# Callbacks
# ------------------------------------

@callback(Output('num-topics-slider', 'options'), [Input('my-date-picker-range', 'value')])
def update_num_topics_options(dates):
    if not dates or None in dates:
        raise PreventUpdate

    start_date, end_date = map(date.fromisoformat, dates)
    num_topics = df.loc[(df['created_utc'] >= start_date) & (df['created_utc'] <= end_date), 'Topic'].nunique()
    
    return [{"label": str(i), "value": i} for i in range(1, min(num_topics, 5) + 1)]

@callback(
    [Output('output-container-date-picker-range', 'children'),
     Output('table-container', 'children'),
     Output('stances-chart', 'figure'),
     Output('sentiments-chart', 'figure'),
     Output('popularity-chart', 'figure')],
    [Input('my-date-picker-range', 'value'), Input('num-topics-slider', 'value')]
)
    
def update_output(dates, value):
    if None in dates:
        raise PreventUpdate
   
   # Extract start and end dates
    start_date, end_date = dates

    # Convert start_date and end_date to datetime.date objects for comparison
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)

    # Date selection text
    date_selection_string = f"You have selected from {start_date} to {end_date}"
    
    # Ensure the DataFrame's `created_utc` column is in datetime format
    df['created_utc'] = pd.to_datetime(df['created_utc']).dt.date
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
    stance_proportions = (stance_counts.div(stance_counts.sum(axis=1), axis=0) * 100).round(0).astype(int)
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
        )
    
    # Sentiment chart

    sentiment_counts = filtered_df_topic.groupby(['Topic', 'Sentiment']).size().unstack(fill_value=0)
    # Calculate the proportions
    sentiment_proportions = (sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0) * 100).round(0).astype(int)
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
        'created_utc': 'Date',
        'No_of_comments': 'Popularity',
        'Topic': 'TOPICS'
    })
    fig_popularity = px.line(combined_line_plot_data, x='Date', y='Popularity', color='TOPICS')
    
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
        
    return date_selection_string, table, fig_stance, fig_sentiment, fig_popularity
