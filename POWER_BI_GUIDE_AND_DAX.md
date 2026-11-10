# Power BI model and report build guide

## Data import and model

Run `py .\python\run_analysis.py`, then import `outputs/application_analysis.csv`. This flat table is at one row per application and is the recommended model for all four pages. Set `application_date` and `hire_date` to Date, `ai_screening_score`, `score_band_sort`, `offered`, `offer_accepted` and `hired` to Whole number. Format rates as percentages and time-to-hire as days. In Power BI select `score_band`, then **Column tools → Sort by column → score_band_sort**.

Do not import both the flattened table and the source tables into the same report model unless you intentionally manage duplicate measures. For a normalized alternative, load the four raw CSVs and create one-to-many, single-direction relationships: `jobs[job_id]` to `applications[job_id]`, `sources[source_id]` to `applications[source_id]`, and `applications[application_id]` to `stage_events[application_id]`.

## DAX measures (flat application table)

```DAX
Applications = DISTINCTCOUNT(application_analysis[application_id])
Offers Extended = SUM(application_analysis[offered])
Offers Accepted = SUM(application_analysis[offer_accepted])
Hires = SUM(application_analysis[hired])
Offer Acceptance Rate = DIVIDE([Offers Accepted], [Offers Extended])
Overall Hire Rate = DIVIDE([Hires], [Applications])
Average Time to Hire (Days) =
    CALCULATE(
        AVERAGE(application_analysis[time_to_hire_days]),
        application_analysis[hired] = 1
    )
Median Time to Hire (Days) =
    CALCULATE(
        MEDIAN(application_analysis[time_to_hire_days]),
        application_analysis[hired] = 1
    )
Average Screening Score = AVERAGE(application_analysis[ai_screening_score])
```

To display stage reach and conversion, import `outputs/funnel_summary.csv` as a separate disconnected visual table. It contains precomputed reach and previous-stage conversion; application slicers will not filter this summary. For interactive funnel slicers, use the normalized event table and explicit stage-aware measures, or create a Power Query model tailored to stage progression. Do not imply slicer interaction that the static summary does not support.

## Suggested pages

1. **Executive Overview:** cards for applications, hires, offer acceptance and average time-to-hire; monthly application trend; source hires; role/department demand. Note that the time series is 2025 only.
2. **Recruitment Funnel:** candidate reach by canonical stage and conversion from previous stage, with clear definitions and a note that the funnel table is static unless modeled from events.
3. **Source & Hiring Efficiency:** applications, hires, hire rate, offer acceptance and average time-to-hire by source. Display sample sizes alongside rates.
4. **AI Screening Outcomes:** score-band application counts and observed hire rate, plus high-score screening rejections and low-score hires for human review. Label these as simulated outcomes; never call them accuracy or fairness.

Use a 16:9 canvas, restrained consistent colors, descriptive titles, useful units, aligned cards and slicers for source, department and role. Add the synthetic-data notice to every page or as a persistent report banner.

## Validation before sharing

Reconcile total applications, offers and hires to the Python KPI output. Confirm the offer acceptance denominator is applications with an Offer event, and that one application contributes at most once to each flat-table count. Check date and percentage formatting, filter behavior, empty categories and score band order. The `.pbix` must be saved and validated in Power BI Desktop; a PBIX is not supplied because Desktop authoring is unavailable in this environment.
