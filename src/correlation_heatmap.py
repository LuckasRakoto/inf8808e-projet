import pandas as pd
import plotly.graph_objects as go

def get_correlation_figure(df):
    corr_vars = [
        'study_hours_per_day', 'social_media_hours', 'netflix_hours',
        'attendance_percentage', 'sleep_hours', 'exercise_frequency',
        'mental_health_ranking', 'exam_score'
    ]
    corr_df = df[corr_vars].dropna()
    corr_matrix = corr_df.corr().round(2)

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='YlOrRd',
        zmin=-1,
        zmax=1,
        colorbar=dict(title="Correlation"),
        hovertemplate='Correlation %{x} ↔ %{y}: %{z}<extra></extra>'
    ))
    fig.update_layout(
        title="Correlation Matrix of Students’ Habits",
        xaxis=dict(side="bottom"),
        yaxis=dict(autorange="reversed"),
        font=dict(color="white"),
        paper_bgcolor="black",
        plot_bgcolor="black"
    )
    return fig