
'''
    Provides the template for the tooltips.
'''


def get_radar_hover_template(user=False):
    if user:
        return (
            "<b>Habit:</b> %{theta}<br>"
            "<b>Your value:</b> %{r:.2f}<br>"
            "<b>Advice:</b> %{customdata}<extra></extra>"
        )
    else:
        return (
            "<b>Group:</b> %{fullData.name}<br>"
            "<b>Habit:</b> %{theta}<br>"
            "<b>Average value:</b> %{r:.2f}<extra></extra>"
        )



