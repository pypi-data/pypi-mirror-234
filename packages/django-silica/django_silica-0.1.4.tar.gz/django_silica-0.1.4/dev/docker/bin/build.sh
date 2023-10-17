#!/bin/bash

# Determine script directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Change directory to project directory
cd $SCRIPT_DIR

docker build -f ../Dockerfile ../../example_project -t silica-test-app "$@"