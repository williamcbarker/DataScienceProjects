import csv
import os
from pathlib import Path

import psycopg2
from airflow.decorators import dag, task
from pendulum import datetime


PROJECT_DIR = Path("/opt/airflow/project")
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA", "capstone")


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "host.docker.internal"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "cameronbarker"),
        password=os.getenv("POSTGRES_PASSWORD", ""),
    )


def table_name(name):
    return f"{POSTGRES_SCHEMA}.{name}"


def load_csv_to_table(csv_file: str, table_name: str, columns: list[str]):
    csv_path = PROJECT_DIR / csv_file
    column_list = ", ".join(columns)

    with get_connection() as conn:
        with conn.cursor() as cur:
            with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
                reader = csv.reader(file)
                header = next(reader)

                if header != columns:
                    raise ValueError(
                        f"{csv_file} columns do not match the expected table columns."
                    )

                copy_sql = f"""
                    COPY {table_name} ({column_list})
                    FROM STDIN
                    WITH CSV
                """
                cur.copy_expert(copy_sql, file)


@dag(
    dag_id="load_capstone_csvs",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
)
def load_capstone_csvs():
    @task
    def clear_tables():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    TRUNCATE TABLE
                        {table_name("ai_productivity_targets")},
                        {table_name("ai_productivity_features")},
                        {table_name("ai_company_adoption")},
                        {table_name("ai_industry_summary")},
                        {table_name("country_ai_index")},
                        {table_name("ai_worker_burnout_attrition")},
                        {table_name("ai_dev_productivity")}
                    RESTART IDENTITY CASCADE;
                    """
                )

    @task
    def load_productivity_features():
        load_csv_to_table(
            "ai_productivity_features1.csv",
            table_name("ai_productivity_features"),
            [
                "Employee_ID",
                "job_role",
                "experience_years",
                "ai_tool_usage_hours_per_week",
                "tasks_automated_percent",
                "manual_work_hours_per_week",
                "learning_time_hours_per_week",
                "deadline_pressure_level",
                "meeting_hours_per_week",
                "collaboration_hours_per_week",
                "error_rate_percent",
                "task_complexity_score",
                "focus_hours_per_day",
                "work_life_balance_score",
                "burnout_risk_score",
            ],
        )

    @task
    def load_productivity_targets():
        load_csv_to_table(
            "ai_productivity_targets1.csv",
            table_name("ai_productivity_targets"),
            ["Employee_ID", "productivity_score", "burnout_risk_level"],
        )

    @task
    def load_industry_summary():
        load_csv_to_table(
            "ai_industry_summary4.csv",
            table_name("ai_industry_summary"),
            [
                "industry",
                "avg_ai_adoption_rate",
                "avg_productivity_change_percent",
                "avg_ai_maturity_score",
                "avg_ai_failure_rate",
                "avg_jobs_displaced",
                "avg_jobs_created",
                "avg_customer_satisfaction",
            ],
        )

    @task
    def load_country_index():
        load_csv_to_table(
            "country_ai_index4.csv",
            table_name("country_ai_index"),
            [
                "country",
                "region",
                "gdp_per_capita",
                "internet_penetration",
                "digital_maturity_index",
                "country_ai_policy",
                "ai_patent_filings_2024",
                "ai_researchers_per_million",
            ],
        )

    @task
    def load_company_adoption():
        load_csv_to_table(
            "ai_company_adoption4.csv",
            table_name("ai_company_adoption"),
            [
                "response_id",
                "company_id",
                "survey_year",
                "quarter",
                "country",
                "region",
                "industry",
                "company_size",
                "num_employees",
                "annual_revenue_usd_millions",
                "company_founding_year",
                "company_age",
                "company_age_group",
                "ai_adoption_rate",
                "ai_adoption_stage",
                "years_using_ai",
                "ai_primary_tool",
                "num_ai_tools_used",
                "ai_use_case",
                "ai_projects_active",
                "ai_training_hours",
                "ai_budget_percentage",
                "ai_maturity_score",
                "ai_failure_rate",
                "ai_investment_per_employee",
                "regulatory_compliance_score",
                "data_privacy_level",
                "ai_ethics_committee",
                "ai_risk_management_score",
                "remote_work_percentage",
                "employee_satisfaction_score",
                "task_automation_rate",
                "time_saved_per_week",
                "productivity_change_percent",
                "jobs_displaced",
                "jobs_created",
                "reskilled_employees",
                "revenue_growth_percent",
                "cost_reduction_percent",
                "innovation_score",
                "customer_satisfaction",
                "survey_source",
                "data_collection_method",
            ],
        )

    @task
    def load_worker_burnout():
        load_csv_to_table(
            "ai_worker_burnout_attrition_2026.csv",
            table_name("ai_worker_burnout_attrition"),
            [
                "employee_id",
                "job_role",
                "years_experience",
                "education_level",
                "country",
                "industry",
                "company_size",
                "remote_work_type",
                "team_size",
                "salary_usd_k",
                "primary_ai_tool",
                "ai_tools_used_per_day",
                "hours_with_ai_assistance_daily",
                "ai_replaces_my_tasks_pct",
                "ai_adoption_stage",
                "weekly_ai_upskilling_hrs",
                "productivity_score",
                "burnout_score",
                "job_satisfaction_1_5",
                "fear_of_ai_replacement",
                "attrition_risk",
            ],
        )

    @task
    def load_dev_productivity():
        load_csv_to_table(
            "ai_dev_productivity.csv",
            table_name("ai_dev_productivity"),
            [
                "hours_coding",
                "coffee_intake_mg",
                "distractions",
                "sleep_hours",
                "commits",
                "bugs_reported",
                "ai_usage_hours",
                "cognitive_load",
                "task_success",
            ],
        )

    clear = clear_tables()

    features = load_productivity_features()
    targets = load_productivity_targets()

    industry = load_industry_summary()
    country = load_country_index()
    company = load_company_adoption()

    worker = load_worker_burnout()
    dev = load_dev_productivity()

    clear >> features >> targets
    clear >> [industry, country] >> company
    clear >> [worker, dev]


load_capstone_csvs()
