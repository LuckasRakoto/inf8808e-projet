import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def get_cluster_figure(df):
    # Features used for clustering
    habits = [
        'study_hours_per_day', 'social_media_hours', 'netflix_hours',
        'exercise_frequency', 'exam_score','sleep_hours','mental_health_rating',
        'social_media_hours', 'attendance_percentage'
    ]
    
    # Drop rows with missing required fields
    df = df.dropna(subset=habits + ['gender', 'age', 'extracurricular_participation', 'part_time_job'])
    
    # Normalize
    X = StandardScaler().fit_transform(df[habits])
    # PCA for 2D projection
    pca = PCA(n_components=2)
    df[['PC1', 'PC2']] = pca.fit_transform(X)
    # Clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)

    # Define personas
    cluster_map = {
        0: {'name': 'The Academic Achiever', 'color': '#1f77b4', 'desc': 'Focused, healthy and top of the class.'},
        1: {'name': 'The Balanced Learner', 'color': '#2ca02c', 'desc': 'Stable academic and personal life balance.'},
        2: {'name': 'The Social Butterfly', 'color': '#ff7f0e', 'desc': 'Socially active, academically inconsistent.'},
        3: {'name': 'The Minimalist', 'color': '#d62728', 'desc': 'Low engagement, just getting by.'}
    }
    # Assign profile names/colors/descriptions
    df['profile'] = df['cluster'].map(lambda x: cluster_map[x]['name'])
    df['color'] = df['cluster'].map(lambda x: cluster_map[x]['color'])
    df['description'] = df['cluster'].map(lambda x: cluster_map[x]['desc'])

    # Build rich hover text (to match marker color)
    def make_hover(row):
        return (
            f"<span style='background-color:{row['color']}; padding:5px; display:block;'>"
            f"<b>{row['profile']}</b></span><br>"
            f"Gender: {row['gender']}<br>"
            f"Age: {row['age']}<br>"
            f"Extracurricular: {row['extracurricular_participation']}<br>"
            f"Part-time Job: {row['part_time_job']}"
        )

    df['hover_card'] = df.apply(make_hover, axis=1)

    # Create figure manually for better control
    fig = go.Figure()
    for cluster_id, group in df.groupby('cluster'):
        fig.add_trace(go.Scatter(
            x=group['PC1'],
            y=group['PC2'],
            mode='markers',
            name=cluster_map[cluster_id]['name'],
            marker=dict(size=10, color=cluster_map[cluster_id]['color'], line=dict(width=1, color='black')),
            customdata=group[['hover_card']],
            hovertemplate="%{customdata[0]}<extra></extra>"
        ))

    fig.update_layout(
        title="Patterns of Success: Student Profiles and Habit Clusters",
        xaxis_title="PC1",
        yaxis_title="PC2",
        plot_bgcolor="white",
        hoverlabel=dict(font_size=12),
        legend_title="Profile"
    )
    
    return fig