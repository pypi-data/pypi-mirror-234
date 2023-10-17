PROJECT_NAME=lrn-cli

PYTHON=python3
VIRTUALENV=${PYTHON} -m venv
VENV=.venv
VENVPATH=${VENV}/${PROJECT_NAME}

SED=$(shell which gsed || which sed)

all: ${VENVPATH}/bin/lrn-cli

test: ${VENVPATH}/bin/pytest
		${VENVPATH}/bin/python -m pytest

dist: dist-clean venv-dev
	${VENVPATH}/bin/${PYTHON} setup.py sdist
	${VENVPATH}/bin/${PYTHON} setup.py bdist_wheel --universal

release:
	${info Once built, you can use \`make dist-upload\` to publish the new version to PyPI}
	./release.sh

dist-upload: dist-check-version clean test dist-upload-twine
PKG_VER=v$(shell ${SED} -n "s/^.*__version__\s*=\s*\"\([^']\+\)\".*$$/\1/p" src/_version.py)
GIT_TAG=$(shell git describe --tags)
dist-check-version:
ifeq ('$(shell echo ${GIT_TAG} | grep "^${PKG_VER}$$")', '')
	$(error Version number ${PKG_VER} in src/_version.py does not match git tag ${GIT_TAG})
endif
dist-upload-twine: dist ${VENVPATH}/bin/twine # This target doesn't do any safety check!
	${VENVPATH}/bin/twine upload dist/*

clean: dist-clean
	find . -path __pycache__ -delete
	find . -name *.pyc -delete
dist-clean:
	test ! -d dist || rm -r dist
real-clean: clean
	test ! -d ${VENV} || rm -r ${VENV}
	test ! -d lrn_cli.egg-info || rm -r lrn_cli.egg-info

# Python environment and dependencies
venv ${VENVPATH}/bin/lrn-cli: ${VENVPATH}/bin/pip
	${VENVPATH}/bin/pip install -e .
venv-dev ${VENVPATH}/bin/twine: ${VENVPATH}/bin/pip
	${VENVPATH}/bin/pip install -e .[dev]
venv-test ${VENVPATH}/bin/pytest: ${VENVPATH}/bin/pip
	${VENVPATH}/bin/pip install -e .[test]
${VENVPATH} ${VENVPATH}/bin/python ${VENVPATH}/bin/pip:
	${VIRTUALENV} ${VENVPATH}

.PHONY: all test clean dist-clean real-clean \
	release dist dist-upload dist-check-version dist-upload-twine \
	venv venv-dev venv-test
