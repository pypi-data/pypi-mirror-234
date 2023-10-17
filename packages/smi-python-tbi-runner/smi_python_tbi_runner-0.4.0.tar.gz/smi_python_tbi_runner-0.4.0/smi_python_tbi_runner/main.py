import importlib
import sys

from smi_python_tbi_runner.runner_application import main

if __name__ == "__main__":
    module_name = "register"
    try:
        register_module = importlib.import_module("application")
        register_module.register()
    except ImportError:
        print(f"Couldn't load module: {module_name}")
    sys.exit(main(sys.argv))
