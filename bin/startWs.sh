#!/bin/bash
# get current path
parent_path=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
cd "$parent_path"

# set environment variables
source ./envrc

# start web services
python ../ws/ws.py
