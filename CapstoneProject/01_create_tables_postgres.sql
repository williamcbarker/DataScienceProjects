DROP SCHEMA IF EXISTS capstone CASCADE;

CREATE SCHEMA IF NOT EXISTS capstone;

-- ---------------------------------------------------------------------------
-- Dataset 1: employee productivity features and productivity targets
-- Relationship: one-to-one using employee_id
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS capstone.ai_productivity_features (
    employee_id TEXT PRIMARY KEY,
    job_role TEXT,
    experience_years INTEGER,
    ai_tool_usage_hours_per_week DOUBLE PRECISION,
    tasks_automated_percent DOUBLE PRECISION,
    manual_work_hours_per_week DOUBLE PRECISION,
    learning_time_hours_per_week DOUBLE PRECISION,
    deadline_pressure_level TEXT,
    meeting_hours_per_week DOUBLE PRECISION,
    collaboration_hours_per_week DOUBLE PRECISION,
    error_rate_percent DOUBLE PRECISION,
    task_complexity_score INTEGER,
    focus_hours_per_day DOUBLE PRECISION,
    work_life_balance_score DOUBLE PRECISION,
    burnout_risk_score DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS capstone.ai_productivity_targets (
    employee_id TEXT PRIMARY KEY,
    productivity_score DOUBLE PRECISION,
    burnout_risk_level TEXT,
    CONSTRAINT fk_productivity_targets_employee
        FOREIGN KEY (employee_id)
        REFERENCES capstone.ai_productivity_features (employee_id)
);

-- ---------------------------------------------------------------------------
-- Dataset 2: developer productivity experiment
-- Relationship: standalone dataset, one row per coding session
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS capstone.ai_dev_productivity (
    dev_productivity_id BIGSERIAL PRIMARY KEY,
    hours_coding DOUBLE PRECISION,
    coffee_intake_mg INTEGER,
    distractions INTEGER,
    sleep_hours DOUBLE PRECISION,
    commits INTEGER,
    bugs_reported INTEGER,
    ai_usage_hours DOUBLE PRECISION,
    cognitive_load DOUBLE PRECISION,
    task_success INTEGER
);

-- ---------------------------------------------------------------------------
-- Dataset 3: worker burnout and attrition
-- Relationship: standalone employee survey dataset
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS capstone.ai_worker_burnout_attrition (
    employee_id TEXT PRIMARY KEY,
    job_role TEXT,
    years_experience INTEGER,
    education_level TEXT,
    country TEXT,
    industry TEXT,
    company_size TEXT,
    remote_work_type TEXT,
    team_size INTEGER,
    salary_usd_k INTEGER,
    primary_ai_tool TEXT,
    ai_tools_used_per_day INTEGER,
    hours_with_ai_assistance_daily DOUBLE PRECISION,
    ai_replaces_my_tasks_pct INTEGER,
    ai_adoption_stage TEXT,
    weekly_ai_upskilling_hrs DOUBLE PRECISION,
    productivity_score INTEGER,
    burnout_score INTEGER,
    job_satisfaction_1_5 DOUBLE PRECISION,
    fear_of_ai_replacement TEXT,
    attrition_risk TEXT
);

-- ---------------------------------------------------------------------------
-- Dataset 4: company AI adoption, industry summary, and country AI index
-- Relationships:
--   company adoption many-to-one industry summary using industry
--   company adoption many-to-one country index using country
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS capstone.ai_industry_summary (
    industry TEXT PRIMARY KEY,
    avg_ai_adoption_rate DOUBLE PRECISION,
    avg_productivity_change_percent DOUBLE PRECISION,
    avg_ai_maturity_score DOUBLE PRECISION,
    avg_ai_failure_rate DOUBLE PRECISION,
    avg_jobs_displaced DOUBLE PRECISION,
    avg_jobs_created DOUBLE PRECISION,
    avg_customer_satisfaction DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS capstone.country_ai_index (
    country TEXT PRIMARY KEY,
    region TEXT,
    gdp_per_capita DOUBLE PRECISION,
    internet_penetration DOUBLE PRECISION,
    digital_maturity_index DOUBLE PRECISION,
    country_ai_policy TEXT,
    ai_patent_filings_2024 INTEGER,
    ai_researchers_per_million DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS capstone.ai_company_adoption (
    response_id INTEGER PRIMARY KEY,
    company_id TEXT,
    survey_year INTEGER,
    quarter TEXT,
    country TEXT,
    region TEXT,
    industry TEXT,
    company_size TEXT,
    num_employees INTEGER,
    annual_revenue_usd_millions DOUBLE PRECISION,
    company_founding_year INTEGER,
    company_age INTEGER,
    company_age_group TEXT,
    ai_adoption_rate DOUBLE PRECISION,
    ai_adoption_stage TEXT,
    years_using_ai INTEGER,
    ai_primary_tool TEXT,
    num_ai_tools_used INTEGER,
    ai_use_case TEXT,
    ai_projects_active INTEGER,
    ai_training_hours DOUBLE PRECISION,
    ai_budget_percentage DOUBLE PRECISION,
    ai_maturity_score DOUBLE PRECISION,
    ai_failure_rate DOUBLE PRECISION,
    ai_investment_per_employee DOUBLE PRECISION,
    regulatory_compliance_score INTEGER,
    data_privacy_level TEXT,
    ai_ethics_committee TEXT,
    ai_risk_management_score INTEGER,
    remote_work_percentage DOUBLE PRECISION,
    employee_satisfaction_score DOUBLE PRECISION,
    task_automation_rate DOUBLE PRECISION,
    time_saved_per_week DOUBLE PRECISION,
    productivity_change_percent DOUBLE PRECISION,
    jobs_displaced INTEGER,
    jobs_created INTEGER,
    reskilled_employees INTEGER,
    revenue_growth_percent DOUBLE PRECISION,
    cost_reduction_percent DOUBLE PRECISION,
    innovation_score INTEGER,
    customer_satisfaction DOUBLE PRECISION,
    survey_source TEXT,
    data_collection_method TEXT,
    CONSTRAINT fk_company_industry
        FOREIGN KEY (industry)
        REFERENCES capstone.ai_industry_summary (industry),
    CONSTRAINT fk_company_country
        FOREIGN KEY (country)
        REFERENCES capstone.country_ai_index (country)
);

