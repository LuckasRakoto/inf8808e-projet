import pandas as pd
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

def get_correlation_figure(df, selected_cluster='All students'):
    df = assign_cluster_labels(df)

    corr_vars = [
        'study_hours_per_day', 'social_media_hours', 'netflix_hours',
        'attendance_percentage', 'sleep_hours', 'exercise_frequency',
        'mental_health_rating', 'exam_score'
    ]

    habits_names = {
        'study_hours_per_day': 'Study Hours Per Day',
        'social_media_hours': 'Social Media Hours',
        'netflix_hours': 'Netflix Hours',
        'attendance_percentage': 'Attendance (%)',
        'sleep_hours': 'Sleep Hours',
        'exercise_frequency': 'Exercise Frequency',
        'mental_health_rating': 'Mental Health Rating',
        'exam_score': 'Exam Score'
    }

    df_corr = df[corr_vars + ['cluster_name']].dropna()

    if selected_cluster == "All students":
        subset = df_corr[corr_vars]
    else:
        subset = df_corr[df_corr['cluster_name'] == selected_cluster][corr_vars]

    corr_matrix = subset.corr().round(2)
    corr_matrix.rename(columns=habits_names, index=habits_names, inplace=True)

    hovertext = [
        [
            f"<b>{x}</b> vs <b>{y}</b><br>Correlation: {corr_matrix.loc[y, x]:.2f}<br>{interpret_correlation(corr_matrix.loc[y, x])}"
            for x in corr_matrix.columns
        ]
        for y in corr_matrix.index
    ]

    fig = go.Figure(go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        text=hovertext,
        hoverinfo="text", 
        zmin=-1, zmax=1,
        colorscale='YlOrRd',
        colorbar=dict(
            title=dict(
                text="Correlation",
                font=dict(size=14, color="black"),
                side="right"
            ),
            len=0.8,           # length of the colorbar (80% of plot height)
            y=0.5,             # center vertically (0 bottom, 1 top)
            yanchor="middle",  # anchor y position in the middle
            thickness=20       # width of the colorbar
        )
    ))

    fig.update_layout(
        title=f'Correlation Matrix - {selected_cluster}',
        xaxis=dict(side="bottom"),
        yaxis=dict(autorange="reversed"),
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="black",
        height=700
    )
    

    return fig


def interpret_correlation(r):
    if r >= 0.7:
        return "Strong positive relationship"
    elif r >= 0.4:
        return "Moderate positive correlation"
    elif r >= 0.1:
        return "Weak positive relationship"
    elif r <= -0.7:
        return "Strong negative relationship"
    elif r <= -0.4:
        return "Moderate negative correlation"
    elif r <= -0.1:
        return "Weak negative relationship"
    else:
        return "No meaningful correlation"
    

