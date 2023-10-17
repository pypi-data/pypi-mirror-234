.PHONY: default clean install pip-install test install-with-tests distribute generate-docs publish-docs
ENVIRONMENT_NAME=venv
DOCS_PATH=./docs/_build/html

default:
	@echo "Read the readme"

clean:
	rm -rf $(ENVIRONMENT_NAME) build dist montecarlodata.egg-info .coverage nosetests.xml

install: clean
	virtualenv $(ENVIRONMENT_NAME); \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	pip install -r requirements-dev.txt; \
	$(MAKE) pip-install; \
	montecarlo --version

pip-install:
	pip install --editable .

format:
	. $(ENVIRONMENT_NAME)/bin/activate; python -m black .

test:
	@# Requires activating the virtualenv created in `install` if running locally
	export DEBUG=True; unset MCD_USER_ID_HEADER; coverage run -m pytest ./tests

lint:
	. $(ENVIRONMENT_NAME)/bin/activate; python -m black --check .

install-with-tests: install
	. $(ENVIRONMENT_NAME)/bin/activate; $(MAKE) test

install-with-tests-and-lint: install-with-tests
	. $(ENVIRONMENT_NAME)/bin/activate; $(MAKE) lint

distribute: install
	. $(ENVIRONMENT_NAME)/bin/activate; \
	pip install -r requirements-ci.txt; \
	python setup.py sdist bdist_wheel; \
	twine check dist/*; \
	twine upload --non-interactive dist/*

generate-docs: install
	. $(ENVIRONMENT_NAME)/bin/activate; \
	pip install -r requirements-ci.txt; \
	make -C docs clean; \
	make -C docs html; \
	cp -a ./docs/_static/. $(DOCS_PATH)

publish-docs: generate-docs
	aws s3 cp $(DOCS_PATH)/ s3://${CLI_DOCS_BUCKET} --recursive
	AWS_MAX_ATTEMPTS=10 aws cloudfront create-invalidation --distribution-id=${CLI_DOCS_CLOUDFRONT_DIST} --paths /* --no-cli-pager
