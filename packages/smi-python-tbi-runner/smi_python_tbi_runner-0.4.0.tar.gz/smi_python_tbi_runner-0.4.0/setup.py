from setuptools import setup, find_packages

from smi_python_tbi_runner.project import NAME, VERSION

setup(
    name=NAME,
    version=VERSION,
    description='setmy.info Python TBI runner library.',
    long_description='setmy.info Python TBI runner library.',
    author='Imre Tabur',
    author_email='info@setmy.info',
    license='MIT',
    url='https://github.com/setmy-info/python-tbi-runner',
    packages=find_packages(),
    install_requires=[
        "smi-python-tbi-parser==0.1.0"
    ],
)
