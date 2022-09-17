# example todo applications with Flask framework

There are three example applications all using Flask.

- todos_mvc: classic mvc web stack
- todos_rest_singlefile: a miminal single-file flask REST api stack
  - raw sql data access implementation
- todos_rest_sql: REST api stack, the modular version of the singfile stack

## python environment setup

For each stack, environment is set by its own Dockerfile.

For a local development environment, use pyenv venv setup:

```sh
# create .python-version file with v3.7.13
pyenv shell 3.7.13
# venv is natively supported in python v3.4+
python -m venv venv
# activate venv:
source venv/bin/activate
# install pkgs
pip install -r requirements.txt

# to deactivate venv:
(venv) > deactivate
```

For older Python versions, like 3.7, need to update pip to avoid
possible setup.py metada error.

```sh
python -m pip install --upgrade pip
pip install setuptools --force-reinstall
```
