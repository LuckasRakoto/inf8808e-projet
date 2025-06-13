import pandas as pd
import plotly.graph_objects as go

from preprocess import preprocess_sankey_chart_data

def get_sankey_chart_figure(df):
    
    habits = [
        "study_hours_per_day",
        "sleep_hours",
        "social_media_hours",
        "netflix_hours",
        "exercise_frequency",
        "mental_health_rating",
        "diet_quality_numeric"
    ]
    
    df = preprocess_sankey_chart_data(df)
    
    def prepare_sankey_data(left_type):
        """
        Precompute everything needed for a Sankey when left nodes are either "age" or "gender".
        Returns:
        - all_labels: list of left_labels + perf_labels
        - source_indices, target_indices: for links (in that fixed order)
        - values_by_habit[habit]: list of average-habit values (one entry per link)
        - link_customdata_by_habit[habit]: list of [perf, count, avg] per link
        - node_x, node_y, node_colors, node_hovertemplate
        - a helper make_node_hovertemplate(habit) to recompute node-hover when habit changes
        """
        # 1) Decide the left‐side categories & sort them
        if left_type == "age":
            left_values = sorted(df[left_type].unique(), reverse=True)
        else:
            left_values = sorted(df[left_type].unique())
        perf_labels = ["Low", "Mid", "Top"]

        # 2) Build node labels: left_labels (as strings) + perf_labels
        left_labels = [str(v) for v in left_values]
        all_labels = left_labels + perf_labels

        # 3) Map every label to its index in "all_labels"
        label_to_index = {lab: i for i, lab in enumerate(all_labels)}

        # 4) Enumerate ordered_pairs = [(lv, perf) for lv in left_values for perf in perf_labels]
        ordered_pairs = [(lv, perf) for lv in left_values for perf in perf_labels]

        # 5) Build source_indices and target_indices
        source_indices = [label_to_index[str(lv)] for (lv, _) in ordered_pairs]
        target_indices = [label_to_index[perf] for (_, perf) in ordered_pairs]

        # 6) For each habit, compute:
        #    - average habit value per (lv, perf)
        #    - count of students per (lv, perf)
        #    - link-hover lines that reference perf, count, avg
        values_by_habit = {}
        link_customdata_by_habit = {}
        # We'll build a hover‐template string using customdata:
        #   - customdata[0] = perf label
        #   - customdata[1] = count of students
        #   - customdata[2] = avg habit
        for habit in habits:
            avg_list = []
            customdata_list = []
            for (lv, perf) in ordered_pairs:
                subset = df[(df[left_type] == lv) & (df["PerformanceGroup"] == perf)]
                count = subset.shape[0]
                avg_val = subset[habit].mean() if count > 0 else 0.0
                avg_list.append(avg_val)
                customdata_list.append([perf, count, avg_val])
            values_by_habit[habit] = avg_list
            link_customdata_by_habit[habit] = customdata_list

        # 7) Compute fixed node‐positions (x,y):
        n_left = len(left_labels)
        n_perf = len(perf_labels)

        if n_left == 1:
            left_ys = [0.5]
        else:
            left_ys = [1.0 - i/(n_left - 1) for i in range(n_left)]
        perf_ys = [0.8, 0.5, 0.2]

        node_x = [0.0]*n_left + [1.0]*n_perf
        node_y = left_ys + perf_ys

        # 8) Node colors: left side = cornflowerblue; right side = red/orange/green
        node_colors = ["cornflowerblue"] * n_left
        perf_color_map = {"Low": "red", "Mid": "orange", "Top": "green"}
        node_colors += [perf_color_map[p] for p in perf_labels]

        # 9) Build node-hovertemplate **function**:
        #    When hovering on a left node (lv), we want:
        #      "Age (or Gender): lv
        #       Number of students: <count_of_all_students_with_lv>
        #       Avg {habit}: <avg_for_that_lv>"
        #
        #    When hovering on a right node (perf), we want:
        #      "Performance Group: perf
        #       Number of students: <count_of_all_students_in_perf>"
        #
        # Precompute left‐node counts & per‐habit averages for each left_value:
        left_data = []
        for lv in left_values:
            total_count = df[df[left_type] == lv].shape[0]
            # Compute average of each habit for that left_value:
            avg_by_habit = {h: df[df[left_type] == lv][h].mean() if total_count>0 else 0.0 for h in habits}
            left_data.append((lv, total_count, avg_by_habit))

        # Precompute right‐node counts:
        right_hover_static = []
        for perf in perf_labels:
            total_count = df[df["PerformanceGroup"] == perf].shape[0]
            right_hover_static.append(f"Performance: {perf}<br>Number of students: {total_count}<extra></extra>")

        # A helper to generate node‐hovertemplate list for a given habit:
        def make_node_hovertemplate(selected_habit):
            txts = []
            # left nodes first
            for (lv, cnt, avg_dict) in left_data:
                avg_val = avg_dict[selected_habit]
                txts.append(
                    f"{left_type.title()}: {lv}<br>"
                    f"Number of students: {cnt}<br>"
                    f"Avg {selected_habit}: {avg_val:.2f}<extra></extra>"
                )
            # then right nodes
            txts.extend(right_hover_static)
            return txts

        # Create initial node_hovertemplate for the first habit:
        initial_habit = habits[0]
        node_hovertemplate = make_node_hovertemplate(initial_habit)

        return {
            "all_labels": all_labels,
            "source_indices": source_indices,
            "target_indices": target_indices,
            "values_by_habit": values_by_habit,
            "link_customdata_by_habit": link_customdata_by_habit,
            "node_x": node_x,
            "node_y": node_y,
            "node_colors": node_colors,
            "node_hovertemplate": node_hovertemplate,
            "make_node_hovertemplate": make_node_hovertemplate
        }


    # Prepare data for "age" and "gender" upfront
    data_age = prepare_sankey_data("age")
    data_gender = prepare_sankey_data("gender")

    initial_left_type = "age"
    initial_habit = habits[0]

    def get_data(left_type):
        return data_age if left_type == "age" else data_gender

    dat = get_data(initial_left_type)

    # --- Build initial Sankey trace ---
    sankey_trace = go.Sankey(
        arrangement="fixed",
        domain=dict(x=[0,1], y=[0,1]),
        node=dict(
            label=dat["all_labels"],
            color=dat["node_colors"],
            x=dat["node_x"],
            y=dat["node_y"],
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            customdata=dat["node_hovertemplate"],
            hovertemplate="%{customdata}<extra></extra>"
        ),
        link=dict(
            source=dat["source_indices"],
            target=dat["target_indices"],
            value=dat["values_by_habit"][initial_habit],
            customdata=dat["link_customdata_by_habit"][initial_habit],
            hovertemplate=(
                "Performance: %{customdata[0]}<br>"
                "Number of students: %{customdata[1]}<br>"
                "Avg " + initial_habit + ": %{customdata[2]:.2f}<extra></extra>"
            )
        )
    )

    fig = go.Figure(data=[sankey_trace])

    # --- Dropdown for selecting habit (updates link.value, link.customdata & link.hovertemplate, and node-hovertemplate) ---
    habit_buttons = []
    for habit in habits:
        habit_buttons.append(dict(
            label=habit,
            method="restyle",
            args=[{
                # Update link values:
                "link.value": [dat["values_by_habit"][habit]],
                # Update link customdata (perf, count, avg_for_this_habit):
                "link.customdata": [dat["link_customdata_by_habit"][habit]],
                # Update link.hovertemplate to reference customdata array:
                "link.hovertemplate": [
                    "Performance: %{customdata[0]}<br>"
                    "Number of students: %{customdata[1]}<br>"
                    f"Avg {habit}: " + "%{customdata[2]:.2f}<extra></extra>"
                ],
                # Also update node.customdata & node.hovertemplate (show avg habit on left nodes)
                "node.customdata": [dat["make_node_hovertemplate"](habit)],
                "node.hovertemplate": ["%{customdata}<extra></extra>"]
            }]
        ))

    # --- Dropdown for selecting left_type ("age" or "gender") (updates entire node & link structure) ---
    left_type_buttons = []
    for ltype in ["age", "gender"]:
        d = get_data(ltype)
        left_type_buttons.append(dict(
            label=ltype.title(),
            method="update",
            args=[{
                # Node updates:
                "node.label": [d["all_labels"]],
                "node.color": [d["node_colors"]],
                "node.x": [d["node_x"]],
                "node.y": [d["node_y"]],
                "node.customdata": [d["make_node_hovertemplate"](initial_habit)],
                "node.hovertemplate": ["%{customdata}<extra></extra>"],
                # Link updates:
                "link.source": [d["source_indices"]],
                "link.target": [d["target_indices"]],
                "link.value": [d["values_by_habit"][initial_habit]],
                "link.customdata": [d["link_customdata_by_habit"][initial_habit]],
                "link.hovertemplate": [
                    "Performance: %{customdata[0]}<br>"
                    "Number of students: %{customdata[1]}<br>"
                    f"Avg {initial_habit}: " + "%{customdata[2]:.2f}<extra></extra>"
                ]
            }],
        ))

    fig.update_layout(
        title_text=f"Sankey: {initial_left_type.title()} (left) → PerformanceGroup (Avg {initial_habit})",
        font_size=12,
        updatemenus=[
            dict(
                buttons=left_type_buttons,
                direction="down",
                showactive=True,
                x=0.3,
                y=0.15,
                xanchor="right",
                yanchor="top",
                pad={"r": 10, "t": 10},
                bgcolor="lightgrey",
                bordercolor="grey",
                borderwidth=1,
                font=dict(size=12),
            ),
            dict(
                buttons=habit_buttons,
                direction="down",
                showactive=True,
                x=0.7,
                y=0.15,
                xanchor="right",
                yanchor="top",
                pad={"r": 10, "t": 10},
                bgcolor="lightgrey",
                bordercolor="grey",
                borderwidth=1,
                font=dict(size=12),
            )
        ],
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return fig