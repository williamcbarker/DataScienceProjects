import os

from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px


app = Dash()

os.chdir(os.path.dirname(__file__))


features_df = pd.read_csv("ai_productivity_features1.csv")
targets_df = pd.read_csv("ai_productivity_targets1.csv")
burnout_df = pd.read_csv("ai_worker_burnout_attrition_2026.csv")
company_df = pd.read_csv("ai_company_adoption4.csv")
industry_df = pd.read_csv("ai_industry_summary4.csv")
country_df = pd.read_csv("country_ai_index4.csv")

productivity_df = features_df.merge(targets_df, on="Employee_ID", how="inner")
company_enriched_df = company_df.merge(industry_df, on="industry", how="left")
company_enriched_df = company_enriched_df.merge(country_df, on=["country", "region"], how="left")

model_comparison_df = pd.read_csv("models/model_comparison.csv")
cluster_summary_df = pd.read_csv("models/cluster_summary.csv")


colors = {
    "background": "#f6f7fb",
    "card": "white",
    "text": "#1f2937",
    "muted": "#667085",
    "accent": "#2563eb",
}

card_style = {
    "backgroundColor": colors["card"],
    "border": "1px solid #e5e7eb",
    "borderRadius": "8px",
    "padding": "16px",
    "boxShadow": "0 1px 2px rgba(16, 24, 40, 0.05)",
}

grid_style = {
    "display": "grid",
    "gridTemplateColumns": "repeat(auto-fit, minmax(260px, 1fr))",
    "gap": "16px",
    "marginBottom": "16px",
}

tab_style = {
    "padding": "12px",
    "fontWeight": "600",
}

selected_tab_style = {
    "padding": "12px",
    "fontWeight": "700",
    "borderTop": f"3px solid {colors['accent']}",
    "color": colors["accent"],
}


def metric_card(title, value, subtitle):
    return html.Div(
        [
            html.Div(title, style={"fontSize": "14px", "color": colors["muted"]}),
            html.Div(value, style={"fontSize": "28px", "fontWeight": "700", "color": colors["text"]}),
            html.Div(subtitle, style={"fontSize": "13px", "color": colors["muted"]}),
        ],
        style=card_style,
    )


def format_fig(fig):
    fig.update_layout(
        paper_bgcolor=colors["card"],
        plot_bgcolor="white",
        font_color=colors["text"],
        title_x=0.02,
        margin=dict(l=40, r=20, t=60, b=40),
        legend_title_text="",
    )
    return fig


top_industry_df = (
    company_df.groupby("industry", as_index=False)
    .agg(
        avg_productivity_change=("productivity_change_percent", "mean"),
        avg_innovation_score=("innovation_score", "mean"),
        avg_revenue_growth=("revenue_growth_percent", "mean"),
        avg_cost_reduction=("cost_reduction_percent", "mean"),
        avg_ai_adoption_rate=("ai_adoption_rate", "mean"),
    )
    .round(2)
    .sort_values("avg_productivity_change", ascending=False)
)

role_threat_df = (
    burnout_df.groupby("job_role", as_index=False)
    .agg(
        avg_task_replacement_pct=("ai_replaces_my_tasks_pct", "mean"),
        avg_burnout_score=("burnout_score", "mean"),
        avg_productivity_score=("productivity_score", "mean"),
        avg_job_satisfaction=("job_satisfaction_1_5", "mean"),
    )
    .round(2)
    .sort_values("avg_task_replacement_pct", ascending=False)
)

ai_usage_df = productivity_df.copy()
ai_usage_df["ai_usage_bucket"] = pd.qcut(
    ai_usage_df["ai_tool_usage_hours_per_week"],
    q=5,
    labels=["Very low", "Low", "Medium", "High", "Very high"],
)
ai_usage_summary_df = (
    ai_usage_df.groupby("ai_usage_bucket", observed=True, as_index=False)
    .agg(
        avg_ai_hours=("ai_tool_usage_hours_per_week", "mean"),
        avg_productivity=("productivity_score", "mean"),
        avg_burnout=("burnout_risk_score", "mean"),
        avg_manual_hours=("manual_work_hours_per_week", "mean"),
        avg_tasks_automated=("tasks_automated_percent", "mean"),
    )
    .round(2)
)


