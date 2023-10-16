from abstract_provisionner import AbstractProvisionner
from log_manager import logging
log = logging.getLogger('provisionner.LogstashProvisionner')
import os
class LogstashProvisionner(AbstractProvisionner):

    ########### Initialisation du provisionner ###########
    def initialise(self, machine_controller, machine_name):
        self.machine_controller = machine_controller
        self.env = self.global_config.get_node('machine').get_node('env')

    ########### Lancement de logstash ###############
    def test_config(self, **others):
        """
        Lancement oneshot afin de tester la configuration fournie
        """
        arguments= [
            "--log.level=info",
            "--config.debug",
            "--config.test_and_exit"
        ]
        path_settings =  others.get('path_settings', None)
        if path_settings is not None:
            arguments.append("--path.settings {}".format(path_settings))

        username = others.get('run_as', 'root')

        # Lancement Logstash
        ret, out = self.machine_controller.run_cmd(
            "su -l {} -c '{} {}'".format(
                username,
                self.env.get('logstash::bin_path'),
                " ".join(arguments)
            )
        )

        # Interpretation resultats
        result = True if ret == 0  else False
        return result, out

    ########### Lancement du servuce logstash ###############
    def mock_logstash_input(self, pipeline_conf_path, logstash_input_http_port):
        """
        Remplace la partie input d'un pipeline par une sortie permettant l'utilisation des testsauto
        """

        # Recuperation du contenu de la configuration a mocker
        ret, file_content = self.machine_controller.get_file_content(file_path=pipeline_conf_path)

        logstash_conf_mock = """
        # Debut Mock ajoute par les testauto
        input{
         http {
           codec => "json"
           port => """ + str(logstash_input_http_port) + """
           ecs_compatibility => disabled
         }
        }
        # Fin Mock ajoute par les testauto
        """
        iline = 0
        file_content_lines = file_content.split('\n')

        # Recherche de la ligne ou apparait le "filter{" ou "output{" pour s'arreter juste avant"
        # ce qui suivra sera supprime
        while iline < len(file_content_lines) and file_content_lines[iline].replace(' ', '')[:7] != "filter{" and file_content_lines[iline].replace(' ', '')[:7] != "output{":
            iline += 1

        logstash_conf_mock += '\n'.join(file_content_lines[iline::])

        # Remplacement de la config par le mock
        ret, file_content = self.machine_controller.put_in_file(
            content=logstash_conf_mock,
            file_path=pipeline_conf_path
        )
        return True if ret == 0  else False, "config mockee : {}\n".format(logstash_conf_mock)

    def mock_logstash_output(self, pipeline_conf_path, logstash_out_filepath, verifiers_logstash_out_filepath):
        """
        Remplace la partie output d'un pipeline par une sortie permettant l'utilisation des testsauto
        """

        # Recuperation du contenu de la configuration a mocker
        ret, file_content = self.machine_controller.get_file_content(file_path=pipeline_conf_path)

        logstash_conf_mock = ""
        iline = 0
        file_content_lines = file_content.split('\n')
        # Recherche de la ligne ou apparait le "output{"
        # ce qui suivra sera supprime
        while iline < len(file_content_lines) and file_content_lines[iline].replace(' ', '')[:7] != "output{":
            logstash_conf_mock += file_content_lines[iline] + "\n"
            iline += 1
        # Le output est remplace par le mock
        logstash_conf_mock += """
        output{ # Debut Mock ajoute par les testauto
         file {
           codec => "json_lines"
           enable_metric => false
           ecs_compatibility => disabled
           path => \"""" + str(logstash_out_filepath) + """\"
           file_mode => 0777
         }
        } # Fin Mock ajoute par les testauto
        """

        # Remplacement de la config par le mock
        ret, file_content = self.machine_controller.put_in_file(
            content=logstash_conf_mock,
            file_path=pipeline_conf_path
        )
        self.initialise_mock_output_file(verifiers_logstash_out_filepath)
        # Initialisation et changement des droits du fichier de sorti
        return True if ret == 0  else False, "config mockee : {}\n".format(logstash_conf_mock)

    def initialise_mock_output_file(self, verifiers_logstash_out_filepath):
        ret, out = self.machine_controller.run_cmd(f"touch {verifiers_logstash_out_filepath}")
        ret, out = self.machine_controller.run_cmd(f"chmod 777 {verifiers_logstash_out_filepath}")
        return str(ret) != '0', out
