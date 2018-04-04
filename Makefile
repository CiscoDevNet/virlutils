# Heavily borrowed from:
# https://github.com/audreyr/cookiecutter-pypackage/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/Makefile

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	flake8 

coverage:
	pip install -r test-requirements.txt
	coverage run --include virl ./tests/test_cli.py

report: coverage
	coverage html
	coverage report
	open htmlcov/index.html

test: ## run tests quickly with the default Python
	python setup.py test
