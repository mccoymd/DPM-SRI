# DPM-SRI

## To run app run commands in DPM-SRI directory

```
export FLASK_APP=runSRI.py
export FLASK_ENV=development
####flask run
python3 -m flask run --host=0.0.0.0 --port=5000
```


## To run on the linux machine, you can simply run:

`bash launchApp.sh`

## To install dependencies run:

`pip3 install -r requirements.txt`


## DB
The app uses a Postgres relational db
To modify the database, make the necessary changes in `app/models.py`
After these changes are saved, run `flask db migrate -m "YOUR MESSAGE HERE"` to create a db migration script
Once this script has been created, run `flask upgrade` which will execute the script and make the changes in the db

These changes can be confirmed using the psql command line or app
On the command line, run `psql` to connect to the psql server
`\l` will list all available databases
use `\c DATABASE_NAME` to connect to the database,`\c dpm_dev`to connect to your local db
Once connected to a database, `\dt` will list all relations in the database
To view the relations use `\d RELATION_NAME` and confirm changes
