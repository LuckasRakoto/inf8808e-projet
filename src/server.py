import dash
from dash import dcc, html
import pandas as pd
from cluster_scatter import get_cluster_figure
from correlation_heatmap import get_correlation_figure

# Load data
df = pd.read_csv("data/Student_Mental_health_and_academic_performance.csv")

# Initialize app
app = dash.Dash(__name__)
app.title = "Student Behavior Visualizations"

# Layout
app.layout = html.Div([
    html.H1("Student Behavior Profiles & Academic Performance"),
    
    html.Div([
        html.H2("Cluster-Based Scatterplot"),
        dcc.Graph(figure=get_cluster_figure(df))
    ]),
    
    html.Div([
        html.H2("Habit Correlation Heatmap"),
        dcc.Graph(figure=get_correlation_figure(df))
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)