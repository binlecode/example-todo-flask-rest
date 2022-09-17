
# todos_rest_singlefile: minimal web stack

## python environment setup


```sh
# create .python-version file with v3.7.13
pyenv shell 3.7.13
# venv is natively supported in python v3.4+
python -m venv venv
# activate venv:
source venv/bin/activate

# for python 3.7, need to update pip and setuptools to 
# avoid possible setup.py metada error.
python -m pip install --upgrade pip
pip install setuptools --force-reinstall
# install pkgs
pip install -r requirements.txt

# to deactivate venv:
(venv) > deactivate
```

To run:

```sh
export FLASK_DEBUG=1
python todos_rest.py
```

This script will create a sqlite3 `todos.db` file