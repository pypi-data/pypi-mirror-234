from smi_python_commons.arguments.argument import Argument
from smi_python_commons.arguments.config import Config
from smi_python_commons.arguments.constants import SMI_PROFILES_ARGUMENT, SMI_CONFIG_PATHS_ARGUMENT, \
    SMI_OPTIONAL_CONFIG_FILES_ARGUMENT
from smi_python_commons.config.application import Application
from smi_python_tbi_parser.tbi import parse_tbi

from smi_python_tbi_runner.services.arguments_register_service import arguments_register_service
from smi_python_tbi_runner.services.runner_register_service import runner_register_service


def main(argv):
    arguments_config = [
        SMI_PROFILES_ARGUMENT,
        SMI_CONFIG_PATHS_ARGUMENT,
        SMI_OPTIONAL_CONFIG_FILES_ARGUMENT,
        Argument('runner-command', 'r', str, 'Runner to be executed', True),
        Argument('tbi-file', 't', str, 'TBI yaml to be used', True),
        Argument('sub-command', 's', str, 'TBI sub-command', True)
    ]
    arguments_config.extend(arguments_register_service.arguments)
    argv_config = Config('TBI runner', arguments_config)
    app = Application(argv, argv_config)
    runner = runner_register_service.get_runner(app.arguments.runner_command)
    tbi = parse_tbi(app.arguments.tbi_file)
    return runner.execute(app, tbi, app.arguments.sub_command)
