import csv
import urllib
import requests
import geocoder
from datetime import datetime

def geocode(row_mem, memory, mem_writer):
	in_file = open("Location.csv", "rb")
	reader = csv.reader(in_file)
	for row in reader:
		if row[0] not in row_mem:
			print(row[0])
			g = geocoder.google(str(row[2] + ','+ row[3]))	
			if len(g.latlng) > 1:
				row[5] = g.latlng[1]
				row[6] = g.latlng[0]
				mem_writer.writerow(row)
				print(g.latlng)

	



def main():
	memory = []
	row_mem = []
	try:
		print("Memory found!")
		with open('geo.csv', 'rb') as f:
		    reader = csv.reader(f)
		    for row in reader:
		    	row_mem.append(row[0])
		    	memory.append(row)
		    print(row_mem)
		    # reader.close()
		    mem_csv = open("geo.csv", 'wb')
		    mem_writer = csv.writer(mem_csv)
		    for item in memory:
		    	mem_writer.writerow(item)
		    geocode(row_mem, memory, mem_writer)
	except IOError:
		print("Memory not found")
		mem_csv = open("geo.csv", 'wb')
		mem_writer = csv.writer(mem_csv)
		geocode(row_mem, memory, mem_writer)
main()