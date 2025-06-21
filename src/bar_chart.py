import pandas as pd
import plotly.graph_objects as go

def get_bar_chart_figure(df):
    habits = [
        'study_hours_per_day', 'sleep_hours', 'social_media_hours', 'netflix_hours',
        'exercise_frequency', 'mental_health_rating', 'diet_quality_numeric',
    ]
    
    pretty_labels = [
        'Study Hours per Day', 'Sleep Hours', 'Social Media Hours', 'Netflix Hours',
         'Exercise Frequency', 'Mental Health Rating', 'Diet Quality'
    ]
    
    unit_by_label = {
        'Study Hours per Day': 'hours',
        'Sleep Hours': 'hours',
        'Social Media Hours': 'hours',
        'Netflix Hours': 'hours',
        'Exercise Frequency': 'times/week',
        'Mental Health Rating': '(1–10 scale)',
        'Diet Quality': '(1–3 scale)',
    }
    
    diet_mapping = {'Poor': 1, 'Fair': 2, 'Good': 3}
    df['diet_quality_numeric'] = df['diet_quality'].map(diet_mapping)
     
    quantiles = df['exam_score'].quantile([0.4, 0.8])
    low_df = df[df['exam_score'] <= quantiles[0.4]]
    top_df = df[df['exam_score'] >= quantiles[0.8]]
    all_df = df
    

    low_means = low_df[habits].mean().round(2)
    top_means = top_df[habits].mean().round(2)
    all_means = all_df[habits].mean().round(2)

    fig = go.Figure()

    
    for means, name in zip(
        [top_means, low_means, all_means],
        ['Top Performers', 'Low Performers', 'All Students']
    ):
        fig.add_trace(go.Bar(
            x=pretty_labels,
            y=means.values,
            name=name,
            customdata=[
                [unit_by_label[label]] for label in pretty_labels
            ],
            hovertemplate=hover_template(name)
        ))

    fig.update_layout(
        title="Average Student Habits by Performance Group",
        xaxis_title="Habits",
        yaxis_title="Average Value",
        barmode='group',
        template="plotly_white"
    )
    fig.update_yaxes(tickformat=".2f")

    return fig

def hover_template(group):
    return (
        f"Group: {group}<br>"
        "Habit: %{x}<br>"
        "Average: %{y:.2f} %{customdata[0]}<extra></extra>"
    )

