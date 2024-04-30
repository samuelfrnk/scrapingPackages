#!/bin/bash

# # PyPI URL
# pypi_url="https://pypi.org/project/alibi/"

# # Extract the package name from the URL
# package_name=$(echo $pypi_url | sed 's#.*/project/\(.*\)/#\1#')

PACKAGE_NAME=$1
ENV_NAME="env_$PACKAGE_NAME"
if [ ! -d $ENV_NAME ]; then
	echo 'Create a virtual environment'
	python3 -m venv $ENV_NAME #&> /dev/null

	echo 'Activate the virtual environment'
	source $ENV_NAME/bin/activate #&> /dev/null
	
	echo 'Update the virtual environment'
	pip install -U pip setuptools wheel #&> /dev/null

	echo "Install $PACKAGE_NAME"
	pip install $PACKAGE_NAME &> /dev/null
else
	. $ENV_NAME/bin/activate	
fi

pip show $PACKAGE_NAME | grep '^Name:' | awk -F': ' '{print $2}'