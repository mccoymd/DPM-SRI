--to run app run commands in DPM-SRI directory
export FLASK_APP=runSRI.py
export FLASK_ENV=development
####flask run
python3 -m flask run --host=0.0.0.0 --port=5000


to run on the linux machine, you can simply run:

bash launchApp.sh


To install dependencies run:

`pip3 install -r requirements.txt`


Use `flask db migrate` to create automatic db migrations

Use `flask db upgrade/downgrade` to apply or remove the migrations
