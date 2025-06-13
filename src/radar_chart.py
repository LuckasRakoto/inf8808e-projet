import pandas as pd
import plotly.graph_objects as go
from preprocess import get_groups_radar_chart

# Exemple de données normalisées entre 0 et 1

def get_radar_chart(df, user_data=None):
    # Liste des habitudes (mêmes que dans ton code)
    habits = ['study_hours_per_day', 'social_media_hours', 'netflix_hours',
              'sleep_hours','diet_quality', 'exercise_frequency',
              'mental_health_rating']

    colors = {
        'Low Performers': 'red',
        'Mid-Level Performers': 'orange',
        'Top Performers': 'green',
        'You': 'blue'
    }

    labels = ['Study Hours', 'Social Media Hours', 'Netflix Hours',
          'Sleep Hours', 'Diet Quality', 'Exercise Frequency',
          'Mental Health Rating']

    categories = get_groups_radar_chart(df)

    fig = go.Figure()

    order = ['Top Performers', 'Mid-Level Performers','Low Performers']

    for group in order:
        row = categories[categories['performance_group'] == group]
        if not row.empty:
            row = row.iloc[0]
            fig.add_trace(go.Scatterpolar(
                r=row[habits].tolist() + [row[habits[0]]],  # boucler
                theta=labels + [labels[0]],
                fill='toself',
                name=group,
                line=dict(color=colors.get(group, 'gray'))
            ))

    if user_data:
        fig.add_trace(go.Scatterpolar(
            r=user_data + [user_data[0]],
            theta=labels + [labels[0]],
            fill='toself',
            name="You",
            line=dict(color=colors['You'], dash='dash')
        ))

    fig.update_layout(
        legend=dict(traceorder='normal'),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=True,
        title="Comparison between groupes based on habits"
    )


    return fig