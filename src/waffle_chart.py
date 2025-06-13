import pandas as pd
import numpy as np
import plotly.graph_objects as go

from preprocess import preprocess_waffle_chart_data

def get_waffle_figure(df):
    df = preprocess_waffle_chart_data(df)
    counts = df.groupby(['parental_education_level', 'exam_score']).size().unstack(fill_value=0)

    education_levels = ['None', 'High School', 'Bachelor', 'Master']
    performance_levels = ['Low', 'Mid', 'Top']
    colors = {'Top': 'green', 'Mid': 'orange', 'Low': 'red'}

    # Create a lookup for totals per (education, performance)
    totals_lookup = {}
    for level in education_levels:
        for perf in performance_levels:
            count = counts.loc[level, perf] if (level in counts.index and perf in counts.columns) else 0
            totals_lookup[(level, perf)] = count

    # Waffle chart settings
    cols = 8
    group_gap = 2
    marker_size = 8
    scale_y = 1  # moderate vertical spacing

    x_vals, y_vals, color_vals, text_vals = [], [], [], []
    max_rows = 0
    group_rows = []

    # Calculate rows needed per education level
    for i, level in enumerate(education_levels):
        level_counts = counts.loc[level] if level in counts.index else pd.Series([0, 0, 0], index=performance_levels)
        total = level_counts.sum()
        rows = int(np.ceil(total / cols))
        group_rows.append(rows)
        if rows > max_rows:
            max_rows = rows

    # Build waffle squares (fill from top)
    for i, level in enumerate(education_levels):
        level_counts = counts.loc[level] if level in counts.index else pd.Series([0, 0, 0], index=performance_levels)
        rows = group_rows[i]

        x_offset = i * (cols + group_gap)
        pos = 0
        for perf in reversed(performance_levels):
            count_perf = level_counts.get(perf, 0)
            for _ in range(count_perf):
                row = pos // cols
                col = pos % cols
                x = x_offset + col
                y = row  # top aligned

                x_vals.append(x + 0.5)
                y_vals.append(y * scale_y + 0.5)
                color_vals.append(colors[perf])

                total_same = totals_lookup.get((level, perf), 0)
                hover_text = (
                    f"Education: {level}<br>"
                    f"Performance: {perf}<br>"
                    f"Total Students: {total_same}"
                )
                text_vals.append(hover_text)
                pos += 1

    # Create figure
    fig = go.Figure(data=go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='markers',
        marker=dict(size=marker_size, color=color_vals, symbol='square'),
        text=text_vals,
        hoverinfo='text'
    ))

    # Add group labels below each waffle group
    annotations = []
    for i, level in enumerate(education_levels):
        x_pos = i * (cols + group_gap) + cols / 2
        annotations.append(dict(
            x=x_pos, y=-1.2,
            text=f"<b>{level}</b>",
            showarrow=False,
            font=dict(size=10)
        ))

    # Add custom legend on the right
    for j, perf in enumerate(reversed(performance_levels)):
        annotations.append(dict(
            xref='paper', yref='paper',
            x=1.02, y=0.9 - j * 0.1,
            text=f"<span style='color:{colors[perf]}'><b>{perf}</b></span>",
            showarrow=False,
            font=dict(size=10)
        ))

    # Update layout
    fig.update_layout(
        title="Waffle Chart: Student Performance by Parental Education Level",
        annotations=annotations,
        dragmode=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(t=25, l=10, r=60, b=40),
        # width=500,
        height=max_rows * marker_size * scale_y * 1.5 + 50,
        plot_bgcolor='white'
    )

    fig.update_xaxes(range=[-1, len(education_levels) * (cols + group_gap)])
    fig.update_yaxes(range=[-2, max_rows * scale_y + 1], autorange='reversed')
    
    
    return fig