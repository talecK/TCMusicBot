#!/bin/bash

PYTHON_V=$(which python)

if [ "$(uname)" == "Darwin" ]; then
    # Run python under 32bit for OSX
    arch -i386 $PYTHON_V serve.py
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Run python as is.
    $PYTHON_V serve.py
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    # Optional handling under windows git bash.
fi
