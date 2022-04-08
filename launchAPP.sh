#/bin/bash

export FLASK_APP=runSRI.py
export FLASK_ENV=development

pip3 install -r requirements.txt

python3 -m flask run --host=0.0.0.0 --port=5000
