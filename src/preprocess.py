'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def get_groups_radar_chart(my_df):

    habits = ['study_hours_per_day', 'social_media_hours', 'netflix_hours',
               'sleep_hours','diet_quality', 'exercise_frequency',
              'mental_health_rating']
    
    df = my_df.dropna(subset=habits + ['exam_score'])

    df['diet_quality'] = df['diet_quality'].map({'Poor': 1, 'Fair': 2, 'Good' : 3})

    p85 = df['exam_score'].quantile(0.85)
    p50 = df['exam_score'].quantile(0.50)

    def assign_group(score):
        if score < p50: 
            return 'Low Performers'
        if score < p85:
            return 'Mid-Level Performers'
        elif score >= p50:
            return 'Top Performers'

    df['performance_group'] = df['exam_score'].apply(assign_group)

    scaler = MinMaxScaler()
    df_normalized = df.copy()
    df_normalized[habits] = scaler.fit_transform(df[habits])

    group_means = df_normalized.groupby('performance_group')[habits].mean().reset_index()

    order = ['Low Performers', 'Mid-Level Performers', 'Top Performers']
    group_means['performance_group'] = pd.Categorical(group_means['performance_group'], categories=order, ordered=True)
    group_means = group_means.sort_values('performance_group').reset_index(drop=True)


    return group_means