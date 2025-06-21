import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

from correlation_heatmap import get_correlation_figure, assign_cluster_labels
from cluster_scatter import get_cluster_figure
from radar_chart import get_radar_chart
from bar_chart import get_bar_chart_figure
from waffle_chart import get_waffle_figure
from sankey_chart import get_sankey_chart_figure

app = dash.Dash(__name__)
server = app.server
app.title = 'Student Habits vs Performance'

df = pd.read_csv("assets/data/student_habits_performance.csv")
df_clustered = assign_cluster_labels(df)
available_clusters = ["All students"] + sorted(df_clustered['cluster_name'].unique())

habits = [
    'study_hours_per_day', 'social_media_hours_per_day', 'netflix_hours_per_day',
    'sleep_hours_per_day', 'diet_quality', 'exercise_frequency_per_week',
    'mental_health_rating'
]

slider_config = {
    'study_hours_per_day': {'min': 0, 'max': 9, 'step': 1},
    'social_media_hours_per_day': {'min': 0, 'max': 7, 'step': 1},
    'netflix_hours_per_day': {'min': 0, 'max': 6, 'step': 1},
    'sleep_hours_per_day': {'min': 3, 'max': 10, 'step': 1},
    'diet_quality': {'min': 1, 'max': 3, 'step': 1},
    'exercise_frequency_per_week': {'min': 0, 'max': 6, 'step': 1},
    'mental_health_rating': {'min': 1, 'max': 10, 'step': 1}
}

# Sankey dropdown options
sankey_left_type_options = [
    {'label': 'Age', 'value': 'age'},
    {'label': 'Gender', 'value': 'gender'}
]

sankey_habit_options = [
    {'label': 'Study Hours per Day', 'value': 'study_hours_per_day'},
    {'label': 'Sleep Hours per Day', 'value': 'sleep_hours_per_day'},
    {'label': 'Social Media Hours per Day', 'value': 'social_media_hours_per_day'},
    {'label': 'Netflix Hours per Day', 'value': 'netflix_hours_per_day'},
    {'label': 'Exercise Frequency per Week', 'value': 'exercise_frequency_per_week'},
    {'label': 'Mental Health Rating', 'value': 'mental_health_rating'},
    {'label': 'Diet Quality', 'value': 'diet_quality'}
]

waffle_desc = """The waffle chart visualizes the relationship between the students' academic performance and their parents' education level.
Each column group represents one of four parental education categories: None, High School, Bachelor, and Master.
Inside each group, colored squares indicate the number of students performing at different levels.
Hovering over each square reveals a tooltip with detailed information: the education level, performance tier, and number of students that fall into that specific combination."""

waffle_post_desc = "From what we see in the chart, a parent's education level doesn't strongly determine a student's performance. For example, having parents with a Master's degree doesn't necessarily mean a student will be a top performer, and students with parents who have no formal education can still perform well. This suggests that other factors beyond parental education play a more significant role in academic success."

sankey_desc = """The Sankey chart illustrates how students' demographic attributes (either age or gender) relate to their academic performance levels (Low, Mid, or Top). The flow between groups shows how students are distributed across performance categories based on their age or gender, with the width of each link representing the number of students. The color of each node indicates the group type and performance level.

Users can interact with the chart using two dropdown menus: one to switch between 'Age' and 'Gender' as the grouping variable on the left, and another to select a specific habit to visualize (e.g., study hours, sleep, exercise, etc.). Hovering over the links reveals the performance group, number of students, and the average value of the selected habit. Hovering over nodes gives a summary for each demographic or performance group."""

sankey_post_desc = """From the chart, we can see that there are variations in habits across different performance groups, but the patterns are not always consistent. For example, students with higher mental health ratings or more study hours don’t always fall into the top performance category. This suggests that while certain habits may influence performance, they are not the sole determining factors, and academic success likely depends on a combination of behaviors and other underlying factors."""

