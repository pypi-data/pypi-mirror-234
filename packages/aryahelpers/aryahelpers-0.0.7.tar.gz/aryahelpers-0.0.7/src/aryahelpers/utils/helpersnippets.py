# -*- coding: utf-8 -*-

# ================================================
# Helper codes snippets -- Leoforce
# ================================================
import sys, os, json
from importlib import reload, import_module
from aryautils.storageutils import *
from Candidate_Explanation_V2.Codes import *
# from aryautils import MySQLManager
from IPython.core.display import display

# Save 'requirements.txt'
"subprocess.run('pipreqs --force .')"
"display('INFO: Successfully saved requirements file in .\\requirements.txt')"
"$ `sort-requirements requirements.txt`"

# Checking sourcing flow status for a job
"call `queuing`.`sourcingflowstatus`(<job_id>);"  # in queuing db
"call `queuing`.`jobworkflowstatus`(<job_id>);"
"MySQLManager.call_proc('sourcingflowstatus', (<job_id>, ), **CONFIG['database']['queuing'])"
"MySQLManager.call_proc('jobworkflowstatus', (<job_id>, ), **CONFIG['database']['queuing'])"

# ==================================
# sys.path setting for debugging aryacandidateanalyzer/intelcomposer etc.
extendPaths = [
    "/home/ratnadip",  # master path (cwd)
    "/home/ratnadip/aryacandidateanalyzer/src"  # ref path
]
cfilePath = os.path.dirname(os.path.abspath(__file__))
sys.path.remove(cfilePath)
sys.path = extendPaths + sys.path
# ==================================

# ==================================
# table info : `candidate_reservoir`.`toprocess_candidates`
table_cols = [
    'job_id', 'portal_id', 'portal_candidate_id', 'source_config_id', 'log_id',  'activation_id', 'org_id',
    'batch_id', 'name', 'title', 'resume_title', 'past_title', 'company', 'highest_degree', 'industry', 'skills',
    'link', 'source_name', 'email', 'phone', 'city', 'state', 'location', 'postal_code', 'total_experience',
    'last_updated_date', 'summary', 'recent_pay', 'user_did', 'search_string_type_id', 'saved_search_string',
    'feeder', 'last_activity', 'relocation', 'facebook_url', 'twitter_url', 'is_diverse', 'diversity_confidence',
    'predictive_skills', 'authorization', 'search_type', 'vault_name', 'html_experiences', 'html_educations',
    'serialized_experiences', 'serialized_educations', 'resume_content', 'is_analyzed', 'created_date',
    'updated_date', 'unauthorization', 'experience_range', 'serialized_salaries', 'serialized_skills',
    'career_levels', 'work_permit_documents', 'desired_job_titles', 'job_types', 'dilated_filter_id', 'occupations', 
    'filters', 'filters_matched_count', 'preferred_location'
]
# ==================================
# table info : `candidate_reservoir`.`toprocess_analyzed_candidate_details_info`
table_cols = [
    'jobId', 'portalId', 'portalGuid', 'batchGuid', 'MoversLabel', 'MoversProbability', 'CandidateRating',
    'CandidateScore', 'CandidateScoreReason', 'JobFunction', 'SICDescription', 'RoleLevelScore', 'OccupationScore',
    'SkillScore', 'IndustryScore', 'ExperienceScore', 'SuccessProfileScore', 'EducationScore', 'BehavioralScore',
    'CompanyScore', 'RecencyScore', 'ListExperiences', 'UpdatedDateTime', 'Intel', 'PersonalInfo', 'LTRScore',
    'Explanation'
]
# table info: `arya`.`analyzed_candidate_details`
table_cols = [
    'job_id', 'portal_id', 'portal_guid', 'serialized_diversity_info', 'explanation', 'MoversLabel',
    'MoversProbability', 'CandidateRating', 'CandidateScore', 'RoleLevelScore', 'OccupationScore',
    'SkillScore', 'IndustryScore', 'ExperienceScore', 'SuccessProfileScore', 'CandidateScoreReason',
    'JobFunction', 'SICDescription', 'UpdatedDateTime', 'EducationScore', 'BehavioralScore', 'CompanyScore',
    'ListExperiences', 'RecencyScore'
]
# ==================================
# table info : `arya`.`job`
table_cols = [
    'JobId', 'JobCode', 'JobTitle', 'JobDesc', 'VmsJobDesc', 'MustHaveSrchStr', 'SearchString', 'DepartmentId',
    'Organization', 'EntitySubTypeId', 'VmsReferenceType', 'JobCreatedDate', 'DivisionId', 'JobOwner', 'JobStartDate', 
    'JobEndDate', 'QualificationId', 'DomainId', 'Location', 'latitude', 'longitude', 'CategoryId', 'RequiredSkills',
    'Skills', 'Responsibilities', 'Certifications', 'Specialization', 'AllKeyWord_Search', 'TotalExpMin', 
    'TotalExpMax', 'RelevantExpMin', 'RelevantExpMax', 'NoOfPositions', 'PriorityLevel', 'JobStatusId', 'IsHot',
    'AllocatedTo', 'EmployeeType', 'CreatedById', 'CreatedDate', 'ModifiedById', 'ModifiedDate', 'IsActive',
    'PayRateFrom', 'PublishId', 'Comments', 'DesignationId', 'PayFrequencyId', 'JobGuid', 'StateId', 'Zipcode',
    'Company', 'BillRateFrom', 'Address', 'Instructions', 'PayRateTo', 'BillRateTo', 'BillRateToMin',
    'BillRateFromMin', 'BillFrequencyId', 'Country', 'OverTime', 'Reference', 'TravelAllowance', 'DrugTest', 'BGV',
    'SecurityClearance', 'EmailIdList', 'EmailSend', 'BillRateType', 'PayRateType', 'Exempted', 'jobtype',
    'jobposition', 'JobCategoryId', 'WorkStatus', 'ReportTo', 'VendorId', 'jobCatTaleo', 'recruiterTaleo',
    'clientTaleo', 'durationTaleo', 'payRangeTaleo', 'joburl', 'JobApplyUrl', 'Miles', 'JTsynonymes', 'IsVerified',
    'VerifiedDate', 'Industries', 'ATSCreatedDate', 'ATSModifiedDate', 'IsPullByUser', 'JobSource', 'HasAttachment',
    'ExcludeML', 'VaultName', 'LastUpdateTimeStamp', 'PrimaryContact', 'is_advanced_job', 'is_remote_job',
    'is_multilocation_job'
]
# ==================================
# table info : `arya`.`job_top_recommendations`
table_cols = [
    'recommendation_id', 'association_id', 'job_id', 'portal_id', 'portal_candidate_id', 'rank_num',
    'reshuffle_count', 'created_time', 'updated_time', 'recommendation_status_id', 'recommended_mode',
    'source_config_id', 'arya_candidate_id', 'is_valid'
]
# table info : `arya`.`job_recommendations_metadata`
table_cols = [
    'metadata_id', 'recommendation_id', 'candidate_id', 'downloaded_candidate_id', 'vault_candidate_id',
    'candidate_guid', 'candidate_rating', 'candidate_score', 'candidate_score_reason', 'viewed', 'is_published',
    'searchtype_id', 'saved_search_string', 'is_feeder', 'movers_label', 'movers_probability', 'notes',
    'rejected_reasons', 'months_of_experience', 'current_company', 'current_title', 'recent_pay', 'past_title',
    'sic_codes', 'desired_title', 'candidate_name', 'skills', 'highest_education_title', 'occupation',
    'profile_updated_date', 'profile_updated_date_time', 'is_relevant', 'relocation_status', 'is_diverse',
    'diversity_percentage', 'last_activity', 'last_activity_date_time', 'currency', 'past_company',
    'highest_education_institution', 'industry', 'city', 'state', 'country', 'zipcode', 'location',
    'authorized_countries', 'unauthorized_countries', 'created_time', 'updated_time', 'link', 'sourcename',
    'resume_title', 'experience_range', 'career_levels', 'work_permit_documents', 'job_types', 'log_id', 'filter_id'
]
# ==================================
