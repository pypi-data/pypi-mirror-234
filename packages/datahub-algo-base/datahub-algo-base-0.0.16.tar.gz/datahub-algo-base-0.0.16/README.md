### Algorithm Node Template For DataHub

## Install
1. go get the source file [Test-Pypi](https://test.pypi.org/project/dataHubPy/0.0.7/)
2. unzip dataHubPy-X.X.X.tar.gz
3. cd source dir **dataHubPy-X.X.X**
4. execute
    ```shell
    python ./setup.py build
    python ./setup.py install
    ``` 

## Build
```shell
python .\setup.py sdist bdist_wheel
python -m twine upload -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkZTlkMDNiNGMtZTAzMi00N2M4LTg0MTYtYmJiODNiZmU0NmE0AAIqWzMsImRkODRhMjdiLWQ2MDgtNDMyNi1hZTUyLWI4ZGM1OTgyNWM5NSJdAAAGIDqe93qMQUwOaIcx9VB60pbA9iEx-Wvuu47LTakSxAs0 --repository-url https://test.pypi.org/legacy/ dist/*

```

## Algo Developer

after you debug your code, you can compress code by following shell:
```shell
tar --exclude='venv' --exclude='dataHubPy*' --exclude='*idea' -cvzf ../test_ay_algo.tar .

```