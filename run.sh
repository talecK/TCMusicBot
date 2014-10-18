#!/bin/bash

source tcmusicbot-venv/bin/activate

PYTHON_V=$(which python)

arch -i386 $PYTHON_V serve.py
