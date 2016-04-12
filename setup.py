from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
from app import db


def process_file(conn, table_name, file_object):

	SQL_STATEMENT = """
	COPY %s FROM STDIN WITH
	    CSV
	    HEADER
	    DELIMITER AS ','
	"""
	cursor = conn.cursor()
	print("Importing %s" % table_name)
	cursor.copy_expert(sql=SQL_STATEMENT % table_name, file=file_object)
	conn.commit()
	cursor.close()


def main():
	print("Creating Table Schemas")
	db.create_all()
	conn = None
	#change to your own personal settings
	conn = connect(dbname='mapbox_db', user='uli', password='st')

	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = conn.cursor()
	
	print("Importing Data")
	prov_file = open("Provider.csv")
	loc_file = open("Location.csv")
	diag_file = open("Diagnosis.csv")
	try:
	    process_file(conn, 'provider', prov_file)
	    process_file(conn, 'location', loc_file)
	    process_file(conn, 'diagnosis', diag_file)
	finally:
	    conn.close()

main()