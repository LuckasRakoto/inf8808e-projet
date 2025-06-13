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

    scaler = MinMaxScaler(feature_range=(0,5))
    df_normalized = df.copy()
    df_normalized[habits] = scaler.fit_transform(df[habits])

    group_means = df_normalized.groupby('performance_group')[habits].mean().reset_index()

    order = ['Low Performers', 'Mid-Level Performers', 'Top Performers']
    group_means['performance_group'] = pd.Categorical(group_means['performance_group'], categories=order, ordered=True)
    group_means = group_means.sort_values('performance_group').reset_index(drop=True)

    mid_means_row = group_means[group_means['performance_group'] == 'Mid-Level Performers']
    mid_means = mid_means_row[habits].iloc[0].tolist() if not mid_means_row.empty else [2.5]*len(habits)


    return group_means, mid_means

def preprocess_waffle_chart_data(df):
    
    def categorize_score(score):
        if score >= 85:
            return 'Top'
        elif score >= 50:
            return 'Mid'
        else:
            return 'Low'
    
    df = df[['parental_education_level', 'exam_score']]
    df['exam_score'] = df['exam_score'].apply(categorize_score)
    df['parental_education_level'] = df['parental_education_level'].fillna('None')
    
    return df

def preprocess_sankey_chart_data(df):
    df["PerformanceGroup"] = "Mid"
    df.loc[df["exam_score"] >= 85, "PerformanceGroup"] = "Top"
    df.loc[df["exam_score"] <= 50, "PerformanceGroup"] = "Low"

    diet_map = {"Poor": 1, "Fair": 2, "Good": 3}
    df["diet_quality_numeric"] = df["diet_quality"].map(diet_map)
    
    return df