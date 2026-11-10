# Recruitment Operations & AI Screening Analytics

A reproducible portfolio project using Python, Pandas, NumPy, MySQL 8.0, SQL and Power BI to explore recruitment demand, source performance, funnel conversion, offer acceptance, hiring speed and simulated AI screening outcomes.

> **Synthetic data:** all candidate, score and hiring records are simulated. Score and outcomes are related by the simulation rules; they do not establish real-world screening accuracy, predictive validity, causality or fairness. No protected-group attributes are available, so fairness cannot be assessed. Exception lists are examples for human review only.

## Contents

- `data/`: source CSVs for jobs, sources, applications and stage events.
- `sql/01_create_schema.sql`: MySQL 8 schema, keys and relationships.
- `sql/02_analysis_queries.sql`: 15 analytical and quality queries.
- `python/load_to_mysql.py`: preflight validation and transactional database reload.
- `python/run_analysis.py`: data checks, derived analysis and Power BI-ready outputs.
- `python/test_project.py`: repeatable checks of row counts, KPIs and funnel totals.
- `python/dashboard_app.py`: optional Streamlit dashboard.
- `power_bi/POWER_BI_GUIDE_AND_DAX.md`: model, measures and four-page report guide.
- `DATA_DICTIONARY.md`: source and derived field definitions.
- `BUSINESS_INSIGHTS.md`: sample readout and practical recommendations.
- `TESTING_REPORT.md`: executed validation and integration limitations.
- `outputs/`: generated tables from the bundled dataset.

## Windows setup

1. Install Python 3.10+ and MySQL Server 8.0, then ensure the MySQL server is running.
2. In PowerShell from the project folder, install packages: `py -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and enter your MySQL connection settings. `.env` is excluded from Git.
4. Create the schema in Workbench or run `Get-Content .\sql\01_create_schema.sql | mysql -u root -p`.
5. Load the CSVs: `py .\python\load_to_mysql.py`. The loader validates nulls and foreign-key references before deleting rows. It inserts all table data in one transaction and rolls back on insertion failure; it never drops tables.
6. Generate outputs: `py .\python\run_analysis.py`.
7. Run reproducibility checks: `py .\python\test_project.py`.
8. Optional app: `py -m streamlit run .\python\dashboard_app.py` (requires Plotly).
9. Build the four-page Power BI report using the guide. A `.pbix` is not included because Power BI Desktop authoring is unavailable in this environment.

## KPI definitions

- Applications: distinct application IDs.
- Offer acceptance: applications with an accepted Offer event divided by applications with any Offer event.
- Hires: applications with a Hired event.
- Time-to-hire: calendar days from application date to earliest Hired event date, not recruiter work time.
- Funnel reach: unique applications recorded at each canonical stage; conversion is relative to the prior stage.
- Score-band outcomes: observed outcomes by simulated score band, not model accuracy.

## Bundled sample readout

The bundled synthetic data contains 5,000 applications, 801 offers, 637 accepted offers and hires, 79.53% offer acceptance, 12.74% hires per application and 26.7 average calendar days to hire. Funnel reach is 5,000 Screening, 3,611 Phone Interview, 2,181 Technical Interview, 1,263 Final Interview, 801 Offer and 637 Hired. These describe only this simulated 2025 sample.

## Scope and limitations

Hiring targets and AI screening scores are simulated. The project has no real ATS integration, production credentials, demographic analysis or validated hiring model. The Python analysis and local tests are executable here; MySQL reload requires a separately running MySQL 8 server and credentials. Power BI Desktop is needed to author and validate the `.pbix` report.
