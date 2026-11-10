from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
STAGES = ["Screening", "Phone Interview", "Technical Interview", "Final Interview", "Offer", "Hired"]

jobs = pd.read_csv(DATA / "jobs.csv", parse_dates=["posted_date", "closing_date"])
sources = pd.read_csv(DATA / "sources.csv")
apps = pd.read_csv(DATA / "applications.csv", parse_dates=["application_date"])
events = pd.read_csv(DATA / "stage_events.csv", parse_dates=["event_date"])

checks = {
    "applications_rows": len(apps), "jobs_rows": len(jobs), "sources_rows": len(sources), "stage_events_rows": len(events),
    "duplicate_application_ids": int(apps.application_id.duplicated().sum()),
    "duplicate_job_ids": int(jobs.job_id.duplicated().sum()),
    "duplicate_source_ids": int(sources.source_id.duplicated().sum()),
    "duplicate_event_ids": int(events.event_id.duplicated().sum()),
    "missing_values": int(sum(x.isna().sum().sum() for x in (jobs, sources, apps, events))),
    "invalid_job_references": int((~apps.job_id.isin(jobs.job_id)).sum()),
    "invalid_source_references": int((~apps.source_id.isin(sources.source_id)).sum()),
    "orphan_stage_events": int((~events.application_id.isin(apps.application_id)).sum()),
    "events_before_application": int((events.merge(apps[["application_id", "application_date"]], on="application_id").eval("event_date < application_date")).sum()),
    "screening_score_out_of_range": int((~apps.ai_screening_score.between(0, 100)).sum()),
    "negative_experience": int((apps.candidate_experience_years < 0).sum()),
    "invalid_job_dates": int((jobs.closing_date < jobs.posted_date).sum()),
    "unknown_stage_names": int((~events.stage_name.isin(STAGES)).sum()),
}
pd.Series(checks, name="value").to_csv(OUT / "data_quality_checks.csv")
row_keys = {"applications_rows", "jobs_rows", "sources_rows", "stage_events_rows"}
if any(v > 0 for k, v in checks.items() if k not in row_keys) or any(checks[k] == 0 for k in row_keys):
    raise ValueError(f"Data validation failed; inspect outputs/data_quality_checks.csv: {checks}")

hire = events.loc[events.stage_name.eq("Hired")].groupby("application_id", as_index=False).event_date.min().rename(columns={"event_date": "hire_date"})
offers = events.loc[events.stage_name.eq("Offer")]
accepted = set(offers.loc[offers.stage_status.eq("Accepted"), "application_id"])
hired = set(hire.application_id)
analysis = apps.copy()
analysis["offered"] = analysis.application_id.isin(set(offers.application_id)).astype(int)
analysis["offer_accepted"] = analysis.application_id.isin(accepted).astype(int)
analysis["hired"] = analysis.application_id.isin(hired).astype(int)
analysis = analysis.merge(hire, on="application_id", how="left")
analysis["time_to_hire_days"] = (analysis.hire_date - analysis.application_date).dt.days
analysis = analysis.merge(jobs[["job_id", "job_title", "department", "target_headcount"]], on="job_id").merge(sources, on="source_id")

offers_n, accepted_n, hires_n = int(analysis.offered.sum()), int(analysis.offer_accepted.sum()), int(analysis.hired.sum())
kpi = pd.DataFrame([{
    "applications": len(analysis), "offers_extended": offers_n, "offers_accepted": accepted_n, "hires": hires_n,
    "offer_acceptance_rate_pct": round(100 * accepted_n / offers_n, 2) if offers_n else np.nan,
    "overall_hire_rate_pct": round(100 * hires_n / len(analysis), 2) if len(analysis) else np.nan,
    "avg_time_to_hire_days": round(analysis.loc[analysis.hired.eq(1), "time_to_hire_days"].mean(), 1),
}])
kpi.to_csv(OUT / "kpi_summary.csv", index=False)

source = analysis.groupby("source_name", as_index=False).agg(applications=("application_id", "count"), offers=("offered", "sum"), hires=("hired", "sum"), avg_time_to_hire_days=("time_to_hire_days", "mean"))
source["hire_rate_pct"] = (100 * source.hires / source.applications).round(2)
source["avg_time_to_hire_days"] = source.avg_time_to_hire_days.round(1)
source.to_csv(OUT / "source_performance.csv", index=False)
job = analysis.groupby(["job_title", "department", "target_headcount"], as_index=False).agg(applications=("application_id", "count"), hires=("hired", "sum"))
job["target_gap"] = job.target_headcount - job.hires
job.to_csv(OUT / "job_performance.csv", index=False)
monthly = analysis.assign(month=analysis.application_date.dt.to_period("M").astype(str)).groupby("month", as_index=False).agg(applications=("application_id", "count"), hires=("hired", "sum"))
monthly.to_csv(OUT / "monthly_trend.csv", index=False)
funnel = events.groupby("stage_name").application_id.nunique().reindex(STAGES, fill_value=0).rename("candidates_reached").reset_index()
funnel["conversion_from_previous_pct"] = (100 * funnel.candidates_reached / funnel.candidates_reached.shift(1)).round(2)
funnel.to_csv(OUT / "funnel_summary.csv", index=False)
analysis["score_band"] = pd.cut(analysis.ai_screening_score, bins=[-1, 39, 59, 74, 89, 100], labels=["0-39", "40-59", "60-74", "75-89", "90-100"])
analysis["score_band_sort"] = analysis.score_band.cat.codes + 1
analysis.to_csv(OUT / "application_analysis.csv", index=False)
score = analysis.groupby("score_band", observed=False).agg(applications=("application_id", "count"), hires=("hired", "sum")).reset_index()
score["observed_hire_rate_pct"] = (100 * score.hires / score.applications.replace(0, np.nan)).round(2)
score.to_csv(OUT / "score_band_outcomes.csv", index=False)
print(pd.Series(checks))
print("\nKPIs\n", kpi.to_string(index=False))
print("\nGenerated outputs in", OUT)
