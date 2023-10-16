# python-tbi-runner

Training Backlog Item file parser

## Development

### Preparations

```shell
py -3.9 -m venv ./.venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For developing depending project/module, dependency can be added into **requirements.txt** as:

    python-commons @ file:///C:/sources/setmy.info/submodules/python-commons

### PyCharm

"File" -> "Settings" -> Python Integrated Tools -> Default test runner: Unittest

Running tests have a problem: working directory has to be set for tests.

### Run unit tests

```shell
python -m unittest discover -s ./test
```

### Run integration tests

```shell
python -m unittest discover -s ./test -p it_*.py
```

### All tests

```shell
python -m unittest discover -s ./test && python -m unittest discover -s ./test -p it_*.py
```

### Update version info

```shell
python git_version.py
git add ./smi_python_tbi_runner/project.py
git commit -m "project.py updated"
```

## Deploy

```shell
python setup.py sdist bdist_wheel
twine upload dist/*
git tag -a 0.3.0 -m "0.3.0"
git push --tags
```

## Release

1. Update version info
2. Deploy

```shell
python setup.py sdist bdist_wheel && twine upload dist/*
```

## Usage

**register.py**

```python
from smi_python_commons.arguments.argument import Argument

from smi_python_tbi_runner.services.arguments_register_service import arguments_register_service
from smi_python_tbi_runner.services.runner_register_service import runner_register_service
from test.empty_runner import EmptyRunner


def register():
    arguments_register_service.register(Argument('example', 'e', str, 'Example', True))
    empty_runner = EmptyRunner()
    runner_register_service.register(empty_runner)
```
