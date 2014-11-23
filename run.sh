#!/bin/bash

if [[ "$(uname)" == "Darwin" && -f "/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python" ]]; then
    # Run python under 32bit for OSX
    arch -i386 /System/Library/Frameworks/Python.framework/Versions/2.7/bin/python serve.py
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Run python as is.
    python serve.py
fi
