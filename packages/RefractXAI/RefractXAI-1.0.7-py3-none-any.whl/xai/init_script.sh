#!/bin/bash
echo "Installing packaeges"
pip install bs4==0.0.1

if [ -z $datasource ]; then
    echo "datasource environment variable is not set"
    exit 1
fi

pip install refractio[$datasource] -t /packages/custom_plugin/refractio
pip install requests -t /packages/custom_plugin/refractio

export PYTHONPATH="$PYTHONPATH:/packages/custom_plugin/refractio"

echo "Done with dependency installtion!";

