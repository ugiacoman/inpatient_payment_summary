import csv
import urllib
import requests

# 0:procedure, 1:id, 2:name, 3:street, 4:city, 5:state, 6:zip, 7:region, 8:totaldischarge, 9:covered, 10:total, 11:med

def writetoCSV_Loc(csv_2011, csv_2012, csv_2013):
	loc_csv = csv.writer(open("Location.csv","wb"))
	container_1 = []
	for col in csv_2011:
		if (col[1].lstrip("0") not in container_1) and (len(col[1]) > 1):
			container_1.append(col[1].lstrip("0"))
			loc_csv.writerow([col[1].lstrip("0"),col[4],col[3],col[5],col[6]])

	for col in csv_2012:
		if (col[1].lstrip("0") not in container_1) and (len(col[1]) > 1):
			container_1.append(col[1].lstrip("0"))
			loc_csv.writerow([col[1].lstrip("0"),col[4],col[3],col[5],col[6]])

	for col in csv_2013:
		if (col[1].lstrip("0") not in container_1) and (len(col[1]) > 1):
			container_1.append(col[1].lstrip("0"))
			loc_csv.writerow([col[1].lstrip("0"),col[4],col[3],col[5],col[6]])		

def writetoCSV_Provider(csv_2011, csv_2012, csv_2013):
	prov_csv = csv.writer(open("Provider.csv","wb"))
	container = []
	for col in csv_2011:
		if col[1].lstrip("0") not in container:
			container.append(col[1].lstrip("0"))
			is_hospital = False
			if "hospital" in col[2].lower():
				is_hospital = True
			if len(col[1]) > 1:
				prov_csv.writerow([col[1].lstrip("0"),col[2], is_hospital])	

	for col in csv_2012:
		if col[1].lstrip("0") not in container:
			container.append(col[1].lstrip("0"))
			is_hospital = False
			if "hospital" in col[2].lower():
				is_hospital = True
			if len(col[1]) > 1:
				prov_csv.writerow([col[1].lstrip("0"),col[2], is_hospital])	

	for col in csv_2013:
		if col[1].lstrip("0") not in container:
			container.append(col[1].lstrip("0"))
			is_hospital = False
			if "hospital" in col[2].lower():
				is_hospital = True
			if len(col[1]) > 1:

				prov_csv.writerow([col[1].lstrip("0"),col[2], is_hospital])						

def writetoCSV_Diagnosis(csv_2011, csv_2012, csv_2013):
	diag_csv = csv.writer(open("Diagnosis.csv","wb"))

	for col in csv_2011:
		if len(col[1]) > 1:
			diag_csv.writerow([col[0],col[1].lstrip("0"), "2011", col[10].strip("$"),col[11].strip("$"),col[9].strip("$"),col[8]])

	for col in csv_2012:
		if (len(col[1]) > 1) and (col[0] != "DRG Definition"):
			diag_csv.writerow([col[0],col[1].lstrip("0"), "2012", col[10].strip("$"),col[11].strip("$"),col[9].strip("$"),col[8]])

	for col in csv_2013:
		if len(col[1]) > 1 and (col[0] != "DRG Definition"):
			diag_csv.writerow([col[0],col[1].lstrip("0"), "2013", col[10].strip("$"),col[11].strip("$"),col[9].strip("$"),col[8]])
		
def download_file(url, filename):
	local_filename = filename
	# NOTE the stream=True parameter
	r = requests.get(url, stream=True)
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
	return local_filename

def runScripts(file_2011, file_2012, file_2013):
	csv_2011 = csv.reader(file_2011)
	csv_2012 = csv.reader(file_2012)
	csv_2013 = csv.reader(file_2013)
	file_2011.seek(0)
	file_2012.seek(0)
	file_2013.seek(0)	
	writetoCSV_Provider(csv_2011, csv_2012, csv_2013)	
	file_2011.seek(0)
	file_2012.seek(0)
	file_2013.seek(0)
	writetoCSV_Diagnosis(csv_2011, csv_2012, csv_2013)	
	file_2011.seek(0)
	file_2012.seek(0)
	file_2013.seek(0)
	writetoCSV_Loc(csv_2011,csv_2012,csv_2013)	


def main():
    try:
    	print ('\nLooking for CSV...')
        f = open('source_2011.csv', 'rb')
        f = open('source_2012.csv', 'rb')
        f = open('source_2013.csv', 'rb')
        print ('CSVs found, generating separate CSV files for tables.')
        runScripts(f_11, f_12, f_13)
    except IOError:
		print ('Not all CSVs found, generating separate CSV files for tables.')

		url_2011 = 'https://raw.githubusercontent.com/ugiacoman/mapbox_data/master/source_2011.csv'
		url_2012 = 'https://raw.githubusercontent.com/ugiacoman/mapbox_data/master/source_2012.csv'
		url_2013 = 'https://raw.githubusercontent.com/ugiacoman/mapbox_data/master/source_2013.csv'
		file_2011 = download_file(url_2011, "source_2011.csv")
		file_2012 = download_file(url_2012, "source_2012.csv")
		file_2013 = download_file(url_2013, "source_2013.csv")
		f_11 = open(file_2011, 'rb')
		f_12 = open(file_2012, 'rb')
		f_13 = open(file_2013, 'rb')
		runScripts(f_11, f_12, f_13)

main()


