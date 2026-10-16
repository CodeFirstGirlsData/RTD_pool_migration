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
INITCAP(Town___City) town_city, 
CASE
  WHEN work_study_status = 'Employed (Full-time)' THEN 'Employed (full time)'
  WHEN work_study_status = 'Employed (Part-time)' THEN 'Employed (part time)'
  ELSE work_study_status
END work_study_status,
eu_rtw eu_rtw_og, 
CASE 
  WHEN eu_rtw = 'Yes - I am an EU or EEA citizen' THEN TRUE
  ELSE FALSE
END eu_citizen,
CASE 
  WHEN eu_rtw LIKE 'Yes%' THEN TRUE 
  WHEN eu_rtw LIKE 'No, I require a sponsored visa to work in the EEA' THEN FALSE 
  ELSE NULL
END eu_rtw,
CASE
  WHEN eu_rtw = 'No -  I am a non-EU national with a work, family, student or graduate visa' THEN 'non-EU national with a work, family, student or graduate visa'
  WHEN eu_rtw = 'Yes, I have permanent residency/settled status' THEN 'permanent residency/settled status'
  WHEN eu_rtw = 'Yes, I am a British citizen and can live and work in EEA countries without restrictions' THEN 'British citizen in Ireland'
  WHEN eu_rtw = 'Yes - I have been granted refugee/asylum status by the EU' THEN 'granted refugee/asylum status by the EU'
  ELSE NULL
END eu_rtw_details, 
CASE 
  WHEN eu_rtw = 'No, I require a sponsored visa to work in the EEA' THEN TRUE
  WHEN eu_rtw LIKE 'Yes%' THEN FALSE
  ELSE NULL
END eu_requires_sponsorship,
hireflix,
ARRAY_TO_STRING(array[Nationality,Property_dual_nationality],", ") nationalities,
Dual_nationality_yes eu_holds_dual_nationality,
financial_checks_ consent_to_financial_check, 
CASE WHEN plagiarism = TRUE THEN TRUE ELSE FALSE END plagiarism_on_course,
SPLIT(Notice_period," ")[0] notice_period,
Specific_skills commercial_skills,
confirm_salary,
REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(salary_expectations,'-',' - '),'£85,000 - £95,000','Above £85,000'),'Above £95,000','Above £85,000'),'Above £85,000;Above £85,000','Above £85,000'),'£65,000 - £70,000','£65,000 - £75,000'),'Above £70,000', '£65,000 - £75,000'),'£65,000 - £75,000;£65,000 - £75,000','£65,000 - £75,000') salary_expectations, 
DATE(IC_session) ic_session,
latest_cv, 
cloud_infrastructure_training

from `data-hub-375915.RTD_Pool_Import.rtd_import`
WHERE Country not like 'United Kingdom%'