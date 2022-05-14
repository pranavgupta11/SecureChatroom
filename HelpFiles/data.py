import csv
import hashlib
# field names
fields = ['Enroll', 'Fname', 'Lname', 'Password', 'Hash']
# data rows of csv file
# Creating a file
rows = []
file1 = open("db.txt", "r")
L = file1.readlines()
for i in L:
    data = i.split()
    h = hashlib.new('sha256')
    pwd = bytes(data[3], 'utf-8')
    h.update(pwd)
    data.append(h.hexdigest())
    print(data)
    rows.append(data)
	
# name of csv file
filename = "ref.csv"
	
# writing to csv file
with open(filename, 'w') as csvfile:
	# creating a csv writer object
	csvwriter = csv.writer(csvfile)
		
	# writing the fields
	csvwriter.writerow(fields)
		
	# writing the data rows
	csvwriter.writerows(rows)
file1.close()
