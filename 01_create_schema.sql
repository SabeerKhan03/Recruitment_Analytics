CREATE DATABASE IF NOT EXISTS recruitment_analytics;
USE recruitment_analytics;

CREATE TABLE IF NOT EXISTS jobs (job_id VARCHAR(10) PRIMARY KEY, job_title VARCHAR(100) NOT NULL, department VARCHAR(60) NOT NULL, posted_date DATE NOT NULL, closing_date DATE NOT NULL, target_headcount INT NOT NULL, job_status VARCHAR(20) NOT NULL);
CREATE TABLE IF NOT EXISTS sources (source_id VARCHAR(10) PRIMARY KEY, source_name VARCHAR(60) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS applications (application_id VARCHAR(12) PRIMARY KEY, job_id VARCHAR(10) NOT NULL, source_id VARCHAR(10) NOT NULL, application_date DATE NOT NULL, candidate_experience_years DECIMAL(4,1) NOT NULL, ai_screening_score TINYINT UNSIGNED NOT NULL, CONSTRAINT fk_app_job FOREIGN KEY(job_id) REFERENCES jobs(job_id), CONSTRAINT fk_app_source FOREIGN KEY(source_id) REFERENCES sources(source_id));
CREATE TABLE IF NOT EXISTS stage_events (event_id VARCHAR(12) PRIMARY KEY, application_id VARCHAR(12) NOT NULL, stage_name VARCHAR(30) NOT NULL, stage_status VARCHAR(20) NOT NULL, event_date DATE NOT NULL, CONSTRAINT fk_event_app FOREIGN KEY(application_id) REFERENCES applications(application_id));
