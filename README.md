# Mapping Medical Procedure Costs all over the United States 

Inpatient Prospective Payment System Provider Summary for Top 100 Diagnoses FY2011


## Requirements

	* Make sure to `pip install -r requirements.txt` to install reqs for app (If on db add `--user` flag)
	* Postgres


## How to Setup DB

	1. First let's get our data by running `$ python datascraper.py`. This will download the data if you do not 
	already have it and create the CSVs for our database tables. 
	2. Next, run setup.py. This will create the database `mapbox_db`, create tables and populates them with the
	data downloaded.


## PSQL Cheatsheet

	```sql
	\l : List all dbs
	\dt : List all tables in database


	```