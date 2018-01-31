#!/usr/bin/env bash

set -u # crash on missing env
set -e # stop on any error

cd api

echo "Running style checks"
flake8

echo "Running unit tests 2"
python -m pytest
