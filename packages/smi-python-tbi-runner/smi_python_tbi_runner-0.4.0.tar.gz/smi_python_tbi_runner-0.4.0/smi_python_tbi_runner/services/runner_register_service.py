from smi_python_tbi_runner.runners.application_base_runner import ApplicationBaseRunner, DEFAULT_RUNNER


class RunnerRegisterService:

    def __init__(self):
        self.instances = {}

    def register(self, runner: ApplicationBaseRunner):
        self.instances[runner.get_name()] = runner

    def get_runner(self, sub_command: str):
        return self.instances.get(sub_command, DEFAULT_RUNNER)


runner_register_service = RunnerRegisterService()
