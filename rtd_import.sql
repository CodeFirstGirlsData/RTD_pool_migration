select 
SPLIT(name," ")[0] first_name, 
ARRAY_TO_STRING(ARRAY_SLICE(SPLIT(name," "),1,-1)," ") last_name,
email, 
phone, 
job_title, 
CASE 
  WHEN Course_Type = 'DEGREE' Then 'Degree'
  WHEN Course_Type = 'MLA' Then 'MLA' 
END course_type,
CASE
  WHEN Course_Type = 'DEGREE' Then Course_date 
END degree_cohort,
CASE
  WHEN Course_Type = 'MLA' Then Course_date 
END mla_cohort, 
CASE 
  WHEN Course_Type = 'DEGREE' Then Stream
END degree_stream, 
CASE 
  WHEN Course_Type = 'MLA' Then Stream
END mla_stream, 
masters_stream,
CASE
  WHEN VR_student_flag = 1 THEN TRUE
  ELSE FALSE
END vr_student,
CASE 
  WHEN Course_Type = 'DEGREE' Then INITCAP(Status)
END degree_outcome,
CASE 
  WHEN Course_Type = 'MLA' Then INITCAP(Status)
END mla_outcome,
CASE 
  WHEN rtd_opt_in = 'Yes' THEN TRUE
END rtd_opt_in,
Country country_of_residence,
REGION uk_region,
INITCAP(Town___City) town_city, 
CASE
  WHEN work_study_status = 'Employed (Full-time)' THEN 'Employed (full time)'
  WHEN work_study_status = 'Employed (Part-time)' THEN 'Employed (part time)'
  ELSE work_study_status
END work_study_status,
CASE 
  WHEN uk_rtw LIKE '%permanent settled%' THEN 'Other'
  WHEN uk_rtw LIKE '%British Citizen%' THEN 'British citizen'
  WHEN uk_rtw LIKE '%graduate%' THEN 'Graduate Visa'
  WHEN uk_rtw LIKE '%work or family visa%' THEN 'Other'
  WHEN uk_rtw LIKE '%refugee%' THEN 'Refugee or Humanitarian Protection'
END uk_rtw, 
CASE
    WHEN uk_rtw LIKE '%permanent settled%' THEN uk_rtw
    WHEN uk_rtw LIKE '%work or family visa%' THEN uk_rtw
END uk_rtw_other_reason,
hireflix,
ARRAY_TO_STRING(array[Nationality,Property_dual_nationality],", ") nationalities,
Dual_nationality_yes uk_holds_dual_nationality,
financial_checks_ consent_to_financial_check, 
CASE
  WHEN LENGTH_RESIDENCE_IN_UK LIKE ANY ('%since birth%','%10%') THEN TRUE
  ELSE FALSE
END uk_resident_10_years , 
CASE
  WHEN LENGTH_RESIDENCE_IN_UK LIKE ANY ('%since birth%','%10%','%5%') THEN TRUE
  ELSE FALSE
END uk_resident_5_years , 
CASE
  WHEN LENGTH_RESIDENCE_IN_UK LIKE ANY ('%since birth%','%10%','%5%','%3%') THEN TRUE
  ELSE FALSE
END uk_resident_3_years , 
CASE 
  WHEN TRAVELLED_OUTSIDE_UK_LAST_10_YEARS_CRITERIA IN ('Yes','No') THEN 'Unknown'
  ELSE REPLACE(REPLACE(TRAVELLED_OUTSIDE_UK_LAST_10_YEARS_CRITERIA,'Have not spent more than six months abroad within the last previous three years','Have not spent more than six months abroad overall within the last previous three years'),'Have not spent more than 28 days outside the United Kingdom within the last five years','Have not spent more than 28 days consecutively outside the United Kingdom within the last five years')
END
 uk_last_10_years_checks,
CASE WHEN plagiarism = TRUE THEN TRUE ELSE FALSE END plagiarism_on_course,
SPLIT(Notice_period," ")[0] notice_period,
Specific_skills commercial_skills,
confirm_salary,
REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(salary_expectations,'-',' - '),'£85,000 - £95,000','Above £85,000'),'Above £95,000','Above £85,000'),'Above £85,000;Above £85,000','Above £85,000'),'£65,000 - £70,000','£65,000 - £75,000'),'Above £70,000', '£65,000 - £75,000'),'£65,000 - £75,000;£65,000 - £75,000','£65,000 - £75,000') salary_expectations, 
DATE(IC_session) ic_session,
latest_cv, 
cloud_infrastructure_training

from `data-hub-375915.RTD_Pool_Import.rtd_import`
WHERE Country like 'United Kingdom%'