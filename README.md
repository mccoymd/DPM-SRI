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

If running on a GCP VM, add the 'flask' and 'postgres' network tags to the machine to open the correct ports

## To install dependencies run:

Dependencies are based on Python version 3.9.7 and pip 22.1
`pip3 install -r requirements.txt`


## DB
The app uses a Postgres relational db

To run the app on a new machine or test locally, the db needs to be initialized.
To do this, ensure psql is installed by running `psql --version`.
With psql installed, run `psql` to connect to the psql command line.
From here, run `CREATE DATABASE dpm_dev`. With the database created, run `flask db upgrade` to follow latest migration scripts.

To modify the database, make the necessary changes in `app/models.py`
After these changes are saved, run `flask db migrate -m "YOUR MESSAGE HERE"` to create a db migration script
Once this script has been created, run `flask db upgrade` which will execute the script and make the changes in the db

These changes can be confirmed using the psql command line or app
On the command line, run `psql` to connect to the psql server
`\l` will list all available databases
use `\c DATABASE_NAME` to connect to the database,`\c dpm_dev`to connect to your local db
Once connected to a database, `\dt` will list all relations in the database
To view the relations use `\d RELATION_NAME` and confirm changes


## TODO
- [] Look into restructuring data to be unique in transtion_rates table
- [] Import simulation results data at scale
- [] Scale query request
- [x] Import csv data through app
- [] Look into db table for storing previously created image urls
- [] Auto update updated_on db field