fig_ai_productivity = px.scatter(
    productivity_df,
    x="ai_tool_usage_hours_per_week",
    y="productivity_score",
    color="burnout_risk_level",
    title="AI Tool Usage vs Productivity",
    labels={
        "ai_tool_usage_hours_per_week": "AI usage hours per week",
        "productivity_score": "Productivity score",
        "burnout_risk_level": "Burnout risk",
    },
)
fig_ai_productivity = format_fig(fig_ai_productivity)

fig_usage_bucket = px.bar(
    ai_usage_summary_df,
    x="ai_usage_bucket",
    y=["avg_productivity", "avg_burnout"],
    barmode="group",
    title="Productivity and Burnout by AI Usage Bucket",
    labels={
        "ai_usage_bucket": "AI usage bucket",
        "value": "Average score",
        "variable": "Metric",
        "avg_productivity": "Avg Productivity",
        "avg_burnout": "Avg Burnout"
    },
)
fig_usage_bucket = format_fig(fig_usage_bucket)

fig_industry = px.bar(
    top_industry_df.sort_values("avg_productivity_change"),
    x="avg_productivity_change",
    y="industry",
    color="avg_innovation_score",
    title="Industries Benefiting Most From AI",
    labels={
        "avg_productivity_change": "Avg productivity change (%)",
        "industry": "Industry",
        "avg_innovation_score": "Avg innovation score",
    },
)
fig_industry = format_fig(fig_industry)

fig_roles = px.bar(
    role_threat_df.sort_values("avg_task_replacement_pct"),
    x="avg_task_replacement_pct",
    y="job_role",
    color="avg_burnout_score",
    title="Roles Reporting the Most AI Task Replacement",
    labels={
        "avg_task_replacement_pct": "Avg task replacement (%)",
        "job_role": "Job role",
        "avg_burnout_score": "Avg burnout score",
    },
)
fig_roles = format_fig(fig_roles)

fig_ml = px.bar(
    model_comparison_df,
    x="model",
    y="R2",
    color="model",
    title="ML Model Comparison: R-squared",
    labels={"model": "Model", "R2": "R-squared"},
)
fig_ml = format_fig(fig_ml)

fig_clusters = px.bar(
    cluster_summary_df,
    x="cluster",
    y=["avg_ai_hours", "avg_manual_hours", "avg_productivity", "avg_burnout"],
    barmode="group",
    title="K-Means Employee Segment Profiles",
    labels={"cluster": "Cluster", "value": "Average value", "variable": "Metric"},
)
fig_clusters = format_fig(fig_clusters)


