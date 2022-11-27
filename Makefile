# Heavily borrowed from:
# https://github.com/audreyr/cookiecutter-pypackage/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/Makefile

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -and -not -name "venv*" -exec rm -fr {} +
	find . -name '*.egg' -and -not -name 'venv*' -exec rm -rf {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -f 5f0d96.yaml
	rm -f default_inventory.ini
	rm -f default_inventory.yaml
	rm -f default_testbed.yaml
	rm -f .virl/cached_cml_labs/*
	rm -f .virl/current_cml_lab

lint: ## check style with flake8
	flake8

coverage:
	coverage run --source=virl setup.py test

report: coverage
	coverage html
	coverage report
	open htmlcov/index.html

test: ## run tests quickly with the default Python
	python -W ignore::DeprecationWarning setup.py test

release: dist ## package and upload a release
	@echo "*** Uploading virlutils... ***"
	twine upload dist/virl*
	@echo "*** Uploading cmlutils... ***"
	twine upload dist/cml*

dist: clean ## builds source and wheel package
	# Build virlutils
	python setup.py sdist
	python setup.py bdist_wheel
	# Flip the name
	sed -i .orig -e 's|NAME,|CMLNAME,|' setup.py
	# Build cmlutils
	python setup.py sdist
	python setup.py bdist_wheel
	cp -f setup.py.orig setup.py
	rm -f setup.py.orig 
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