bar_post_desc = """
From this bar chart, we can see that the top 20% group generally exhibits healthier habits than the lowest 40% group. This suggests that certain lifestyle choices may be associated with academic success. The habits that stand out the most are:

- **Study Hours**: The top 20% group studies significantly more hours per day compared to the lowest 40%.
- **Social Media and Netflix**: The top group spends less time on social media and Netflix, indicating that they may prioritize their time more effectively.
- **Mental Health Rating**: The top performers have a higher average mental health rating, suggesting that mental well-being is linked to academic success.
"""

cluster_desc = """This scatter plot displays distinct student profiles based on daily habits and academic performance where each dot represents a student, colored by profile group: The Academic Achiever, The Social Butterfly, The Minimalist, or The Balanced Learner. 
Hover to get more insight and click for more details on the profiles. """


cluster_desc_post ="""These profiles were generated using the k-means clustering algorithm, which grouped students based on 8 key features. The 2D scatter plot displays a projection of these features using Principal Component Analysis (PCA), allowing similar student behavior patterns to appear closer together visually.

"""

correlation_desc = """The Habit Correlation Heatmap illustrates the strength and direction of relationships between various student habits. Each cell shows the correlation between two behaviors, with colors indicating positive or negative connections.
This chart helps identify how habits like study time, social media use, sleep, and attendance interact with each other. Hovering over a cell reveals the exact correlation value and a brief explanation to better understand these patterns.
This insight supports students and educators in recognizing habits that influence academic success and well-being."""


correlation_desc_post ="""From this chart, we can see that across all student profiles, study hours strongly correlate with higher exam scores, making it the most important factor for academic success. Excessive social media use negatively impacts exam performance and attendance, especially for Media Addicts and Balanced Learners. Sleep consistently shows positive links to exam results and mental health, highlighting its role in well-being and performance. Attendance correlates moderately with exam scores and is negatively affected by social media in some groups. Exercise has a small positive effect on both mental health and academics. Overall, good study habits, adequate sleep, and limited social media use are key to better academic outcomes and well-being.

"""
correlation_controls = html.Div([
    html.Label("Select Cluster Group:", style={
        'color': 'black',
        'fontSize': '18px',
        'fontWeight': '600',
        'textAlign': 'center',
        'display': 'block',
        'marginBottom': '10px'
    }),

    html.Div([
        dcc.Dropdown(
            id='cluster-dropdown',
            options=[{'label': name, 'value': name} for name in available_clusters],
            value='All students',
            clearable=False,
            style={'width': '300px'}
        )
    ], style={'margin': '0 auto', 'marginBottom': '30px', 'width': '300px'}),

    dcc.Graph(id='correlation-graph', figure=get_correlation_figure(df, selected_cluster='All students'))
])


# Create sections to compartmentalize the charts
def create_section(title, description, content, post_description=None, bgcolor="white", title_color="black", description_color="black"):
    return html.Div(
        className='section',
        style={
            'minHeight': '100vh',
            'backgroundColor': bgcolor,
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'padding': '20px',
            'boxSizing': 'border-box',
            'position': 'relative'
        },
        children=[
            html.Div(
                className='section-content',
                style={
                    'width': '90%',
                    'maxWidth': '1100px',
                    'margin': '0 auto',
                    'opacity': 0,
                    'transform': 'translateY(50px)',
                    'transition': 'all 0.8s ease-out',
                    'zIndex': 2,
                    'position': 'relative',
                    'paddingTop': '50px',
                    'paddingBottom': '50px',
                    'boxSizing': 'border-box'
                },
                children=[
                    html.H2(title, style={
                        'color': title_color,
                        'fontSize': '3rem',
                        'marginBottom': '20px',
                        'fontWeight': '700'
                    }),
                    html.P(description, style={
                        'color': description_color,
                        'fontSize': '1.5rem',
                        'marginBottom': '30px',
                        'fontWeight': '300',
                        'lineHeight': '1.4'
                    }),
                    html.Div(content, style={
                        'backgroundColor': 'rgba(255, 255, 255, 0.9)',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.15)'
                    }),
                    html.P(post_description, style={
                        'color': description_color,
                        'fontSize': '1.3rem',
                        'marginTop': '25px',
                        'fontWeight': '300',
                        'lineHeight': '1.4'
                    }) if post_description else None
                ]
            )
        ]
    )


