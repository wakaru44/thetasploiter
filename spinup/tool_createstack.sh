#!/bin/bash

echo "create a stack"
echo "Any parameter passed after calling the script will be appended to the aws cloudformation command"
NAME=kalinstance$(cat version.md)
TMPL=kalinstance.json
CFNPARAMS=create-stack-parameters.json


# TODO: modify the key to be a parameter
# swetter version with file based parameters
aws cloudformation create-stack  --stack-name $NAME --template-body file://$TMPL  --cli-input-json file://$CFNPARAMS ${@:2}  | tee -a stack_id.log


