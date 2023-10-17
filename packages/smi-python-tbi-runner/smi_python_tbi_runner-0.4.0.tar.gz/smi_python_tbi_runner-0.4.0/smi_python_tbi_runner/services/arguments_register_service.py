from smi_python_commons.arguments.argument import Argument


class ArgumentsRegisterService:

    def __init__(self):
        self.arguments = []

    def register(self, argument: Argument):
        self.arguments.append(argument)


arguments_register_service = ArgumentsRegisterService()
