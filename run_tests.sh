#!/usr/bin/env bash

echo "Installing dependencies…"
pipenv --venv && pipenv --rm && pipenv install --dev
pipenv run pip install --upgrade -e .

echo "$ pipenv run time pytest -v --terraform-dir=terraform"
pipenv run pytest