# Installation
```bash
python3.10 -m venv venv
pip install -r requrements.txt
```

# Push to PyPI
```commandline
python setup.py sdist bdist_wheel
twine upload dist/*
```

```commandline
username: __token__
password: <token>
```