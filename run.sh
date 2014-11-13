#!/bin/bash

PYTHON_V=$(which python)

if [[ "$(uname -s | tr '[:upper:]' '[:lower:]')" -eq "darwin" ]]; then
    arch -i386 $PYTHON_V serve.py
else
    $PYTHON_V serve.py
fi