# app.py

from dash import Dash, html, dcc
import pandas as pd
from cluster_scatter import get_cluster_figure
from correlation_heatmap import get_correlation_figure

# Initialize the Dash app
app = Dash(__name__)
app.title = "Student Behavior Visualization"

# Load the dataset
data_path = "./data/Student_Mental_health_and_academic_performance.csv"
df = pd.read_csv(data_path)

# Generate figures
cluster_fig = get_cluster_figure(df)
heatmap_fig = get_correlation_figure(df)

# Layout of the app
app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1("Student Habits vs. Academic Performance"),
        html.H2("Cluster Profiles & Behavioral Patterns")
    ]),

    html.Main(className='viz-container', children=[
        html.Section(children=[
            html.H3("Cluster-Based Scatterplot"),
            dcc.Graph(figure=cluster_fig)
        ]),

        html.Section(children=[
            html.H3("Correlation Matrix of Habits"),
            dcc.Graph(figure=heatmap_fig)
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)