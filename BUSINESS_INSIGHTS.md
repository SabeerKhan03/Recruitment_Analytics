# Business insights and actions

## Observed in the bundled sample

- The 5,000 application records produced 801 offers and 637 hires. Offer acceptance is 79.53% (637/801); hires are 12.74% of applications. These are synthetic sample results, not external benchmarks.
- Stage reach is 5,000 at Screening, 3,611 at Phone Interview, 2,181 at Technical Interview, 1,263 at Final Interview, 801 at Offer and 637 at Hired. The lowest transition rate is Technical Interview to Final Interview (57.91% advance); the largest count reduction is 1,389 between Screening and Phone Interview. These event statuses are generated data.
- LinkedIn has the most applications (1,401) and hires (192), with a 13.70% hire rate. Campus Hiring has the fewest applications (340) and the lowest observed hire rate (10.29%). Source hire rates range from 10.29% to 13.70%; small differences in this simulated data should not be read as causal source quality.
- Average time-to-hire is 26.7 calendar days overall, with source means from 26.0 days (Company Website) to 27.6 days (Naukri). This narrow range gives no strong basis for major source-specific process changes.
- The score bands show increasing simulated observed hire rates: 0.00% for 0–39 (50 applications), 3.78% for 40–59 (952), 8.78% for 60–74 (2,038), 18.40% for 75–89 (1,565) and 33.92% for 90–100 (395). Because the simulation links scores and outcomes, this pattern cannot validate a real AI screening tool.
- Actual hires exceed the small simulated targets for each role, so current target gaps are negative. For example, Junior Data Analyst has 126 hires against a target of 4; Software Engineer has 116 against 8. Treat the target field as a demonstration input, not a staffing plan.

## Recommended actions for a real deployment

1. Review the Screening-to-Phone Interview transition with recruiters: establish consistent criteria, sample rejected applications and check whether the stage definitions reflect actual practice.
2. Compare acquisition channels only after collecting costs, candidate quality measures, role mix and enough real observations. The current volume and rate differences are descriptive, not causal evidence.
3. Rebuild hiring targets from approved workforce plans and requisition-level headcount before using target-gap visuals for operational decisions.
4. Validate time-to-hire definitions with HR stakeholders and collect timestamps for offer approval, candidate response and recruiter work intervals if the goal is to locate delays.
5. Before any real AI-assisted screening, validate the model on representative held-out data, define human review and appeal processes, and assess outcomes across legally appropriate groups. The supplied data cannot support those conclusions.

All figures above are derived from the bundled CSVs by `python/run_analysis.py` and are reproduced by `python/test_project.py`.
