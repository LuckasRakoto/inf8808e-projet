import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from cluster_scatter import get_cluster_figure
from correlation_heatmap import get_correlation_figure
from radar_chart import get_radar_chart
from bar_chart import get_bar_chart_figure

app = dash.Dash(__name__)
app.title = 'Student Habits vs Performance'

df = pd.read_csv("assets/data/student_habits_performance.csv")

habits = ['study_hours_per_day', 'social_media_hours', 'netflix_hours',
          'sleep_hours', 'diet_quality', 'exercise_frequency',
          'mental_health_rating']

slider_config = {
    'study_hours_per_day': {'min': 0, 'max': 9, 'step': 1},
    'social_media_hours': {'min': 0, 'max': 7, 'step': 1},
    'netflix_hours': {'min': 0, 'max': 6, 'step': 1},
    'sleep_hours': {'min': 3, 'max': 10, 'step': 1},
    'diet_quality': {'min': 1, 'max': 3, 'step': 1},
    'exercise_frequency': {'min': 0, 'max': 6, 'step': 1},
    'mental_health_rating': {'min': 1, 'max': 10, 'step': 1}
}

# === LAYOUT ===
app.layout = html.Div([
    html.H1("Student Behavior Profiles & Academic Performance"),
    
    html.Div([
        html.H2("Average Student Habits"),
        dcc.Graph(figure=get_bar_chart_figure(df))
    ]),

    html.Div([
        html.H2("Cluster-Based Scatterplot"),
        dcc.Graph(figure=get_cluster_figure(df))
    ]),

    html.Div([
        html.H2("Habit Correlation Heatmap"),
        dcc.Graph(figure=get_correlation_figure(df))
    ]),

    html.H1("Performance Group Comparison (Radar Chart)"),

    html.Div([
        html.Div([
            html.Label(h.replace("_", " ").capitalize(), 
                       style={
                            "marginRight": "10px", 
                            "width": "150px", 
                            "whiteSpace": "nowrap",
                            "lineHeight": "30px"
                        }),
            html.Div(
                dcc.Slider(
                    id=h,
                    min=slider_config[h]['min'],
                    max=slider_config[h]['max'],
                    step=slider_config[h]['step'],
                    value=(slider_config[h]['min'] + slider_config[h]['max']) / 2,
                    marks=(
                        {1: 'Poor', 2: 'Fair', 3: 'Good'} if h == 'diet_quality'
                        else {i: str(i) for i in range(
                            int(slider_config[h]['min']),
                            int(slider_config[h]['max']) + 1
                        )}
                    ),
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                style={"flex": "1", "height": "30px"}
            )
        ], style={
            "width": "75%",
            "margin": "0 auto",
            "display": "flex",
            "alignItems": "center", 
            "justifyContent": "flex-start", 
            "marginBottom": "20px"
        })
        for h in habits 
    ]),

    html.Button("Compare My Habits", id='update-button', n_clicks=0),

    dcc.Graph(id='radar-chart', style={'width': '100%', 'height': '700px'}, figure=get_radar_chart(df))
])

# === CALLBACK ===
@app.callback(
    Output('radar-chart', 'figure'),
    Input('update-button', 'n_clicks'),
    [State(habit, 'value') for habit in habits]
)
def update_radar_chart(n_clicks, *user_values):
    habit_values = list(user_values)
    ranges = {
        'study_hours_per_day': (0, 9),
        'social_media_hours': (0, 7),
        'netflix_hours': (0, 6),
        'sleep_hours': (3, 10),
        'diet_quality': (1, 3),
        'exercise_frequency': (0, 6),
        'mental_health_rating': (1, 10)
    }

    normalized = [
        5 * (v - ranges[habit][0]) / (ranges[habit][1] - ranges[habit][0])
        for habit, v in zip(habits, habit_values)
    ]

    return get_radar_chart(df, user_data=normalized)
