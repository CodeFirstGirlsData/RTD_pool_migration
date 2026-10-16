SELECT * FROM `rtd_data.RTD_TALENT_POOL` t1
LEFT JOIN `RTD_Pool_Import.rtd_import_BQ` t2 ON cast(t1.contact_id AS INT) = t2.Contact_Id AND t1.course_type = t2.Course_Type
WHERE t2.Contact_Id IS NULL AND t1.STATUS != 'FAIL'