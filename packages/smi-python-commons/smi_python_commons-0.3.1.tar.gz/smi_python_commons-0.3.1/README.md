# python-commons

## Development

### Preparations

```shell
# Win
py -3.9 -m venv ./.venv
# *nix
python -m venv ./.venv
# Win
.\.venv\Scripts\activate
# *nix
source ./.venv/bin/activate
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
python -m unittest discover -s ./test/info/setmy
```

### Run integration tests

```shell
python -m unittest discover -s ./test/info/setmy -p it_*.py
```

### Run behave (Cucumber) integration tests

```shell
behave
```

### All tests

```shell
python -m unittest discover -s ./test/info/setmy && python -m unittest discover -s ./test/info/setmy -p it_*.py && behave
```

### Update version info

```shell
# Win
set NAME=smi_python_commons
set VERSION=0.3.1
# *nix
NAME=smi_python_commons
VERSION=0.3.1
# Win
python smi_python_commons/scm_version.py %NAME% %VERSION%
# *nix
python smi_python_commons/scm_version.py ${NAME} ${VERSION}
git add ./smi_python_commons/project.py
git commit -m "project.py updated"
```

## Deploy

```shell
python setup.py sdist bdist_wheel
twine upload dist/*
git tag -a 0.3.1 -m "0.3.1"
git push --tags
```

## Release

1. Update version info
2. Deploy

```shell
python setup.py sdist bdist_wheel && twine upload dist/*
```
