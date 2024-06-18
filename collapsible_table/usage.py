import dash
from dash import html
import collapsible_table
import pandas as pd
app = dash.Dash(__name__)

import pandas as pd

# Example DataFrames
data_root = {
    'id': ['1', '2', '3'],
    'text': ['Root post 1', 'Root post 2', 'Root post 3'],
    'created_utc': ['2021-01-01', '2021-01-02', '2021-01-03'],
    'Stance': ['Against', 'Favor', 'None'],
    'Sentiment': ['positive', 'Neutral', 'Negative'],
    'No_of_comments': [2, 0, 1]
}

data_comments = {
    'id': ['3', '4', '5', '6'],
    'Parent': ['1', '1', '4', '3'],
    'Link': ['1', '1', '1', '2'],
    'text': ['Reply to root 1', 'Reply to root 1', 'Reply to reply 4', 'Reply to reply 3'],
    'created_utc': ['2021-01-03', '2021-01-04', '2021-01-05', '2021-01-06'],
    'Stance': ['Against', 'Favor', 'None', 'None'],
    'Sentiment': ['Negative', 'Positive', 'Neutral', 'Neutral'],
    'No_of_comments': [1, 0, 0, 0]
}

df_root = pd.DataFrame(data_root)
df_comments = pd.DataFrame(data_comments)

def create_rows(df_root, df_comments):
    def generate_rows(parent_id, visited):
        subrows = []

        # Filter replies where Link is the same as the parent_id
        replies = df_comments[df_comments['Link'] == parent_id]

        # Iterate through the replies
        for _, reply in replies.iterrows():
            if reply['id'] in visited:
                continue  # Skip if already processed to avoid circular reference

            visited.add(reply['id'])  # Mark this reply as visited

            subrow = {
                'id': reply['id'],
                'text': reply['text'],
                'date': reply['created_utc'],
                'stance': reply['Stance'],
                'sentiment': reply['Sentiment'],
                'num_replies': reply['No_of_comments'],
                'replies': []
            }

            # If there are replies to the current reply, recursively generate rows for the nested replies
            nested_replies = generate_rows(reply['id'], visited)
            if nested_replies:
                subrow['replies'] = nested_replies
            
            subrows.append(subrow)

        return subrows

    rows = []

    for _, root_post in df_root.iterrows():
        visited = set()  # Track visited nodes for each root post
        visited.add(root_post['id'])  # Mark the root post as visited

        row = {
            'id': root_post['id'],
            'text': root_post['text'],
            'date': root_post['created_utc'],
            'stance': root_post['Stance'],
            'sentiment': root_post['Sentiment'],
            'num_replies': root_post['No_of_comments'],
            'replies': generate_rows(root_post['id'], visited)
        }
        rows.append(row)
    
    return rows


app.layout = html.Div([
    collapsible_table.ReactTable(
        id='table',
        rows = create_rows(df_root, df_comments)
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)