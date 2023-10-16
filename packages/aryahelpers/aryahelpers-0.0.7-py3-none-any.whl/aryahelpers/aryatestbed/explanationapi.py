"""Flask api to access candidates explanations from DB"""
# http://192.168.38.99:1502/api/qa?expl_type=facts&job_id=359229&name=Vinay%20Pratap
# http://192.168.38.99:1502/api/qa?expl_type=facts&job_id=371151&recommendation_status_id=3
# http://192.168.38.99:1502/api/qa?expl_type=company&job_id=359228&num_candidates=10
# http://192.168.38.99:1502/api/staging?job_id=199436&num_candidates=20


import sys, os, json
BASE_PATH = os.path.abspath("./arya-helpers/Codes/src")
extendPaths = [p for p in (os.path.dirname(BASE_PATH), BASE_PATH) if p not in sys.path]
sys.path = extendPaths + sys.path
from copy import deepcopy
from aryautils.storageutils import MySQLManager
from aryahelpers.config import CONFIG, ALL_FEATURES, FACT_TOKENS, CANDIDATE_TABLES
from aryahelpers.utils.genericutils import merge_dicts, flatten_iterable
from flask import Flask, request, jsonify
import logging
LOGGER = logging.getLogger(__name__)

app = Flask(__name__)


