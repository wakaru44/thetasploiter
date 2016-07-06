#!/bin/bash

echo "Hola pajaro"

echo "This is just the boilerplate code for a future installer. Go away."

virtualenv ENV
source ENV/bin/activate
pip install -r requirements.txt
