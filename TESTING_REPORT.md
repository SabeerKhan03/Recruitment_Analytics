# Testing report

Run date: 2026-11-10

## Executed checks

- `python python/run_analysis.py` — **PASS**. Generated all analysis outputs from the bundled CSVs.
- `python python/test_project.py` — **PASS**. Asserted table row counts, zero missing/duplicate/invalid-key/date/range/stage checks, one row per application, KPI totals, rates and funnel totals.
- `python -m compileall -q python` — **PASS**. Python files compile.
- SQL inventory — **PASS**. The analytical script contains 15 numbered queries.

## Validation evidence

- Source rows: 10 jobs, 6 sources, 5,000 applications and 13,493 stage events.
- Quality counters: zero nulls, duplicate IDs, invalid foreign keys, orphan events, events before application date, out-of-range scores, negative experience, invalid job dates or unknown stage names.
- KPI assertions: 801 offers, 637 accepted offers, 637 hires, 79.53% offer acceptance, 12.74% overall hire rate and 26.7 average calendar days to hire.
- Stage reach assertions: 5,000 Screening; 3,611 Phone Interview; 2,181 Technical Interview; 1,263 Final Interview; 801 Offer; 637 Hired.

## Not validated in this environment

- MySQL database integration: `mysqladmin ping` could not connect to `localhost:3306`; no running MySQL server was available to execute the schema, loader or analytical queries against. Install/start MySQL 8 and provide local credentials to run those setup steps.
- Power BI: Power BI Desktop is not installed/available, so no `.pbix` could be created or opened for report validation. The report design, model guidance and DAX measures are included in `power_bi/POWER_BI_GUIDE_AND_DAX.md`.
- Streamlit UI: the optional dashboard was not launched. Dashboard dependencies are declared in `requirements.txt` and can be installed on Windows.

The SQL statements were reviewed for intended MySQL 8 syntax but not executed against a server. Do not interpret that review as database integration testing.