#Slider and button
def slider_controls():
    return html.Div([
        html.Div([
            html.Label(
                h.replace("_", " ").capitalize(),
                htmlFor=h,
                style={
                    'width': '160px',
                    'display': 'inline-block',
                    'textAlign': 'right',
                    'marginRight': '15px',
                    'fontWeight': '600',
                    'lineHeight': '30px'
                }
            ),
            html.Div(
                dcc.Slider(
                    id=h,
                    min=slider_config[h]['min'],
                    max=slider_config[h]['max'],
                    step=slider_config[h]['step'],
                    value=(slider_config[h]['min'] + slider_config[h]['max']) / 2,
                    marks={1: 'Poor', 2: 'Fair', 3: 'Good'} if h == 'diet_quality' else {
                        i: str(i) for i in range(slider_config[h]['min'], slider_config[h]['max'] + 1)
                    },
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
                style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'middle'}
            )
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'marginBottom': '20px',
            'width': '100%',
            'maxWidth': '800px',
            'margin': '0 auto'
        }) for h in habits
    ] + [
        html.Div(
            html.Button("Compare My Habits", id='update-button', n_clicks=0, className='custom-btn-radar'),
            style={'textAlign': 'center', 'marginTop': '30px'}
        )
    ])

#Get the radar chart and the sliders aligned horizontally
def radar_section():
    return html.Div(
        style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'gap': '40px',
            'width': '100%',
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '20px 0',
            'flexWrap': 'wrap'
        },
        children=[
            html.Div(slider_controls(), style={'flex': '1', 'maxWidth': '600px'}),
            html.Div(
                dcc.Graph(id='radar-chart', figure=get_radar_chart(df), style={'height': '500px'}),
                style={'flex': '1', 'maxWidth': '600px'}
            )
        ]
    )

sections = [
    create_section("How Habits Impact Academic Performance", "Explore the average habits of the top 20% and the lowest 40% compared to all students.",
                   dcc.Graph(figure=get_bar_chart_figure(df)), 
                   bgcolor='#78c2ad',
                   title_color='white',
				   post_description=dcc.Markdown(bar_post_desc),
                   description_color='white'),
    create_section("Cluster-Based Scatterplot Profiles", "See the clustering patterns of student habits in the dataset.",
                   cluster_desc,
		   dcc.Graph(figure=get_cluster_figure(df)), 
                   bgcolor='#cc6041',
                   title_color='white',
		   post_description=dcc.Markdown(cluster_desc_post),
                   description_color='white'),
    create_section("Habit Correlation Heatmap", 
                   correlation_desc,
                   correlation_controls,
                   bgcolor='#569caa',
                   title_color='white',
                   post_description=dcc.Markdown(correlation_desc_post),
                   description_color='white'),
    create_section("Waffle Chart of Student Groups",
                   waffle_desc,
                   dcc.Graph(figure=get_waffle_figure(df)),
                   post_description=waffle_post_desc,
                   bgcolor='#f3969a',
                   title_color='white',
                   description_color='white'),
    create_section(
        "Sankey Chart of Habit Flows",
        sankey_desc,
        html.Div([  # Wrap these two inside one container
            html.Div([
                html.Label("Group By (Left Nodes):"),
                dcc.Dropdown(
                    id='sankey-left-dropdown',
                    options=sankey_left_type_options,
                    value='age',
                    clearable=False,
                    style={'width': '250px'}
                )
            ], style={'display': 'inline-block', 'marginRight': '40px'}),

            html.Div([
                html.Label("Habit Metric:"),
                dcc.Dropdown(
                    id='sankey-habit-dropdown',
                    options=sankey_habit_options,
                    value='study_hours_per_day',
                    clearable=False,
                    style={'width': '300px'}
                )
            ], style={'display': 'inline-block'}),

            dcc.Graph(id='sankey-graph', figure=get_sankey_chart_figure(df, selected_left_type='age', selected_habit='study_hours_per_day'))
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),  # single content argument ends here
        post_description=sankey_post_desc,
        bgcolor='#ffce67',
        title_color='white',
        description_color='white'
    ),

    create_section("Where Do You Fit In?",
                   "Everyone’s habits are unique! Use the sliders to generate a personal profile and see where you align or differ from other student groups. What can you learn from the data?",
                   radar_section(),
                   bgcolor='#6DD2B0',
                   title_color='white',
                   description_color='white')
]

app.layout = html.Div([
    html.Div([
        html.H1("Student Behavior Profiles & Academic Performance", style={
            'fontSize': '4rem',
            'textAlign': 'center',
            'margin': '20px 0 0 0', 
            'fontWeight': '700',
            'color':'white'
        }),
        html.P("Discover how lifestyle choices and study habits shape academic success. Explore behavior patterns across performance groups and see how your own habits compare to top performers and the student average..", style={
            'fontSize': '1.5rem',
            'textAlign': 'center',
            'margin': '0 0 40px 0',
            'color':'white'
        })
    ], style={
        'backgroundColor': '#343a40',
        'paddingTop': '10px',
        'paddingBottom': '10px',
    }),
    *sections,
    dcc.Markdown("""
        <style>
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
                40% {transform: translateY(-20px);}
                60% {transform: translateY(-10px);}
            }
            .section {
                scroll-snap-align: start;
            }
            body {
                scroll-snap-type: y mandatory;
                overflow-y: scroll;
            }
        </style>
    """, style={"display": "none"}),
    dcc.Store(id='scroll-position-store'),
    dcc.Store(id='blur-trigger')
])

# To update the hover of the button and the slider
app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            const btn = document.getElementById('update-button');
            if (btn) {
                setTimeout(() => btn.blur(), 100);  // keep blurring button
            }
            // Remove handle.blur() so dragging highlight works
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('blur-trigger', 'data'),
    Input('update-button', 'n_clicks')
)

