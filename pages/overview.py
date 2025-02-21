import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
from datetime import date
import plotly.express as px
import dash_bootstrap_components as dbc
from utils import explain, create_notification, get_data_supa, get_supabase_client, barchart_layout, stats_count
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
   
    start_date, end_date = dates
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)
    date_selection_string = f"You have selected from {start_date} to {end_date}"
    
    df['created_utc'] = pd.to_datetime(df['created_utc']).dt.date
    filtered_df = df[(df['created_utc'] >= start_date) & (df['created_utc'] <= end_date)]
    
    post_counts = filtered_df.loc[filtered_df['Parent'] == '1', 'Topic'].value_counts()
    replies_counts = filtered_df.loc[filtered_df['Parent'] != '1', 'Topic'].value_counts()
    combined_counts = post_counts.combine_first(replies_counts).sort_values(ascending=False)

    sorted_topics = combined_counts.reset_index()
    sorted_topics.columns = ['Topics', 'Total number of post']
    sorted_topics['Topic_id'] = [str(i).zfill(3) for i in range(1, len(sorted_topics) + 1)]
    
    replies = [replies_counts.get(topic, 0) for topic in sorted_topics['Topics']]
    sorted_topics['Total number of replies'] = replies

    severity_values = ['High'] * 2 + ['Medium'] * 2 + ['Low']
    severity_values = severity_values[:len(sorted_topics)]
    sorted_topics['Harmfulness'] = severity_values

    sorted_topics = sorted_topics.head(value)
    
    table = dash.dash_table.DataTable(
        data=sorted_topics[['Topic_id', 'Topics', 'Total number of post', 'Total number of replies', 'Harmfulness']].to_dict('records'),
        columns=[{'name': col, 'id': col} for col in ['Topic_id', 'Topics', 'Total number of post', 'Total number of replies', 'Harmfulness']],
        style_cell={'textAlign': 'left'},
        sort_action='native'
    )

    topic_id_mapping = dict(zip(sorted_topics['Topics'], sorted_topics['Topic_id']))
    filtered_df_topic = filtered_df[filtered_df['Topic'].isin(sorted_topics['Topics'])]
    topic_order = sorted(topic_id_mapping.values())

    data_stance = stats_count(filtered_df_topic, 'Stance', topic_id_mapping)
    fig_stance = px.bar(data_stance, x='Percentage proportions (%)', y='TOPIC_ID', color='Stance', 
                        orientation='h', barmode='stack', color_discrete_map={'AGAINST': '#bd1f36', 'FAVOR': '#40916c', 'NONE': '#cfcdc9'})
    fig_stance = barchart_layout(fig_stance, topic_order)
    
    data_sentiment = stats_count(filtered_df_topic, 'Sentiment', topic_id_mapping)
    fig_sentiment = px.bar(data_sentiment, x='Percentage proportions (%)', y='TOPIC_ID', color='Sentiment', orientation='h',
                    barmode='stack', color_discrete_map={'POSITIVE': '#4CAF50', 'NEGATIVE': '#F44336', 'NEUTRAL': '#9E9E9E'})
    fig_sentiment = barchart_layout(fig_sentiment, topic_order)

    line_plot_data_list = []

    for topic in sorted_topics['Topics']:
        topic_df = filtered_df_topic[filtered_df_topic['Topic'] == topic]
        line_plot_data = topic_df.groupby('created_utc')['No_of_comments'].sum().reset_index()
        line_plot_data['Topic'] = topic
        line_plot_data_list.append(line_plot_data)
    
    combined_line_plot_data = pd.concat(line_plot_data_list)
    combined_line_plot_data = combined_line_plot_data.rename(columns={
        'created_utc': 'Date',
        'No_of_comments': 'Popularity',
        'Topic': 'TOPICS'
    })

    fig_popularity = px.line(combined_line_plot_data, x='Date', y='Popularity', color='TOPICS'
                            ).update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.45),
                                            legend_title_text=None, modebar=dict(remove=['lasso2d', 'select2d', 'reset', 'hover', 'zoom', 'autoscale']),
                                            yaxis=dict(categoryorder='array', categoryarray=topic_order),
                                            margin=dict(l=0, r=0), 
                                            )
        
    return date_selection_string, table, fig_stance, fig_sentiment, fig_popularity
