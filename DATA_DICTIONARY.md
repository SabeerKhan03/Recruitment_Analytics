# Data dictionary

All source rows describe a simulated 2025 recruitment portfolio. CSV headers map directly to MySQL columns. IDs are synthetic identifiers, not real candidate data.

## Source tables

| Table/file | Grain | Fields |
|---|---|---|
| `jobs` / `jobs.csv` | One row per requisition | `job_id` primary key; `job_title`; `department`; `posted_date`; `closing_date`; `target_headcount` simulated target; `job_status`. |
| `sources` / `sources.csv` | One row per acquisition source | `source_id` primary key; `source_name` unique display name. |
| `applications` / `applications.csv` | One row per application | `application_id` primary key; `job_id` and `source_id` foreign keys; `application_date`; `candidate_experience_years` simulated years; `ai_screening_score` simulated integer score from 0 to 100. |
| `stage_events` / `stage_events.csv` | One row per recorded application stage event | `event_id` primary key; `application_id` foreign key; `stage_name`; `stage_status`; `event_date`. An application can have multiple stage rows. |

Canonical stage order: Screening, Phone Interview, Technical Interview, Final Interview, Offer, Hired. A status describes that event; accepted offers are stage events where `stage_name='Offer'` and `stage_status='Accepted'`.

## Derived outputs

| File | Grain | Contents |
|---|---|---|
| `outputs/application_analysis.csv` | One row per application | Source attributes plus job title, department, target, offer/accept/hire flags, earliest hire date, time-to-hire, score band and numeric `score_band_sort` (1–5) for correct visual ordering. |
| `outputs/kpi_summary.csv` | One row per run | Application, offer, acceptance and hire totals/rates; average time-to-hire. |
| `outputs/funnel_summary.csv` | One row per canonical stage | Distinct applications reaching the stage and conversion from the prior stage. Not filter-aware in Power BI when imported as a static summary. |
| `outputs/source_performance.csv` | One row per source | Applications, offers, hires, hire rate and average time-to-hire. |
| `outputs/job_performance.csv` | One row per job | Applications, hires and simulated target gap. |
| `outputs/monthly_trend.csv` | One row per application month | Application and hire counts by month. |
| `outputs/score_band_outcomes.csv` | One row per screening score band | Application and hire totals and observed hire rate. Descriptive synthetic association only. |
| `outputs/data_quality_checks.csv` | One row per check | Row counts and counts of nulls, duplicate keys, invalid references, invalid dates, invalid score values and unknown stages. Error counts are expected to be zero. |