app.clientside_callback(
    """
    function() {
        const sections = document.querySelectorAll('.section');
        function checkScroll() {
            sections.forEach(section => {
                const content = section.querySelector('.section-content');
                const rect = section.getBoundingClientRect();
                const windowHeight = window.innerHeight;
                if (rect.top < windowHeight * 0.75 && rect.bottom > windowHeight * 0.25) {
                    content.style.opacity = 1;
                    content.style.transform = 'translateY(0)';
                }
            });
        }
        checkScroll();
        window.addEventListener('scroll', checkScroll);
        return window.scrollY;
    }
    """,
    Output('scroll-position-store', 'data'),
    Input('scroll-position-store', 'data')
)


@app.callback(
    Output('radar-chart', 'figure'),
    Input('update-button', 'n_clicks'),
    [State(h, 'value') for h in habits]
)
def update_radar_chart(n_clicks, *user_values):
    if not user_values or any(v is None for v in user_values):
        return get_radar_chart(df)

    ranges = {
        'study_hours_per_day': (0, 9),
        'social_media_hours_per_day': (0, 7),
        'netflix_hours_per_day': (0, 6),
        'sleep_hours_per_day': (3, 10),
        'diet_quality': (1, 3),
        'exercise_frequency_per_week': (0, 6),
        'mental_health_rating': (1, 10)
    }

    normalized = [
        5 * (v - ranges[h][0]) / (ranges[h][1] - ranges[h][0])
        for h, v in zip(habits, user_values)
    ]

    return get_radar_chart(df, user_data=normalized)


@app.callback(
    Output('sankey-graph', 'figure'),
    [Input('sankey-habit-dropdown', 'value'),
     Input('sankey-left-dropdown', 'value')]
)
def update_sankey_chart(selected_habit, selected_left_type):
    return get_sankey_chart_figure(df, selected_left_type=selected_left_type, selected_habit=selected_habit)

@app.callback(
    Output('correlation-graph', 'figure'),
    Input('cluster-dropdown', 'value')
)
def update_correlation_figure(selected_cluster):
    return get_correlation_figure(df, selected_cluster)

if __name__ == '__main__':
    app.run_server(debug=True)
