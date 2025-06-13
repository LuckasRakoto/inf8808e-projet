import pandas as pd
import plotly.graph_objects as go

def get_bar_chart_figure(df):
    habits = [
        'study_hours_per_day', 'sleep_hours', 'social_media_hours', 'netflix_hours',
        'exercise_frequency', 'mental_health_rating', 'diet_quality_numeric',
    ]
    
    pretty_labels = [
        'Study Hours per Day', 'Social Media Hours', 'Netflix Hours',
        'Sleep Hours', 'Diet Quality', 'Exercise Frequency', 'Mental Health Rating'
    ]
    
    diet_mapping = {'Poor': 1, 'Fair': 2, 'Good': 3}
    df['diet_quality_numeric'] = df['diet_quality'].map(diet_mapping)

    
    quantiles = df['exam_score'].quantile([0.25, 0.75])
    low_df = df[df['exam_score'] <= quantiles[0.25]]
    top_df = df[df['exam_score'] >= quantiles[0.75]]
    all_df = df

    low_means = low_df[habits].mean().round(2)
    top_means = top_df[habits].mean().round(2)
    all_means = all_df[habits].mean().round(2)

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=pretty_labels,
        y=top_means.values,
        name='Top Performers',
        marker_color='green',
        hovertemplate=hover_template("Top Performers"),
    ))
    
    fig.add_trace(go.Bar(
        x=pretty_labels,
        y=low_means.values,
        name='Low Performers',
        marker_color='red',
        hovertemplate=hover_template("Low Performers"),
    ))
    
    fig.add_trace(go.Bar(
        x=pretty_labels,
        y=all_means.values,
        name='All Students',
        marker_color='grey',
        hovertemplate=hover_template("All Students"),
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
    return (f"Group: {group}<br>"
            "Habit: %{x}<br>"
            "Average: %{y:.2f}<extra></extra>")

