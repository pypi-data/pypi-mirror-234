"""Modules for generating QA testbed jobs"""
# -*- coding: utf-8 -*-
# @author Ratnadip Adhikari

# exec(open("./arya-helpers/Codes/src/aryahelpers/aryatestbed/testbed.py").read())
from __future__ import absolute_import
import sys, os, json, logging
import warnings
warnings.filterwarnings('ignore')
os.system('clear') # print("\033c", end='')
# +++++++++++++++++
BASE_PATH = os.path.abspath("./arya-helpers/Codes/src")
extendPaths = [p for p in (os.path.dirname(BASE_PATH), BASE_PATH) if p not in sys.path]
sys.path = extendPaths + sys.path
# +++++++++++++++++
from aryautils.storageutils import MySQLManager
from aryahelpers.config import CONFIG, CUSTOM_SAVE_PATH, ALL_FEATURES, CANDIDATE_TABLES
from joblib import Parallel, delayed
from aryahelpers.utils.textclean import PreprocessText
from aryahelpers.utils.genericutils import elapsedTime, save_files, merge_dicts, map_processing
from aryahelpers.utils.mysqlutils import MySQLHelpers
LOGGER = logging.getLogger(__name__)


class CreateQATestbed():
    """QA testbed creation class"""
    def __init__(self, job_ids=[]):
        self.testbed_jobs = []
        self.job_ids = job_ids
        self._ALL_FEATURES = set(k.lower() for k in ALL_FEATURES)
        self.toprocess_db_key, self.toprocess_db_name, self.toprocess_base_table, self.toprocess_jobid_key, \
            self.toprocess_guid_key = tuple(CANDIDATE_TABLES["toprocess"]["base"].values())
        self.expl_db_key, self.expl_db_name, self.expl_base_table, self.expl_jobid_key, \
            self.expl_guid_key, self.expl_key = tuple(CANDIDATE_TABLES["explanation"]["qa-reservoir"].values())
        self.toprocess_copy_table = CANDIDATE_TABLES["toprocess"]["copy"]["table"]
        self.expl_copy_table = CANDIDATE_TABLES["explanation"]["copy"]["table"]
        self.concise_info_keys = ['JobId', 'ClientCompany', 'JobTitle', 'SourceCount', 'PositiveCount', 'JTRCount']
        self.base_api = "http://192.168.38.99:1502/api/new?expl_type=facts"
    
    @staticmethod
    def _get_jtr_candidates(source_guids: set, jobid: int, db_key: str):
        """Get JTR candidates"""
        try:
            jtr_candidates = []
            base_query = "SELECT job_id, candidate_name, portal_candidate_id, recommendation_status_id, \
                CONVERT_TZ(jtr.updated_time,'+00:00','+05:30') AS updated_time FROM \
                    `arya`.`job_top_recommendations` jtr JOIN `arya`.`job_recommendations_metadata` jrm ON \
                        jtr.recommendation_id = jrm.recommendation_id WHERE job_id = "
            query_str = base_query + "{} ORDER BY candidate_score DESC;".format(jobid)
            query_res = MySQLManager.execute_query(query_str, (), **CONFIG[db_key]['arya'])
            for guid in source_guids:
                jtr_info = [d for d in query_res if d['portal_candidate_id'] == guid]
                jtr_info = sorted(jtr_info, key=lambda d: d['updated_time'], reverse=True)
                if jtr_info:
                    jtr_candidates.append(jtr_info[0])
        except Exception:
            jtr_candidates = []
        return jtr_candidates
    
    @staticmethod
    def _extract_arya_jobdetails(job_id: int):
        """Extract details for the given job_id"""
        arya_jobdetails = {}
        try:
            job_details = MySQLManager.call_proc('get_arya_job_params', (job_id, ),
                                                 **CONFIG['database']['arya'])[0][0]
            client_company, job_title, loc_info = job_details['ClientCompany'], job_details['JobTitle'], ''
            if job_details['Location']:
                loc_info += job_details['Location']
            if job_details['Country']:
                _prefix = ", " if job_details['Location'] else ""
                loc_info += _prefix + job_details['Country']
            arya_jobdetails = {
                "ClientCompany": client_company,
                "JobTitle": job_title,
                "Location": loc_info,
            }
        except Exception as error:
            LOGGER.error(error)
            LOGGER.error("Error in extracting Arya job details !!")
        return arya_jobdetails

    @staticmethod
    def _obtain_contd_details(db_key, db_name, tbl_name, jobid_key, guid_key, job_id=None):
        """Obtain existing job & candidate details from base/copy table"""
        wh_clause = "WHERE {}={}".format(jobid_key, job_id) if job_id else ""
        query_str = "SELECT {0}, {1} FROM {2} {3} GROUP BY {0}, {1};".format(jobid_key, guid_key, tbl_name, wh_clause)
        query_res = MySQLManager.execute_query(query_str, (), **CONFIG[db_key][db_name])
        found_jobids = {job_id} if job_id else set([d[jobid_key] for d in query_res])
        contd_details = {jid: {"source_count": sum([1 for d in query_res if d[jobid_key] == jid]),
                               "contd_guids": set([d[guid_key] for d in query_res if d[jobid_key] == jid])}
                         for jid in found_jobids}
        return contd_details
    
    def _filter_sourced_jobs(self, refresh_data=False):
        """Checks each job id for existence in `toprocess_candidates` table and returns the existing ones.
        Also, copies all candidates to the `copy_table` based on the param: `refresh_data`."""
        sourced_jobs, copy_info = {}, []
        db_key, db_name, jobid_key, guid_key = self.toprocess_db_key, self.toprocess_db_name, \
            self.toprocess_jobid_key, self.toprocess_guid_key
        base_table, copy_table = self.toprocess_base_table, self.toprocess_copy_table
        # Select already existing job_ids from 'copy_table'
        try:
            existing_jobs = self._obtain_contd_details(db_key, db_name, copy_table, jobid_key, guid_key)
        except Exception:
            existing_jobs = {}
        if not self.job_ids:
            [sourced_jobs.update({jid: merge_dicts((existing_jobs[jid], {
                "already_exists": True}))}) for jid in existing_jobs]
            return sourced_jobs
        # Now check each job for its existence in the 'toprocess_candidates' table
        for idx, jid in enumerate(self.job_ids):
            if jid in existing_jobs:
                sourced_jobs.update({jid: merge_dicts((existing_jobs[jid], {"already_exists": True}))})
            else:
                existing_basejob = self._obtain_contd_details(db_key, db_name, base_table, jobid_key, guid_key, jid)
                if existing_basejob:
                    sourced_jobs.update({jid: merge_dicts((existing_basejob[jid], {"already_exists": False}))})
            if refresh_data:
                copy_info.append({"job_id": str(jid)})
            elif not sourced_jobs.get(jid, {}).get("already_exists"):
                copy_info.append({"job_id": str(jid)})
        # Copy the requisite jobs to 'copy_table'
        if not copy_info:
            copy_info = False
        if refresh_data:
            MySQLHelpers.transact_cands_from_tbl(base_table, db_key, db_name, "delete", copy_table, None, False, copy_info)
        MySQLHelpers.transact_cands_from_tbl(base_table, db_key, db_name, "copy", copy_table, None, False, copy_info)
        return sourced_jobs

    def _get_available_factkeys(self, expl_dict: dict):
        """Get the available (non-null) facts keys for a given eplanation dict"""
        all_factkeys = []
        [all_factkeys.append(k) for k, v in expl_dict.items() if k.lower() != 'summary'
         and ({k, k.lower()} & self._ALL_FEATURES) and v.get("Facts", [])]
        return all_factkeys
    
    def _extract_explcopied_jobs(self, refresh_data=False):
        """Extract set of jobs for which analyzed info are already copied"""
        db_key, db_name, jobid_key = self.expl_db_key, self.expl_db_name, self.expl_jobid_key
        if refresh_data:
            return set()
        try:
            existing_jobids = MySQLManager.execute_query("SELECT {} FROM {};".format(
                jobid_key, self.expl_copy_table), (), **CONFIG[db_key][db_name])
            return set([j for _dict in existing_jobids for k, j in _dict.items()])
        except Exception:
            return set()
    
    def _extract_explanation_facts(self, source_guids: set, job_id: int):
        """Extract existing explanation facts for the given job_id"""
        analyzed_contds, existing_facts, passed_count = [], [], 0
        db_key, db_name, expl_table, jobid_key, guid_key, expl_key = self.expl_db_key, self.expl_db_name, \
            self.expl_base_table, self.expl_jobid_key, self.expl_guid_key, self.expl_key
        try:            
            query_str = "SELECT *, CONVERT_TZ(UpdatedDateTime,'+00:00','+05:30') \
                AS UpdatedDateTime FROM {0} WHERE {1}={2} AND CandidateScore > 0;".format(
                    expl_table, jobid_key, job_id)                
            query_res = MySQLManager.execute_query(query_str, (), **CONFIG[db_key][db_name])
            # Filter analyzed contds w.r.t. source_guids
            for guid in source_guids:
                analyzed_info = [d for d in query_res if d[guid_key] == guid]
                analyzed_info = sorted(analyzed_info, key=lambda d: d['UpdatedDateTime'], reverse=True)
                if analyzed_info:
                    analyzed_contds.append(analyzed_info[0])
            passed_count = len(analyzed_contds)
            for idx, expl in enumerate(analyzed_contds):
                expl_keys = self._get_available_factkeys(json.loads(expl[expl_key]))
                _expl_keys = set(expl_keys)
                if set(existing_facts) <= _expl_keys:
                    existing_facts = expl_keys
                if (_expl_keys == self._ALL_FEATURES) or (_expl_keys == ALL_FEATURES):
                    break
        except Exception as error:
            LOGGER.error(error)
            LOGGER.error("Error in extracting existing explanation facts !!")
        return analyzed_contds, existing_facts, passed_count
    
    def _multiprocess_details(self, parallelize: bool, db_key: str, sourced_jobmap: dict, job_ids: list):
        """Obtain required DB-intensive details through multiprocessing"""
        args_list_facts = [(sourced_jobmap[jid]["contd_guids"], jid) for jid in job_ids]
        args_list_jtr = [(sourced_jobmap[jid]["contd_guids"], jid, db_key) for jid in job_ids]
        # Extract details through multiprocessing
        if parallelize:
            res_facts = Parallel(n_jobs=-1)(delayed(self._extract_explanation_facts)(*args) for args in args_list_facts)
            res_jtr = Parallel(n_jobs=-1)(delayed(self._get_jtr_candidates)(*args) for args in args_list_jtr)
            res_jobdetails = Parallel(n_jobs=-1)(delayed(self._extract_arya_jobdetails)(jid) for jid in job_ids)
        else:
            res_facts = map_processing(self._extract_explanation_facts, args_list_facts, True)
            res_jtr = map_processing(self._get_jtr_candidates, args_list_jtr, True)
            res_jobdetails = map_processing(self._extract_arya_jobdetails, job_ids)
        # Create dict of the extracted details
        extracted_facts = {jid: res_facts[idx] for idx, jid in enumerate(job_ids)}
        extracted_jtr = {jid: len(res_jtr[idx]) for idx, jid in enumerate(job_ids)}
        extracted_jobdetails = {jid: res_jobdetails[idx] for idx, jid in enumerate(job_ids)}
        return extracted_facts, extracted_jtr, extracted_jobdetails
        
    def _summarize_testbed_jobs(self, concise_info=False):
        """Get a summarized (condensed) form of testbed job details"""
        if self.testbed_jobs and concise_info:
            self.testbed_jobs = sorted([tuple({k: v for k, v in d.items() if k in self.concise_info_keys}.values())
                                        for d in self.testbed_jobs], key=lambda x: x[0], reverse=True)
            self.testbed_jobs = {str(k[0]): k[1:] for k in self.testbed_jobs}
    
    @elapsedTime
    def cleanup_custom_tables(self, keep=False):
        """
        Delete undesirable jobs data from the custom table. The param `keep=False` refers deletion of
        the given jobs, whereas `keep=True` refers to keep the given jobs and delete all others.
        """
        not_str = 'NOT' if keep else ''
        db_key, db_name, job_ids = self.toprocess_db_key, self.toprocess_db_name, tuple(set(self.job_ids))
        cleanup_status = {"toprocess": False, "analyzed_info": False}
        for table in (self.toprocess_copy_table, self.expl_copy_table):
            jobid_key = self.toprocess_jobid_key if table == self.toprocess_copy_table else self.expl_jobid_key
            status_key = 'toprocess' if table == self.toprocess_copy_table else 'analyzed_info'
            query_str = "DELETE FROM {0} WHERE {1} {2} IN {3};".format(table, jobid_key, not_str, job_ids)
            query_str = PreprocessText().spaces_clean(query_str)
            cleanup_status[status_key] = MySQLHelpers.mysql_query_execute(query_str, (), **CONFIG[db_key][db_name])
        return cleanup_status
    
    @elapsedTime
    def extract_testbed_candidates(self, to_extract='both', **kwargs):
        """Extract all testbed candidates from custom toprocess & analyzed info tables as pickle zip files.
        
        Args:
            to_extract (str, optional): Type of candidates to extract: 'both' (default), 'toprocess' or 'analyzed'.
            save_path (bool, optional): The path to save extracted candidates. Defaults to ``False``.
            **kwargs (optional): Any other optional args for `save_files` and `MySQLHelpers.transact_cands_from_tbl`.
        
        Returns:
            List of extracted candidates.
        """
        exclude_kwargs = ['from_table', 'db_key', 'db_name', 'transact_type', 'to_table',
                          'copy_info', 'file_name', 'save_file_type']
        kwargs = {k: v for k, v in kwargs.items() if k not in exclude_kwargs}
        extracted_toprocess, extracted_analyzed = [], []
        if to_extract in ('toprocess', 'both'):
            extracted_toprocess, _ = MySQLHelpers.transact_cands_from_tbl(
                self.toprocess_copy_table, self.toprocess_db_key, self.toprocess_db_name, 'extract',
                copy_info=[], file_name='custom_toprocess', save_file_type='p_zip', **kwargs)
        if to_extract in ('analyzed', 'both'):
            extracted_analyzed, _ = MySQLHelpers.transact_cands_from_tbl(
                self.expl_copy_table, self.expl_db_key, self.expl_db_name, 'extract',
                copy_info=[], file_name='custom_analyzed_info', save_file_type='p_zip', **kwargs)
        return extracted_toprocess, extracted_analyzed
    
    @elapsedTime
    def create_testbed(self, refresh_data=False, concise_info=False, parallelize=True, save_path=False):
        """Main module for creating testbed jobs"""
        refresh_data = False if not self.job_ids else refresh_data
        sourced_jobs = self._filter_sourced_jobs(refresh_data)  # collect jobs which exist in toprocess table
        existing_jobids = self._extract_explcopied_jobs(refresh_data)
        job_ids = set(sourced_jobs) if self.job_ids else set(existing_jobids)
        sourced_jobs = {k: v for k, v in sourced_jobs.items() if k in job_ids}
        job_ids = sorted(list(job_ids), reverse=True)
        db_key, db_name, jobid_key, base_table, copy_table = self.expl_db_key, self.expl_db_name,\
            self.expl_jobid_key, self.expl_base_table, self.expl_copy_table
        facts_details, jtr_counts, arya_jobdetails = self._multiprocess_details(parallelize, db_key, sourced_jobs, job_ids)
        copy_info, analyzed_contds, jobs_record = [], [], []
        try:
            for jid in job_ids:
                contd_details, existing_facts, passed_count = facts_details[jid]
                if not existing_facts:
                    continue
                if jid not in existing_jobids:
                    copy_info.append({jobid_key: str(jid)})
                ccompany_job_title = [arya_jobdetails[jid].get(k, '') for k in ('ClientCompany', 'JobTitle')]
                if any(ccompany_job_title) and (ccompany_job_title in jobs_record):
                    continue  # Record only unique jobs w.r.t. -- ClientCompany-JobTitle
                expl_jobdetails = {
                    "SourceCount": sourced_jobs[jid]['source_count'],
                    "PositiveCount": passed_count,
                    "JTRCount": jtr_counts[jid],
                    "ExplanationKeys": existing_facts,
                    "AvailableExplanations": len(existing_facts),
                    "ExplanationAPI": self.base_api + "&job_id={}&num_candidates=20".format(jid)
                }
                if jid not in existing_jobids:
                    analyzed_contds.extend(contd_details)
                self.testbed_jobs.append(merge_dicts(({"JobId": jid}, arya_jobdetails[jid], expl_jobdetails)))
                jobs_record.append(ccompany_job_title)
            # +++++++++++++++++
            # Copy all candidates details for whom there are explanation facts
            if not copy_info:
                copy_info = False
            MySQLHelpers.transact_cands_from_tbl(base_table, db_key, db_name, "delete", copy_table, copy_info=copy_info)
            if analyzed_contds:
                MySQLHelpers.insert_bulk_data(analyzed_contds, db_key, db_name, base_table, copy_table)
            self._summarize_testbed_jobs(concise_info)
            save_files(self.testbed_jobs, save_path, 'explanation_jobs_details', '.json', indent=4, default=str)
        except Exception as error:
            LOGGER.error(error)
            LOGGER.error("Unexpected Error in creating QA testbed !!")
            raise error
       

if __name__ == '__main__':
    print('python version:', sys.version)   
    print('cwd:', os.getcwd())
    # _testbed = CreateQATestbed(job_ids=[377534, 377522, 377407, 377137])
    # _testbed.create_testbed(refresh_data=False, parallelize=True, concise_info=True, save_path=CUSTOM_SAVE_PATH)
    # print(json.dumps(_testbed.testbed_jobs, indent=4, default=str))
