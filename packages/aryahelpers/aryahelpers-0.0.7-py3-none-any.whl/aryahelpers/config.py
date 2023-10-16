import json
import pickle
from pkgutil import get_data

config_folder, data_folder = 'aryahelpers.configuration', 'aryahelpers.data'
CONFIG = json.loads(get_data(config_folder, 'config.helpers.json').decode())
HEADERS = {'Content-Type': 'application/json'}
CUSTOM_SAVE_PATH = ''.join(CONFIG['CUSTOM_SAVE_PATH'])
ENGLISH_WORDS = set(pickle.loads(get_data(data_folder, 'english_words.p'))["ENGLISH_WORDS"])
CANDIDATE_TABLES = CONFIG["candidate_tables"]
FACT_TOKENS = {'ExplanationFacts', 'Explanation', 'facts', 'Facts'}
ALL_FEATURES = {'Summary', 'Skill', 'Role', 'Occupation', 'Company', 'Industry', 'Education', 'Experience'}

# Bucket dict
BUCKET_DICT = {
    1: ["0-50", "Small"],
    2: ["50-250", "Small"],
    3: ["250-500", "Small"],
    4: ["500-1K", "Medium"],
    5: ["1K-5K", "Medium"],
    6: ["5K-10K", "Medium"],
    7: ["10K-50K", "Large"],
    8: ["50K-100K", "Large"],
    9: ["100K-500K", "Large"],
    10: ["500K-1M", "Large"],
    11: ["1M-10M", "Very large"],
    12: ["10M-100M", "Very large"],
    13: ["100M-500M", "Very large"],
    14: ["500M-1B", "Very large"],
    15: ["1B+", "Very large"]
}

# Companies specific service stopwords
company_stopwords = [
    'agreement', 'amendment', 'bill', 'biz', 'blank', 'bv', 'client', 'clubs', 'co', 'com', 'comp',
    'companies', 'company', 'confidential', 'contract', 'corp', 'corporate', 'corporation', 'dba', 'government',
    'govt', 'group', 'http', 'https', 'inc', 'including', 'incorp', 'incorporat', 'incorporate', 'incorporated',
    'incorporation', 'industries', 'international', 'intl', 'intnl', 'license', 'limited', 'llc', 'llp', 'ltd',
    'machines', 'maintenance', 'membership', 'name', 'ny', 'office', 'oh', 'private', 'pte', 'pvt', 'rent', 's',
    'san', 'service', 'services', 'st', 'unknown', 'utilities', 'utility', 'web', 'website', 'working', 'www',
    'yrs', 'yr', 'mos', 'mo', 'fulltime', 'parttime', 'permanent', 'temporary'
]