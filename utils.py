import pandas as pd

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

# Function to update figure styles
def update_figure_style(fig):
    fig.update_layout(font=dict(family="Arial", size=14, color="#000000"))
    fig.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#ffffff')
    fig.update_xaxes(showgrid=True, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridcolor='LightGray')
    return fig
