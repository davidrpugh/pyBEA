#!/usr/bin/env bash
set -ev  # Needed in order for Travis CI to report failure

if [ $TRAVIS_BRANCH == "master" ] && [ $TRAVIS_EVENT_TYPE == "push" ]
then
  python setup.py sdist bdist_wheel
  twine upload -u $PYPI_USERNAME -p $PYPI_PASSWORD dist/*
else
  echo "No releases published for this build!"
fi
