from dash import html

def no_clicks(style):
    """
    Handle case where no marker is clicked: hide panel
    """
    style["display"] = "none"
    return None, None, None, style

def map_marker_clicked(figure, curve, point, title, mode, theme, style):
    """
    Handle marker click: show profile info panel

    Args:
        figure: current figure dict
        curve: index of curve clicked
        point: index of marker clicked
        title: current panel title (unused)
        mode: current panel subtitle (unused)
        theme: current panel theme/content (unused)
        style: current panel CSS style dict

    Returns:
        updated (title, mode, theme, style)
    """
    # Extract clicked marker data (customdata assumed to be dict with needed info)
    selected_marker = figure["data"][curve]["customdata"][point]

    # Expected keys in selected_marker: 
    # 'profile', 'color', 'description', plus averages of metrics (study_hours, social_media_hours, etc.)

    profile_name = selected_marker.get('profile', 'Unknown Profile')
    color = selected_marker.get('color', '#000000')
    description = selected_marker.get('description', '')

    # Build title with profile name in cluster color
    title = html.Div(profile_name, style={"color": color, "fontSize": "24px", "fontWeight": "bold"})

    # Subtitle description under title
    mode = html.Div(description, style={"fontStyle": "italic", "marginBottom": "10px"})

    # Metrics to display in ordered list (adjust keys as per your data)
    metric_keys = [
        "study_hours_per_day", "social_media_hours", "netflix_hours",
        "attendance_percentage", "sleep_hours", "exercise_frequency",
        "mental_health", "exam_score", "PC1", "PC2"
    ]

    # Build list items only for metrics available in selected_marker
    list_items = []
    for key in metric_keys:
        if key in selected_marker:
            # Format metric name to readable label
            label = key.replace('_', ' ').capitalize()
            value = selected_marker[key]
            if isinstance(value, float):
                value = round(value, 2)
            list_items.append(html.Li(f"{label}: {value}"))

    theme = html.Div([
        html.Div("Cluster averages:", style={"marginBottom": "5px", "fontWeight": "bold"}),
        html.Ol(list_items)
    ])

    # Show panel
    style["display"] = "block"

    return title, mode, theme, style
