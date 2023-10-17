# AioKafkaEngine

## building
```sh
python3 -m pip install --upgrade build
python3 -m build
```
## distributing
For the username, use __token__. For the password, use the token value, including the pypi- prefix.
```sh
python3 -m pip install --upgrade twine
# python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*
```
