import csv
import urllib
import requests

# 0:procedure, 1:id, 2:name, 3:street, 4:city, 5:state, 6:zip, 7:region, 8:totaldischarge, 9:covered, 10:total, 11:med

def writetoCSV_Loc(csv_f):
	loc_csv = csv.writer(open("Location.csv","wb"))
	container_1 = []
	for col in csv_f:
		if col[1] not in container_1:
			container_1.append(col[1])
			loc_csv.writerow([col[1],col[4],col[3],col[5],col[6]])

def writetoCSV_Provider(csv_f):
	prov_csv = csv.writer(open("Provider.csv","wb"))
	container = []
	for col in csv_f:
		if col[1] not in container:
			container.append(col[1])
			is_hospital = False
			if "hospital" in col[2].lower():
				is_hospital = True
			prov_csv.writerow([col[1],col[2], is_hospital])

def writetoCSV_Diagnosis(csv_f):
	diag_csv = csv.writer(open("Diagnosis.csv","wb"))
	for col in csv_f:
		diag_csv.writerow([col[0],col[1],col[10].strip("$"),col[11].strip("$"),col[9].strip("$"),col[8]])
		
def download_file(url):
	local_filename = "Inpatient_Prospective_Payment_System__IPPS__Provider_Summary_for_the_Top_100_Diagnosis-Related_Groups__DRG__-_FY2011.csv"
	# NOTE the stream=True parameter
	r = requests.get(url, stream=True)
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
	            #f.flush() commented by recommendation from J.F.Sebastian
	return local_filename

def runScripts(file):
	csv_f = csv.reader(file)
	writetoCSV_Provider(csv_f)
	writetoCSV_Diagnosis(csv_f)
	writetoCSV_Loc(csv_f)       
	print("Finished.") 


def main():
    try:
    	print ('\nLooking for CSV...')
        f = open('Inpatient_Prospective_Payment_System__IPPS__Provider_Summary_for_the_Top_100_Diagnosis-Related_Groups__DRG__-_FY2011.csv', 'rb')
        print ('CSV found, generating separate CSV files for tables.')
        runScripts(f)
        f.close()
    except IOError:
		print ('CSV not found, downloading from source...')

		url = 'https://data.cms.gov/api/views/97k6-zzx3/rows.csv?accessType=DOWNLOAD&bom=true'
		file = download_file(url)
		f = open(file, 'rb')
		runScripts(f)
		print("Finished.") 
		f.close()

main()


