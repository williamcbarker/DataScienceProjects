# Database Schema Design

This project uses a simple PostgreSQL design with **one table per CSV file**.

That is okay for this capstone because the project uses multiple source files instead of one large source file that needs to be split into many normalized tables. The goal is to load the data cleanly, identify relationships between files, and use SQL joins during analysis.

## Pipeline

```text
CSV files in repo
    -> Airflow loads CSVs
    -> PostgreSQL raw tables
    -> DBeaver SQL queries
    -> dashboard / presentation
```

## Tables

| CSV | PostgreSQL table | Grain |
| --- | --- | --- |
| `ai_productivity_features1.csv` | `capstone.ai_productivity_features` | one row per employee |
| `ai_productivity_targets1.csv` | `capstone.ai_productivity_targets` | one row per employee |
| `ai_dev_productivity.csv` | `capstone.ai_dev_productivity` | one row per coding session |
| `ai_worker_burnout_attrition_2026.csv` | `capstone.ai_worker_burnout_attrition` | one row per employee survey |
| `ai_industry_summary4.csv` | `capstone.ai_industry_summary` | one row per industry |
| `country_ai_index4.csv` | `capstone.country_ai_index` | one row per country |
| `ai_company_adoption4.csv` | `capstone.ai_company_adoption` | one row per company survey response |

## Relationships

```text
capstone.ai_productivity_features
    one-to-one with capstone.ai_productivity_targets
    using employee_id

capstone.ai_company_adoption
    many-to-one with capstone.ai_industry_summary
    using industry

capstone.ai_company_adoption
    many-to-one with capstone.country_ai_index
    using country
```

The other two datasets, `ai_dev_productivity.csv` and `ai_worker_burnout_attrition_2026.csv`, can remain standalone tables. They still support your project questions, but they do not need forced joins unless you later find a reliable shared key.


## Load Order

Because a few tables use foreign keys, load the CSV files in this order:

1. `ai_productivity_features1.csv`
2. `ai_productivity_targets1.csv`
3. `ai_industry_summary4.csv`
4. `country_ai_index4.csv`
5. `ai_company_adoption4.csv`
6. `ai_worker_burnout_attrition_2026.csv`
7. `ai_dev_productivity.csv`
