# Mapping Medical Procedure Costs

Inpatient Prospective Payment System Provider Summary for Top 100 Diagnoses FY2011

[Production Server](http://intense-mapbox.herokuapp.com)


## Requirements

* Make sure to `pip install -r requirements.txt` to install reqs for app (If on db add `--user` flag)
* Postgres


## How to Setup DB

1. First let's get our data by running `$ python datascraper.py`. This will download the data if you do not 
already have it and create the CSVs for our database tables. 

2. Let's create the database by running `$ createdb mapbox_db` 

3. Next, run `$ python manage.py db migrate`. This will create tables with alembic migration control.

4. Now, run `$ python manage.py db upgrade`. This will apply the changes.

5. To add the data let's now run `$ python setup.py`. Then go through steps 3 and 4 again.


## PSQL Cheatsheet

```sql
\l : List all dbs
\dt : List all tables in database
heroku pg:psql : pulls up live db on heroku
heroku run python manage.py db upgrade --app intense-mapbox : after running local migrations, use remote upgrade

```