#import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Fonction pour attribuer des clusters et noms
def assign_cluster_labels(df, n_clusters=4):
    habits = [
        'sleep_hours', 'study_hours_per_day', 'netflix_hours',
        'mental_health_rating', 'social_media_hours', 'attendance_percentage'
    ]
    df = df.dropna(subset=habits + ['gender'])

    X = StandardScaler().fit_transform(df[habits])
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    df['cluster'] = kmeans.fit_predict(X)

    cluster_labels = {
        0: "The Bookworm",
        1: "The Balanced Learner",
        2: "The Media Addict",
        3: "The Minimalist"
    }
    df['cluster_name'] = df['cluster'].map(cluster_labels).fillna("Cluster " + df['cluster'].astype(str))
    return df

# Fonction pour créer une heatmap de corrélation interactive
def get_correlation_figure(df):
    df = assign_cluster_labels(df)

    corr_vars = [
        'study_hours_per_day', 'social_media_hours', 'netflix_hours',
        'attendance_percentage', 'sleep_hours', 'exercise_frequency',
        'mental_health_rating', 'exam_score'
    ]

    df_corr = df[corr_vars + ['cluster_name']].dropna()
    fig = go.Figure()
    buttons = []

    clusters = df_corr['cluster_name'].unique().tolist()
    clusters = ["All students"] + clusters

    for i, cluster in enumerate(clusters):
        subset = df_corr[corr_vars] if cluster == "All students" else df_corr[df_corr['cluster_name'] == cluster][corr_vars]
        corr_matrix = subset.corr().round(2)

        fig.add_trace(go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            zmin=-1, zmax=1,
            colorscale='YlOrRd',
            visible=(i == 0),
            hovertemplate='Correlation %{x} ↔ %{y}: %{z}<extra></extra>'
        ))

        visibility = [False] * len(clusters)
        visibility[i] = True

        buttons.append(dict(
            label=cluster,
            method='update',
            args=[{'visible': visibility},
                  {'title': f'Correlation Matrix - {cluster}'}]
        ))

    fig.update_layout(
        title='Correlation Matrix - All students',
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=1.1,
            y=0.5
        )],
        xaxis=dict(side="bottom"),
        yaxis=dict(autorange="reversed"),
        font=dict(color="white"),
        paper_bgcolor="black",
        plot_bgcolor="black",
        height=700
    )

    return fig
