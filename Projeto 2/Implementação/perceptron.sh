#!/bin/bash

source .env/bin/activate
python main.py "$@"

source ./env/bin/diactivate