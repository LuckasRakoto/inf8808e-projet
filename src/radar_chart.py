import pandas as pd
import plotly.graph_objects as go
from src.preprocess import get_groups_radar_chart
from src.hover_template import get_radar_hover_template


def get_radar_chart(df, user_data=None):
    habits = ['study_hours_per_day', 'social_media_hours', 'netflix_hours',
              'sleep_hours','diet_quality', 'exercise_frequency',
              'mental_health_rating']

    colors = {
        'Low Performers': '#cc6041',
        'Mid-Level Performers': '#ffce67',
        'Top Performers': '#6DD2B0',
        'You': '#569caa'
    }

    labels = ['Study Hours', 'Social Media Hours', 'Netflix Hours',
          'Sleep Hours', 'Diet Quality', 'Exercise Frequency',
          'Mental Health Rating']
    
    habit_advice = {
        'study_hours_per_day': {
            'good': "Keep up the good work!",
            'bad': "Try increasing your study time to improve academic performance"
        },
        'social_media_hours': {
            'bad': "You’re managing your social media time well",
            'good': "Reducing social media use could help you focus more"
        },
        'netflix_hours': {
            'bad': "Nice balance on entertainment",
            'good': "Consider watching less Netflix to make room for more productive habits"
        },
        'sleep_hours': {
            'good': "You're getting a healthy amount of sleep!",
            'bad': "Better sleep habits can significantly improve your performance"
        },
        'diet_quality': {
            'good': "Great! You're maintaining a good diet",
            'bad': "Improving your diet could benefit your health and focus"
        },
        'exercise_frequency': {
            'good': "You're active enough — keep it up!",
            'bad': "Try to exercise more regularly for better mental and physical health"
        },
        'mental_health_rating': {
            'good': "Good mental health is key to success. Keep prioritizing it!",
            'bad': "Consider stress-reducing habits"
        }
    }

    categories, mid_means = get_groups_radar_chart(df)

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
                line=dict(color=colors.get(group, 'gray')),
                hovertemplate=get_radar_hover_template()
            ))

    if user_data:
        user_advice = [
            habit_advice[habit]['good'] if user_val >= mid_val else habit_advice[habit]['bad']
            for habit, user_val, mid_val in zip(habits, user_data, mid_means)
        ]
        user_advice = [wrap_text(a) for a in user_advice]

        fig.add_trace(go.Scatterpolar(
            r=user_data + [user_data[0]],
            theta=labels + [labels[0]],
            fill='toself',
            name="You",
            line=dict(color=colors.get("You", 'gray'), dash='dash'),
            customdata=user_advice + [user_advice[0]],
            hovertemplate=get_radar_hover_template(True)
        ))

    fig.update_layout(
        legend=dict(xanchor='right', yanchor='bottom', traceorder='normal'),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5])
        ),
        showlegend=True,
        transition=dict(
            duration=1000,
            easing='cubic-in-out'
        )
    )

    fig.update_layout(uirevision='constant')

    return fig

def wrap_text(text, max_length=20):
    # Break long strings into lines of max_length
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return "<br>".join(lines)
