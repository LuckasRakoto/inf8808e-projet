import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def get_cluster_figure(df):
    habits = [
        'sleep_hours', 'study_hours_per_day', 'netflix_hours',
        'mental_health_rating', 'social_media_hours', 'attendance_percentage'
    ]
    df = df.dropna(subset=habits + ['gender'])
    X = StandardScaler().fit_transform(df[habits])
    pca = PCA(n_components=2)
    df[['PC1', 'PC2']] = pca.fit_transform(X)
    kmeans = KMeans(n_clusters=4, random_state=0)
    df['cluster'] = kmeans.fit_predict(X)

    cluster_labels = {
        0: "The Bookworm",
        1: "The Balanced Learner",
        2: "The Media Addict",
        3: "The Minimalist"
    }
    df['cluster_name'] = df['cluster'].map(cluster_labels)

    grouped = df.groupby("cluster").agg({
        'sleep_hours': 'mean',
        'study_hours_per_day': 'mean',
        'netflix_hours': 'mean',
        'social_media_hours': 'mean',
        'gender': lambda g: 100 * (g == 'female').mean()
    }).round(1)

    def make_profile(row):
        return (
            f"<b>{cluster_labels[row.name]}</b><br>"
            f"Sleep: {row['sleep_hours']} hrs<br>"
            f"Study: {row['study_hours_per_day']} hrs<br>"
            f"Screen Time: {row['netflix_hours']} hrs<br>"
            f"Social Media: {row['social_media_hours']} hrs<br>"
            f"% Female: {row['gender']}%"
        )

    df['hover_card'] = df['cluster'].map(grouped.apply(make_profile, axis=1).to_dict())

    fig = px.scatter(
        df, x='PC1', y='PC2',
        color='cluster_name',
        hover_name='hover_card',
        title='Patterns of Success: Student Profiles and Habit Clusters'
    )
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color='black')))
    fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=12))

    return fig