app.layout = html.Div(
    [
    html.Div(
        [
            html.H1("AI Workplace Productivity Dashboard", style={"marginBottom": "4px"}),
            html.P(
                "Exploring AI adoption, productivity, burnout, ROI signals, and employee segments.",
                style={"color": colors["muted"], "marginTop": "0"},
            ),
        ],
        style={"marginBottom": "16px"},
    ),
    dcc.Tabs(
        [
            dcc.Tab(
                label="Overview",
                style=tab_style,
                selected_style=selected_tab_style,
                children=[
                    html.Div(
                        [
                            metric_card("Employee productivity records", f"{len(productivity_df):,}", "Joined feature and target rows"),
                            metric_card("Company survey responses", f"{len(company_df):,}", "AI adoption and ROI proxy data"),
                            metric_card("Average productivity score", f"{productivity_df['productivity_score'].mean():.1f}", "Employee productivity dataset"),
                            metric_card("Best regression R-squared", f"{model_comparison_df['R2'].max():.3f}", "From the ML notebook"),
                        ],
                        style={**grid_style, "marginTop": "16px"},
                    ),
                    html.Div(
                        [
                            html.Div([dcc.Graph(figure=fig_ai_productivity)], style=card_style),
                            html.Div([dcc.Graph(figure=fig_industry)], style=card_style),
                        ],
                        style=grid_style,
                    ),
                ],
            ),
            dcc.Tab(
                label="Worker Productivity",
                style=tab_style,
                selected_style=selected_tab_style,
                children=[
                    html.Div(
                        [
                            html.Div([dcc.Graph(figure=fig_ai_productivity)], style=card_style),
                            html.Div([dcc.Graph(figure=fig_usage_bucket)], style=card_style),
                        ],
                        style={**grid_style, "marginTop": "16px"},
                    ),
                    html.Div([dcc.Graph(figure=fig_roles)], style={**card_style, "marginBottom": "16px"}),
                ],
            ),
            dcc.Tab(
                label="Company and Industry",
                style=tab_style,
                selected_style=selected_tab_style,
                children=[
                    html.Div(
                        [
                            html.Div([dcc.Graph(figure=fig_industry)], style=card_style),
                            html.Div(
                                [
                                    html.H2("Explore Company AI Adoption by Industry"),
                                    dcc.Dropdown(
                                        options=sorted(company_df["industry"].unique()),
                                        value="Technology",
                                        id="industry-dropdown",
                                        clearable=False,
                                    ),
                                    dcc.Graph(id="industry-detail-chart"),
                                ],
                                style=card_style,
                            ),
                        ],
                        style={**grid_style, "marginTop": "16px"},
                    ),
                    html.Div(
                        [
                            html.H2("Top Industry Summary"),
                            dash_table.DataTable(
                                data=top_industry_df.to_dict("records"),
                                columns=[{"name": col, "id": col} for col in top_industry_df.columns],
                                page_size=9,
                                sort_action="native",
                                style_table={"overflowX": "auto"},
                                style_cell={"textAlign": "left", "padding": "8px", "fontFamily": "Arial"},
                                style_header={"fontWeight": "bold", "backgroundColor": "#eef2ff"},
                            ),
                        ],
                        style=card_style,
                    ),
                ],
            ),
            dcc.Tab(
                label="ML Segments",
                style=tab_style,
                selected_style=selected_tab_style,
                children=[
                    html.Div(
                        [
                            html.Div([dcc.Graph(figure=fig_ml)], style=card_style),
                            html.Div([dcc.Graph(figure=fig_clusters)], style=card_style),
                        ],
                        style={**grid_style, "marginTop": "16px"},
                    ),
                    html.Div(
                        [
                            html.H2("K-Means Cluster Summary"),
                            dash_table.DataTable(
                                data=cluster_summary_df.to_dict("records"),
                                columns=[{"name": col, "id": col} for col in cluster_summary_df.columns],
                                page_size=4,
                                sort_action="native",
                                style_table={"overflowX": "auto"},
                                style_cell={"textAlign": "left", "padding": "8px", "fontFamily": "Arial"},
                                style_header={"fontWeight": "bold", "backgroundColor": "#eef2ff"},
                            ),
                        ],
                        style=card_style,
                    ),
                ],
            ),
        ],
        style={"marginBottom": "16px"},
    ),
    ],
    style={
        "backgroundColor": colors["background"],
        "minHeight": "100vh",
        "padding": "24px",
        "fontFamily": "Arial, sans-serif",
        "color": colors["text"],
    },
)


@callback(
    Output("industry-detail-chart", "figure"),
    Input("industry-dropdown", "value"),
)
def update_industry_chart(selected_industry):
    filtered_df = company_df[company_df["industry"] == selected_industry]

    summary_df = (
        filtered_df.groupby("ai_adoption_stage", as_index=False)
        .agg(
            avg_productivity_change=("productivity_change_percent", "mean"),
            avg_revenue_growth=("revenue_growth_percent", "mean"),
            avg_cost_reduction=("cost_reduction_percent", "mean"),
            avg_failure_rate=("ai_failure_rate", "mean"),
        )
        .round(2)
    )

    chart_df = summary_df.melt(
        id_vars="ai_adoption_stage",
        value_vars=[
            "avg_productivity_change",
            "avg_revenue_growth",
            "avg_cost_reduction",
            "avg_failure_rate",
        ],
        var_name="metric",
        value_name="average_value",
    )

    fig = px.bar(
        chart_df,
        x="ai_adoption_stage",
        y="average_value",
        color="metric",
        barmode="group",
        title=f"{selected_industry}: AI Adoption Stage and ROI Proxy Metrics",
        labels={
            "ai_adoption_stage": "AI adoption stage",
            "average_value": "Average value",
            "metric": "Metric",
        },
    )
    return format_fig(fig)


if __name__ == "__main__":
    app.run(debug=False)
