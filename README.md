# Test Framework

## Common info:

- Stack: `python`+`pytest`+`selenium`+`docker`+`selenoid-ui`+`allure-server`
- Ready-made solution for `ui/api` testing
- Implemented `selenium` wrapper, integration with `allure-server` and `selenoid/ggr`
- Various clients are implemented, such as `http-client`, `orm`, `imap`, `ssh`, `greylog`
- Tests run in parallel, each in its own container
- Remote launch tests by `gitlab-ci`


## Environment requirements:

1) `Python` ver `3.10.x`
2) `PyСharm Community Edition` or `IntelliJ IDEA Ultimate`
3) Webdriver `chromedriver` and `geckodriver` if you need testing ui
4) `ohMyZsh` for Unix and `Windows Terminal + PowerShell` for Windows

## Setting up environment in IntelliJ IDEA/Pycharm

For setup virtual environment in IDE **recommended** to use the suggested IDE settings when exporting the repository

Manually install virtual environment is below:

<details><summary><b>Show</b></summary><br>

1. Install virtualenv package

```shell script
pip3 install virtualenv
```

2. Create new virtualenv

```shell script
virtualenv env
```

3. Activate new virtualenv

```shell script
venv activate
```

4. Install requirements in your virtualenv

```shell script
pip install -r requirements.txt
```

### Setting up the interpreter

1. Open IDE and go to interpreter settings:

```shell script
File -> Setting -> Project Interpreter
```

2. In the drop-down window specify the path to the interpreter in the virtual environment:

```shell script
/env/bin/python
```

You can also create a new instance of the virtual environment and the interpreter by [official documentation](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html)

### Setting up the test-runner

1. Open IDE and go to tools settings:

```shell script
File -> Setting -> Tools -> Python Integrated Tools
```

2. In the drop-down menu `Default test runner` select `pytest`

</details>

## Test run parameters

<details><summary><b>Show</b></summary><br>

You must uncomment the `pytest.ini.dist` file manually or with a command before running the tests:

```shell script
cp pytest.ini.dist pytest.ini
```

### Run args

For ease of launching and debugging tests, you can change the launch parameters in the `conftest.py` file instead of typing commands

1. Open file `conftest.py`

2. Go to func `pytest_addoption`

3. Change necessary key `default` for run args

Test run parameters in `conftest.py`:

`--env` - select env for test launch, corresponds to the names of the `.env` files in the directory `config/`

`--browser` - select browser for test launch

`--log_level` - select level logs

`--report` - select option of the generating Allure reports. `enable` or `disable`

Test run parameters in `pytest.ini`:

`--reruns [n]` - rerun all failed tests, where `n` - count of reruns

`--reruns-delay [seconds]` - delay before run failed test, in sec

`--only-rerun [ErrorType]` - rerun tests, which failed with specific error, `ErrorType` - type of error, for example, `AssertionError`

</details>

## Troubleshooting

<details><summary><b>Show</b></summary><br>

### Launch malfunctions

// in work

</details>

## Checking code quality

<details><summary><b>Show</b></summary><br>

External module is connected to check the quality of the code [pre-commit](https://pre-commit.com/)

Configuration is listed in the file .pre-commit-config.yaml

For local checking:
```
pre-commit install
```
Now checking of code will be launch automatically when you call `git commit`

Current connected checks:
* Checking spelling errors (English)
* Trimming unnecessary spaces
* Alphabetical sorting of dependencies in requirements.txt
* The last empty line (PEP8)

Connected packages:
* isort
* codespell
* flake8
* black

</details>