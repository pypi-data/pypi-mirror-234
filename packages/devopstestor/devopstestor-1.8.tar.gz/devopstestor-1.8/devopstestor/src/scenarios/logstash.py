import time
from log_manager import logging
from utils import tail
log = logging.getLogger('scenario.logstash')

import yaml
def mock_logstash_conf(machine_provisionner, logstash_provisionner, init_contexte, logstash_pipeline_conf):
    """
    Modifie la configuration de logstash afin de la rendre compatible avec les verifiers io
    """
    res, out = logstash_provisionner.mock_logstash_input(logstash_pipeline_conf, init_contexte['logstash_input_http_port'])
    if res is False:
        return res, out

    return logstash_provisionner.mock_logstash_output(
        logstash_pipeline_conf,
        logstash_out_filepath=init_contexte['logstash_out_filepath'],
        verifiers_logstash_out_filepath=init_contexte.get('verifiers_logstash_out_filepath', init_contexte['logstash_out_filepath'])
    )

def lancer_test_io(logstash_provisionner, init_contexte):
    """
    Affiche le contexte et ne fait rien (les verifications sont geres par les verifieurs)
    """
    # Initialisation et changement des droits du fichier de sorti
    logstash_provisionner.initialise_mock_output_file(
        init_contexte.get('verifiers_logstash_out_filepath', init_contexte['logstash_out_filepath'])
    )

    return True, yaml.dump(init_contexte['test_messages']['input_message'])

def tester_config(machine_provisionner, logstash_provisionner, init_contexte, **provisionner_params):
    """
    Utilise le binaire logstash dans le but de valider la structure de la configuration
    """
    # Start logstash in test mode
    return logstash_provisionner.test_config(**provisionner_params)
