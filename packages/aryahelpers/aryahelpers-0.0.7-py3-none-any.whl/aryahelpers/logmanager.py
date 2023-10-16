import logging
import logging.handlers
from aryaesloghandler.handlers import AryaElasticLogHandler


def configure_logging(apps, config=None):
    if not apps:
        apps = [""]
    logging.basicConfig(format='%(asctime)s %(filename)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)
    es_handler = AryaElasticLogHandler(
        hosts=[{
            'host': config['logs_es_host'],
            'port': config['logs_es_port']
        }],
        use_ssl=False if config['logs_es_use_ssl'] == 'False' else True,
        # Can configure corresponding authentication authority
        auth_type=AryaElasticLogHandler.AuthType.NO_AUTH,
        es_index_name=config['logs_es_index'],
        # One index per month
        index_name_frequency=AryaElasticLogHandler.IndexNameFrequency.MONTHLY,
        flush_frequency_in_sec=15,
        # Additional environmental identification
        raise_on_indexing_exceptions=False)
    es_handler.setLevel(level=logging.INFO)
    for app_name in apps:
        logger = logging.getLogger(app_name)
        logger.addHandler(es_handler)
