# Technical Report

## Project Overview

This project explores how workplace AI adoption relates to productivity, burnout, innovation, perceived job replacement risk, and business return-on-investment signals. The project uses multiple CSV datasets, a PostgreSQL database, an Airflow loading pipeline, exploratory analysis in Jupyter, machine learning models, and a Dash dashboard.

## Questions Asked

- How is AI tool usage related to worker productivity?
- Is AI usage associated with employee burnout or stress?
- Is there a useful balance between AI-assisted work and manual work?
- Which job roles feel most threatened by AI replacement?
- Which industries appear to benefit most from AI adoption?
- Is company AI adoption associated with ROI proxy metrics such as productivity change, revenue growth, cost reduction, and failure rate?
- Can machine learning predict productivity or identify worker segments?

## Datasets Used

Mehta, V. (n.d.). AI workplace productivity dataset [Data set]. Kaggle. Retrieved June 22, 2026, from https://www.kaggle.com/datasets/vishardmehta/ai-tool-usage-and-workplace-productivity-dataset
Abbas, N. (n.d.). AI worker burnout & attrition risk dataset [Data set]. Kaggle. Retrieved June 22, 2026, from https://www.kaggle.com/datasets/nudratabbas/ai-worker-burnout-and-attrition-risk-dataset
Soundankar, A. (n.d.). AI developer productivity dataset [Data set]. Kaggle. Retrieved June 22, 2026, from https://www.kaggle.com/datasets/atharvasoundankar/ai-developer-productivity-dataset
Thalla, M. K. (n.d.). Global AI adoption and workforce impact dataset [Data set]. Kaggle. Retrieved June 22, 2026, from https://www.kaggle.com/datasets/mohankrishnathalla/global-ai-adoption-and-workforce-impact-dataset

## Database Design

The PostgreSQL database uses a simple schema named `capstone`. Each CSV file maps to one database table.

Main relationships:

- `capstone.ai_productivity_features` has a one-to-one relationship with `capstone.ai_productivity_targets` using `employee_id`.
- `capstone.ai_company_adoption` has a many-to-one relationship with `capstone.ai_industry_summary` using `industry`.
- `capstone.ai_company_adoption` has a many-to-one relationship with `capstone.country_ai_index` using `country`.
- `capstone.ai_dev_productivity` and `capstone.ai_worker_burnout_attrition` remain standalone analysis tables.

## ETL Process

The ETL process loads the local CSV files into PostgreSQL using an Airflow DAG.

Pipeline flow:

```text
CSV files
    -> Airflow DAG
    -> PostgreSQL capstone schema
    -> DBeaver SQL validation
    -> Jupyter EDA / ML
    -> Dash dashboard
```

The Airflow DAG clears the seven database tables and reloads the CSVs in foreign-key-safe order:

1. `ai_productivity_features1.csv`
2. `ai_productivity_targets1.csv`
3. `ai_industry_summary4.csv`
4. `country_ai_index4.csv`
5. `ai_company_adoption4.csv`
6. `ai_worker_burnout_attrition_2026.csv`
7. `ai_dev_productivity.csv`

The DAG uses Docker environment variables for the PostgreSQL connection and loads rows with PostgreSQL `COPY`.

## Technologies Used

- GitHub for version control
- Python and Pandas for data analysis
- Jupyter notebooks for EDA and ML
- PostgreSQL for database storage
- DBeaver for database inspection and SQL testing
- Docker for running Airflow
- Airflow for ETL orchestration
- Scikit-learn for machine learning
- Dash and Plotly for the dashboard

## Exploratory Data Analysis

EDA was performed in `EDA.ipynb`. The notebook checks dataset shapes, data types, missing values, duplicates, possible primary keys, joins, correlations, grouped summaries, and visualizations.

Key EDA findings:

- AI tool usage had a moderate positive correlation with employee productivity score (`r = 0.498`).
- Manual work hours had a negative correlation with productivity score (`r = -0.440`).
- Burnout risk had a negative correlation with productivity score (`r = -0.392`).
- Work-life balance had a strong negative correlation with burnout risk (`r = -0.846`), suggesting burnout is more closely connected to balance than AI usage alone.
- Backend Engineers and Software Engineers reported the highest average perceived AI task replacement percentages.
- Technology had the highest average productivity change among industries, followed by Finance and Logistics.

## Machine Learning

Machine learning was performed in `ML.ipynb` using the joined employee productivity dataset.

Models used:

- Linear Regression to predict `productivity_score`
- Random Forest Regressor to predict `productivity_score`
- K-Means Clustering to group employees into behavior segments

Regression results:

| Model | MAE | RMSE | R-squared |
| --- | ---: | ---: | ---: |
| Linear Regression | 3.940 | 4.909 | 0.879 |
| Random Forest Regressor | 4.681 | 5.792 | 0.831 |

Linear Regression performed better than Random Forest on this dataset. This suggests the productivity score is largely explained by relatively linear relationships among the selected features.

K-Means produced four employee segments. The clearest contrast was between:

- a high-AI, high-automation, high-productivity segment; and
- a low-AI, high-manual-work, lower-productivity segment.

The dashboard uses `models/model_comparison.csv` and `models/cluster_summary.csv` as ML summary inputs.

## Dashboard

The dashboard is built with Dash in `app.py`. It uses tabs to organize the project findings:

- Overview
- Worker Productivity
- Company and Industry
- ML Segments

The dashboard includes KPI cards, productivity charts, burnout/job-role charts, industry benefit charts, machine learning model comparison, k-means cluster summaries, and an industry dropdown for exploring company adoption metrics.

## Conclusions

- AI usage appears associated with higher employee productivity, but the relationship should not be interpreted as direct causation.
- Burnout risk appears more strongly related to work-life balance and manual workload than to AI usage by itself.
- Company-level productivity change is positively associated with AI maturity, AI adoption rate, AI budget percentage, time saved, and innovation score.
- AI failure rate is negatively associated with productivity change.
- Technology and Finance appear to benefit most from AI adoption based on productivity change, innovation, and adoption metrics.
- Job replacement concern varies by role, with technical roles reporting some of the highest perceived task replacement percentages.
- Linear Regression was the strongest predictive model in this project, while K-Means provided useful worker segments for explanation and dashboarding.

