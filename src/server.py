'''
    Contains the server to run our application.
'''

#Optional: use failsafe for deployment if needed
#from flask_failsafe import failsafe
#@failsafe

import dash
from dash import dcc, html
import pandas as pd
from src.cluster_scatter import get_cluster_figure
from src.correlation_heatmap import get_correlation_figure
#from callback import register_callbacks

# Load data
#df = pd.read_csv("C:/Users/Propriétaire/Documents/GitHub/inf8808e-projet/src/assets/data/student_habits_performance.csv")


def create_app():
    '''
        Gets the underlying Flask server from our Dash app.

        Returns:
            The server to be run
    '''
    # the import is intentionally inside to work with the server failsafe
    from app import app  # pylint: disable=import-outside-toplevel
    return app.server

    # Generate figures
    '''cluster_fig = get_cluster_figure(df)
    heatmap_fig = get_correlation_figure(df)

    # Layout
    app.layout = html.Div([
        html.H1("Student Behavior Profiles & Academic Performance"),
    
        html.Div([
            html.H2("Cluster-Based Scatterplot Profiles"),
            dcc.Graph(id="cluster-graph", figure=cluster_fig),
            html.Div(id="profile-panel", style={
                "marginTop": "20px",
                "padding": "15px",
                "border": "1px solid #ccc",
                "borderRadius": "8px"
            })
        ]),
    
        html.Div([
            html.H2("Correlation Matrix of Habits"),
            dcc.Graph(figure=get_correlation_figure(df))
        ])
    ])

    # Register callbacks for interactivity
    register_callbacks(app, df)'''

if __name__ == "__main__":
    create_app().run(port="8050", debug=True)
