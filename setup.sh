#!/usr/bin/bash
LIB="lib"

# Make third party folder
if [[ ! -d $LIB ]]; then
    mkdir $LIB
fi

# Setup virtual environment
sudo pip install virtualenv

virtualenv tcmusicbot-venv
source tcmusicbot-venv/bin/activate

# Get third party dependencies
if [[ ! -d "$LIB/pygrooveshark" ]]; then
    git clone "https://github.com/koehlma/pygrooveshark.git" $LIB/pygrooveshark

    cd $LIB/pygrooveshark
    python setup.py install

    cd ../../
fi

if [[ ! -d "$LIB/skype4py" ]]; then
    git clone "https://github.com/awahlig/skype4py.git" $LIB/skype4py

    cd $LIB/skype4py
    # arch -32 /System/Library/Frameworks/Python.framework/Versions/2.7/bin/
    python setup.py install

    cd ../../
fi

# Pip dependencies
pip install -r requirements.txt