class AccessExplanations(object):
    """Access candidates explanations from DB"""
    def __init__(self, **kwargs):
        self._ALL_FEATURES = set(k.lower() for k in ALL_FEATURES)
        [setattr(self, k, v) for k, v in kwargs.items()]
        # job_id, num_candidates, candidate_name, candidate_guid
    
    @staticmethod
    def get_jtr_candidates(jobid, db_key):
        """Get JTR candidates"""
        base_query = "SELECT job_id, candidate_name, portal_candidate_id, recommendation_status_id \
            FROM `arya`.`job_top_recommendations` jtr JOIN `arya`.`job_recommendations_metadata` jrm \
                ON jtr.recommendation_id = jrm.recommendation_id WHERE job_id = "
        query_str = base_query + "{} ORDER BY candidate_score DESC;".format(jobid)
        jtr_candidates = MySQLManager.execute_query(query_str, (), **CONFIG[db_key]['arya'])
        return jtr_candidates
    
    def get_explanation_facts(self, candidate_details: dict):
        """Filter explanations, based on `explanation_type`"""
        explanation_type = self.explanation_type  # 'company', 'skill', 'role', 'occupation',
                                                  # 'industry', 'experience', 'facts'
        filtered_explanations = {}
        if explanation_type:
            if explanation_type != 'facts':
                filtered_explanations = candidate_details.get(
                    explanation_type, candidate_details.get(explanation_type.title(), {}))
            else:
                all_explkeys = list(candidate_details.keys())
                all_explkeys = {k: k if k.lower() != 'summary' else f'#{k}' for k in all_explkeys if isinstance(
                    candidate_details[k], dict) and (set(candidate_details[k].keys()) & FACT_TOKENS)}
                filtered_explanations["ExplanationFacts"] = {}
                for _explkey in all_explkeys:
                    for _fact_key in FACT_TOKENS:
                        get_facts = candidate_details.get(_explkey, {}).get(_fact_key, [])
                        if isinstance(get_facts, list):
                            get_facts = [_fact.get('Fact', '') + _fact.get('fact', '') if isinstance(
                                _fact, dict) else _fact for _fact in get_facts]
                        if get_facts:
                            filtered_explanations["ExplanationFacts"][all_explkeys[_explkey]] = get_facts
                            break
        else:
            return candidate_details
        return filtered_explanations
    
    def extract_analyzed_candidates(self, expl_tbl_key, job_id=None, expl_type=None):
        """Extract analyzed candidates details from the respective db"""
        cand_details = []
        db_key, db_name, table_name, jobid_key, contd_guid, expl_key = tuple(
            CANDIDATE_TABLES["explanation"][expl_tbl_key].values())
        if expl_tbl_key == 'staging':
            query_str = "SELECT {}, {}, {} FROM {} WHERE {}={}".format(
                jobid_key, contd_guid, expl_key, table_name, jobid_key, job_id)
        else:
            # Add the respective Score
            score_keys = ["CandidateScore"]
            if expl_type in self._ALL_FEATURES:
                score_keys += [] if expl_type in ['facts', 'summary'] else [
                    "{}Score".format(expl_type.title())] if expl_type != 'role' else ['RoleLevelScore']
            else:
                score_keys += ['CompanyScore', 'RoleLevelScore', 'OccupationScore', 'EducationScore',
                               'ExperienceScore', 'IndustryScore', 'SkillScore']
            query_str = "SELECT {}, {}, {}, CONVERT_TZ(UpdatedDateTime,'+00:00','+05:30') \
                AS UpdatedDateTime, {} FROM {} WHERE {}={}".format(
                    jobid_key, ", ".join(score_keys), contd_guid, expl_key, table_name, jobid_key, job_id)
        cand_details = MySQLManager.execute_query(query_str, (), **CONFIG[db_key][db_name])
        cand_details = [{k: v for k, v in d.items() if v or (k not in score_keys)} for d in cand_details]
        for idx, d in enumerate(cand_details):
            cand_details[idx][expl_key] = deepcopy(json.loads(d[expl_key]))
            cand_details[idx][expl_key] = self.get_explanation_facts(cand_details[idx][expl_key])
        return cand_details
    
    def filter_candidates(self, contd_details: list, filter_keys: tuple):
        """Filter `contd_details` with respect to `filter_keys`"""
        filtered_details = contd_details.copy()
        num_candidates = self.num_candidates
        candidate_name = self.candidate_name
        candidate_guid = self.candidate_guid
        recommendation_status_id = self.recommendation_status_id  #[1, 2, 3]
        if num_candidates:
            filtered_details = [d for d in filtered_details[:num_candidates]]
        if candidate_name:
            filtered_details = [d for d in filtered_details if d[filter_keys[0]] == candidate_name]
        if candidate_guid:
            filtered_details = [d for d in filtered_details if d[filter_keys[1]] == candidate_guid]
        if recommendation_status_id:
            filtered_details = [d for d in filtered_details if d[filter_keys[2]] == recommendation_status_id]
        return filtered_details
    
    def access_explanations(self):
        """Access explanations, based on specific filtering conditions"""
        job_id, base_env = self.job_id, self.base_env
        explanation_type = self.explanation_type

        # Access candidates explanations and other details
        cand_explanations, filter_guids = [], []
        expl_tbl_key = 'qa-reservoir' if base_env == 'qa' else 'copy' if base_env == 'new' else 'staging'
        cand_details = self.extract_analyzed_candidates(expl_tbl_key, job_id, explanation_type)
        if not cand_details and (base_env in ['qa', 'new']):
            expl_tbl_key = 'qa-arya'
            cand_details = self.extract_analyzed_candidates(expl_tbl_key, job_id, explanation_type)
        
        # Filter cand_guids
        db_key, guid_key = [CANDIDATE_TABLES["explanation"][expl_tbl_key][k] for k in ('db_key', 'guid_key')]
        jtr_candidates = self.get_jtr_candidates(job_id, db_key)
        if jtr_candidates:
            filter_guids = [(d['candidate_name'], d['portal_candidate_id'],
                             d['recommendation_status_id']) for d in jtr_candidates]
            filter_guids = self.filter_candidates(filter_guids, (0, 1, 2))
            # Access explanations
            for cand_info in filter_guids:
                subset_cands = [d for d in cand_details if d[guid_key] == cand_info[1]]
                if guid_key == 'portalGuid':
                    subset_cands = sorted(subset_cands, key=lambda d: d['UpdatedDateTime'], reverse=True)
                if subset_cands:
                    subset_cands = merge_dicts(({
                        "CandidateName": cand_info[0], "recommendation_status_id": cand_info[2]}, subset_cands[0]))
                    cand_explanations.append(subset_cands)
        else:
            # if jtr_candidates list is empty, e.g. manually entered info
            cand_details = [d for d in cand_details if d.get("CandidateScore", 0) >= 0]
            cand_details = sorted(cand_details, key=lambda x: x.get("CandidateScore", 0), reverse=True)
            cand_details = self.filter_candidates(cand_details, ('', guid_key, ''))
            cand_explanations.extend(cand_details)
        cand_explanations = flatten_iterable(cand_explanations)
        return cand_explanations
    

@app.route('/api/<base_env>', methods=['GET'], strict_slashes=False)
def main_func(base_env=None):
    try:
        response = []
        # Access input params
        job_id = request.args.get('job_id')
        num_candidates = request.args.get('num_candidates')
        if num_candidates:
            num_candidates = int(num_candidates)
        candidate_name = request.args.get('name')
        candidate_guid = request.args.get('guid')
        recommendation_status_id = request.args.get('recommendation_status_id')
        explanation_type = request.args.get('expl_type', 'facts').lower()
        if recommendation_status_id:
            recommendation_status_id = int(recommendation_status_id)
        accessor = AccessExplanations(
            job_id=job_id, num_candidates=num_candidates, candidate_name=candidate_name,
            candidate_guid=candidate_guid, recommendation_status_id=recommendation_status_id,
            explanation_type=explanation_type, base_env=base_env)
        response = accessor.access_explanations()
    except Exception as error:
        LOGGER.error('Failed in accessing candidates explanations from DB !')
        LOGGER.exception(error)
    return jsonify(response)
  

if __name__ == '__main__':
    app.run("0.0.0.0", port=1502)
