#!/bin/bash
LIB="lib"

# Make third party folder
if [[ ! -d $LIB ]]; then
    mkdir $LIB
fi

# Get third party dependencies
if [[ ! -d "$LIB/pygrooveshark" ]]; then
    git clone "https://github.com/koehlma/pygrooveshark.git" $LIB/pygrooveshark

    cd $LIB/pygrooveshark
    if [[ "$(uname)" == "Darwin" && -f "/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python" ]]; then
        sudo /System/Library/Frameworks/Python.framework/Versions/2.7/bin/python setup.py install
    else
        sudo python setup.py install
    fi

    cd ../../
fi

if [[ ! -d "$LIB/skype4py" ]]; then
    git clone "https://github.com/awahlig/skype4py.git" $LIB/skype4py

    cd $LIB/skype4py
    if [[ "$(uname)" == "Darwin" && -f "/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python" ]]; then
        sudo arch -i386 /System/Library/Frameworks/Python.framework/Versions/2.7/bin/python setup.py install
    else
        sudo python setup.py install
    fi

    cd ../../
fi

# Pip dependencies
sudo pip install -r requirements.txt
