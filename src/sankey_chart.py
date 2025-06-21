import plotly.graph_objects as go
import pandas as pd
import numpy as np

def get_sankey_chart_figure(df: pd.DataFrame, selected_left_type='age', selected_habit='study_hours_per_day'):
    # Mapping for dropdown to actual column names
    habit_column_map = {
        'study_hours_per_day': 'study_hours_per_day',
        'social_media_hours_per_day': 'social_media_hours',
        'netflix_hours_per_day': 'netflix_hours',
        'sleep_hours_per_day': 'sleep_hours',
        'diet_quality': 'diet_quality',
        'exercise_frequency_per_week': 'exercise_frequency',
        'mental_health_rating': 'mental_health_rating'
    }
    habit_col = habit_column_map[selected_habit]

    # Map for diet quality (categorical → numeric)
    quality_map = {'Poor': 1, 'Fair': 2, 'Good': 3}

    # Define habit bins (group values)
    def categorize_habit(value):
        try:
            value = float(value)
        except:
            return 'Unknown'

        if habit_col == 'diet_quality':
            return {1: 'Poor', 2: 'Fair', 3: 'Good'}.get(int(value), 'Unknown')
        elif habit_col == 'mental_health_rating':
            return 'Low' if value < 4 else 'Mid' if value < 7 else 'High'
        else:
            return 'Low' if value < 2 else 'Mid' if value < 5 else 'High'

    # Add habit group column
    if habit_col not in df.columns:
        return go.Figure()  # empty chart fallback
    habit_series = df[habit_col]
    if habit_col == 'diet_quality':
        habit_series = habit_series.map(quality_map)
    df['habit_group'] = habit_series.apply(categorize_habit)

    # Get node labels
    left_nodes = sorted(df[selected_left_type].dropna().unique().tolist())
    right_nodes = ['Low', 'Mid', 'High'] if habit_col != 'diet_quality' else ['Poor', 'Fair', 'Good']
    labels = left_nodes + right_nodes
    label_to_index = {label: i for i, label in enumerate(labels)}

    # Build links
    source = []
    target = []
    values = []
    link_hover = []

    for l in left_nodes:
        for r in right_nodes:
            subset = df[(df[selected_left_type] == l) & (df['habit_group'] == r)]
            count = len(subset)
            if count > 0:
                source.append(label_to_index[l])
                target.append(label_to_index[r])
                values.append(count)
                link_hover.append(
                    f"{selected_left_type.capitalize()}: {l}<br>Habit group: {r}<br>Students: {count}"
                )

    # Colors
    left_color = 'rgba(58, 129, 191, 0.8)'  # blue
    right_colors_map = {
        'Low': 'rgba(219, 64, 82, 0.8)',     # red
        'Mid': 'rgba(255, 192, 0, 0.8)',     # yellow
        'High': 'rgba(44, 160, 44, 0.8)',    # green
        'Poor': 'rgba(219, 64, 82, 0.8)',
        'Fair': 'rgba(255, 192, 0, 0.8)',
        'Good': 'rgba(44, 160, 44, 0.8)'
    }

    node_colors = [left_color] * len(left_nodes) + [right_colors_map[r] for r in right_nodes]
    link_colors = [left_color] * len(source)  # consistent for simplicity

    fig = go.Figure(go.Sankey(
        arrangement='snap',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=labels,
            color=node_colors,
            hovertemplate='%{label}<extra></extra>'
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color=link_colors,
            customdata=link_hover,
            hovertemplate='%{customdata}<extra></extra>'
        )
    ))

    fig.update_layout(
        title_text=f"Flow from {selected_left_type.capitalize()} to Habit Group ({selected_habit.replace('_', ' ').capitalize()})",
        font_size=14,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig
