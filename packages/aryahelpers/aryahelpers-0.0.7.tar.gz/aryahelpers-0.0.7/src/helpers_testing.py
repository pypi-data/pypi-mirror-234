"""arya-helpers testing script"""
# -*- coding: utf-8 -*-
# @author Ratnadip Adhikari

# execute the script
# exec(open("./arya-helpers/Codes/src/helpers_testing.py").read())

import sys, os, json
import pandas as pd
from functools import reduce
from importlib import reload, import_module
from IPython import get_ipython
# get_ipython().magic('reset -f')
import warnings
warnings.filterwarnings('ignore') ## Ignore warnings
os.system('clear') # print("\033c", end='')  ## clear screen
# globals().clear(); locals().clear() ## for resetting python interpreter memory
# +++++++++++++++++
# Boilerplate code for resolving relative imports
BASE_PATH = os.path.abspath("./arya-helpers/Codes/src")
extendPaths = [p for p in (os.path.dirname(BASE_PATH), BASE_PATH) if p not in sys.path]
sys.path = extendPaths + sys.path
# +++++++++++++++++
from aryahelpers.config import *
from aryahelpers.aryatestbed import testbed
from aryahelpers.utils import genericutils, mysqlutils, textclean
from aryautils.storageutils import MySQLManager
reload(testbed)
reload(sys.modules['aryahelpers.utils.genericutils'])
reload(sys.modules['aryahelpers.utils.mysqlutils'])
reload(sys.modules['aryahelpers.utils.textclean'])
from aryahelpers.utils.genericutils import *
from aryahelpers.utils.mysqlutils import MySQLHelpers
from aryahelpers.utils.textclean import PreprocessText
from aryahelpers.aryatestbed.testbed import CreateQATestbed
# ==================================

# ==================================
if False:
    # =================
    # QA job MySql operations
    MySQLHelpers.qa_job_mysql_operations(job_id=373387, query_seq=3, copy_info=False, to_print=True)
    # -*--*--*--*--*-
    # MySql table queries
    query_strs = [
        "SELECT COUNT(*) FROM custom_toprocess_candidates;",
        "SELECT COUNT(DISTINCT job_id) FROM custom_toprocess_candidates;",
        "SELECT COUNT(*) FROM custom_toprocess_analyzed_info;",
        "SELECT COUNT(DISTINCT jobId) FROM custom_toprocess_analyzed_info;"
    ]
    MySQLManager.execute_query(query_strs[0], (), **CONFIG['database']['candidate_reservoir'])
    # -*--*--*--*--*-
    query_strs = [
        "TRUNCATE TABLE custom_toprocess_candidates;",
        "DROP TABLE custom_toprocess_candidates;",
        "TRUNCATE TABLE custom_toprocess_analyzed_info;",
        "DROP TABLE custom_toprocess_analyzed_info;"
    ]
    MySQLHelpers.mysql_query_execute(query_strs[0], (), **CONFIG['database']['candidate_reservoir'])
    # -*--*--*--*--*-
    query_str = "SELECT DISTINCT(job_id) FROM custom_toprocess_candidates;"
    job_ids = MySQLManager.execute_query(query_str, (), **CONFIG['database']['candidate_reservoir'])
    job_ids = sorted(list(set([d['job_id'] for d in job_ids])), reverse=True)
    
    # =================
    # Determine sourced jobs
    filePath = "./arya-helpers/Codes/src/aryahelpers/data"
    testbed_jobs = import_file(os.path.join(filePath, "QA_testbed_jobs.json"))
    updated_jobs = {}
    for jid, source_details in testbed_jobs.items():
        query_str = "SELECT COUNT(*) FROM toprocess_candidates WHERE job_id={};".format(jid)
        query_res = MySQLManager.execute_query(query_str, (), **CONFIG['database']['candidate_reservoir'])
        source_count = query_res[0]["COUNT(*)"]
        jtr_candidates = MySQLHelpers.get_TopN_JTR(jid, 'database')
        if source_count and len(jtr_candidates) and len(source_details) == 3:
            updated_jobs.update({jid: source_details[:1] + [source_count, "Sourced"]})
        else:
            updated_jobs.update({jid: source_details[:1] + [source_count]})
    # -*--*--*--*--*-
    # Save updated sourced job details
    save_files(updated_jobs, filePath, 'QA_testbed_jobs', '.json', indent=4)
    
    # =================
    # Call `MySQLHelpers.transact_cands_from_tbl`
    params = {
        "from_table": 'custom_toprocess_analyzed_info',
        "db_key": 'database',
        "db_name": 'candidate_reservoir',
        "transact_type": 'extract',
        "to_table": None,
        "select_cols": None,
        "to_truncate": False,
        "copy_info": [],
        "where_clause": 'CandidateScore >= 2',
        "save_path": False,
        "file_name": 'extracted_info',
        "save_file_type": 'p_zip',
        "file_name_suffix": '',
        "indent": 4,
        "default": str
    }
    extractCands, _ = MySQLHelpers.transact_cands_from_tbl(**params)
    # -*--*--*--*--*-
    # Load saved table data
    data_path = os.path.join(CUSTOM_SAVE_PATH, 'extracted_testbed', 'custom_analyzed_info.zip')
    contds_info = import_file(data_path)
# ==================================

if __name__ == "__main__":
    print('python version:', sys.version) 
    print('cwd:', os.getcwd())
