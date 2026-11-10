"""Repeatable assertions for the bundled sample and derived measures."""
from pathlib import Path
import subprocess
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(ROOT / "python" / "run_analysis.py")], cwd=ROOT, check=True)
quality = pd.read_csv(ROOT / "outputs" / "data_quality_checks.csv", index_col=0).value
assert [quality[k] for k in ("jobs_rows", "sources_rows", "applications_rows", "stage_events_rows")] == [10, 6, 5000, 13493]
assert (quality.drop(["jobs_rows", "sources_rows", "applications_rows", "stage_events_rows"]) == 0).all()
analysis = pd.read_csv(ROOT / "outputs" / "application_analysis.csv")
kpi = pd.read_csv(ROOT / "outputs" / "kpi_summary.csv").iloc[0]
assert len(analysis) == analysis.application_id.nunique() == 5000
assert set(analysis.score_band_sort.unique()) == {1, 2, 3, 4, 5}
assert (int(analysis.offered.sum()), int(analysis.offer_accepted.sum()), int(analysis.hired.sum())) == (801, 637, 637)
assert round(kpi.offer_acceptance_rate_pct, 2) == 79.53
assert round(kpi.overall_hire_rate_pct, 2) == 12.74
assert round(kpi.avg_time_to_hire_days, 1) == 26.7
assert pd.read_csv(ROOT / "outputs" / "funnel_summary.csv").candidates_reached.tolist() == [5000, 3611, 2181, 1263, 801, 637]
print("PASS: table row counts, null/key/duplicate checks, application grain, KPIs and funnel totals")
