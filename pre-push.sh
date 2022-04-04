#!/bin/bash
echo "Export requirements"
poetry export -f requirements.txt --output requirements.txt --without-hashes
echo "Run autoflake"
autoflake --recursive --in-place  --remove-unused-variables --remove-all-unused-imports  --ignore-init-module-imports .
echo "Run black"
black .
echo "Rin isort"
isort .
echo "Run flake8"
flake8 . --count --statistics
echo "Run mypy"
mypy .
echo "OK"


