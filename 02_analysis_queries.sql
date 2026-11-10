USE recruitment_analytics;
-- 1. Table row counts
SELECT 'jobs' table_name,COUNT(*) row_count FROM jobs UNION ALL SELECT 'sources',COUNT(*) FROM sources UNION ALL SELECT 'applications',COUNT(*) FROM applications UNION ALL SELECT 'stage_events',COUNT(*) FROM stage_events;
-- 2. Applicants by role
SELECT j.job_title,COUNT(a.application_id) applicants FROM jobs j LEFT JOIN applications a USING(job_id) GROUP BY j.job_id,j.job_title ORDER BY applicants DESC;
-- 3. Applications by source
SELECT s.source_name,COUNT(*) applications FROM applications a JOIN sources s USING(source_id) GROUP BY s.source_id,s.source_name ORDER BY applications DESC;
-- 4. Hires by source
SELECT s.source_name,COUNT(DISTINCT e.application_id) hires FROM stage_events e JOIN applications a USING(application_id) JOIN sources s USING(source_id) WHERE e.stage_name='Hired' GROUP BY s.source_id,s.source_name ORDER BY hires DESC;
-- 5. Funnel counts
SELECT stage_name,COUNT(DISTINCT application_id) candidates_reached FROM stage_events GROUP BY stage_name ORDER BY FIELD(stage_name,'Screening','Phone Interview','Technical Interview','Final Interview','Offer','Hired');
-- 6. Funnel conversion from previous stage
WITH x AS (SELECT stage_name,COUNT(DISTINCT application_id) reached FROM stage_events GROUP BY stage_name) SELECT stage_name,reached,ROUND(100*reached/NULLIF(LAG(reached) OVER(ORDER BY FIELD(stage_name,'Screening','Phone Interview','Technical Interview','Final Interview','Offer','Hired')),0),2) conversion_pct FROM x ORDER BY FIELD(stage_name,'Screening','Phone Interview','Technical Interview','Final Interview','Offer','Hired');
-- 7. Offer acceptance
SELECT COUNT(*) offers, SUM(stage_status='Accepted') accepted,ROUND(100*SUM(stage_status='Accepted')/COUNT(*),2) acceptance_pct FROM stage_events WHERE stage_name='Offer';
-- 8. Overall time-to-hire
SELECT COUNT(*) hires,ROUND(AVG(DATEDIFF(e.event_date,a.application_date)),1) avg_time_to_hire_days FROM stage_events e JOIN applications a USING(application_id) WHERE e.stage_name='Hired';
-- 9. Time-to-hire by source
SELECT s.source_name,COUNT(*) hires,ROUND(AVG(DATEDIFF(e.event_date,a.application_date)),1) avg_days FROM stage_events e JOIN applications a USING(application_id) JOIN sources s USING(source_id) WHERE e.stage_name='Hired' GROUP BY s.source_name ORDER BY avg_days;
-- 10. Monthly applications
SELECT DATE_FORMAT(application_date,'%Y-%m') month,COUNT(*) applications FROM applications GROUP BY month ORDER BY month;
-- 11. Score band vs hired outcome
WITH x AS (SELECT a.application_id,a.ai_screening_score,MAX(e.stage_name='Hired') hired FROM applications a LEFT JOIN stage_events e USING(application_id) GROUP BY a.application_id,a.ai_screening_score) SELECT CASE WHEN ai_screening_score<40 THEN '0-39' WHEN ai_screening_score<60 THEN '40-59' WHEN ai_screening_score<75 THEN '60-74' WHEN ai_screening_score<90 THEN '75-89' ELSE '90-100' END score_band,COUNT(*) applications,SUM(hired) hires,ROUND(100*SUM(hired)/COUNT(*),2) hire_rate_pct FROM x GROUP BY score_band ORDER BY MIN(ai_screening_score);
-- 12. High-score screening rejects for exception review
SELECT a.application_id,a.ai_screening_score,j.job_title,s.source_name FROM applications a JOIN stage_events e USING(application_id) JOIN jobs j USING(job_id) JOIN sources s USING(source_id) WHERE e.stage_name='Screening' AND e.stage_status='Rejected' AND a.ai_screening_score>=80 ORDER BY a.ai_screening_score DESC;
-- 13. Low-score hires for exception review
SELECT a.application_id,a.ai_screening_score,j.job_title,s.source_name FROM applications a JOIN stage_events e USING(application_id) JOIN jobs j USING(job_id) JOIN sources s USING(source_id) WHERE e.stage_name='Hired' AND a.ai_screening_score<50 ORDER BY a.ai_screening_score;
-- 14. Hires vs target
SELECT j.job_title,j.target_headcount,COUNT(DISTINCT e.application_id) hires,j.target_headcount-COUNT(DISTINCT e.application_id) target_gap FROM jobs j LEFT JOIN applications a USING(job_id) LEFT JOIN stage_events e ON a.application_id=e.application_id AND e.stage_name='Hired' GROUP BY j.job_id,j.job_title,j.target_headcount ORDER BY target_gap DESC;
-- 15. Data-quality: apps without screening (expected 0)
SELECT COUNT(*) missing_screening FROM applications a LEFT JOIN stage_events e ON a.application_id=e.application_id AND e.stage_name='Screening' WHERE e.event_id IS NULL;
