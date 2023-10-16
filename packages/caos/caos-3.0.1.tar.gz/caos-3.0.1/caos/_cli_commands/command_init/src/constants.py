NAME: str = "init"
DESCRIPTION: str = """\
            Creates a Python virtual environment based on the configuration
            of an existing 'caos.yml' file in the current directory.
            
            If the 'caos.yml' file is not present in the current directory a
            new virtual environment and configuration file are created.
            
            If the '--simple' flag is used a simplified version of the 'caos.yml'
            is generated and no virtual environment is created automatically.\
"""
CLI_USAGE_EXAMPLE: str = """\
            caos init  
            caos init [VIRTUAL_ENV_NAME]
            caos init --simple | -s | -S
"""

_CAOS_YAML_TEMPLATE="""\
virtual_environment: {VENV_NAME}

dependencies:
  pip: latest
#  requests: 2.31.0  # Allow only Exact version
#  numpy: ^1.26.0 # Allow only Minor version changes
#  flask: ~3.0.0  # Allow only Patch version changes
#  flask: ./flask-3.0.0.tar.gz # Local tar.gz package
#  colorama: ./local_libs/colorama-0.4.6-py2.py3-none-any.whl # Local WHl package
#  colorama: https://files.pythonhosted.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl 

tasks:
  unittest:
    - echo Testing...
    - caos python -m unittest discover -v ./
#
#  start:
#    - echo Starting...
#    - caos python ./main.py
#
#  test_and_start:
#    - unittest
#    - start
"""

_CAOS_YAML_TEMPLATE_SIMPLE="""\
virtual_environment: {VENV_NAME}

dependencies:
  pip: latest

tasks:
  hello:
    - echo Hello World!
"""
