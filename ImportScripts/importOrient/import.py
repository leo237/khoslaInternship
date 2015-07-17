import pyorient
import csv
import sys
import re

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect( "root", "password" )
db_name = "zips"

if client.db_exists(db_name, pyorient.STORAGE_TYPE_MEMORY ):
    print "exists"
else:
    client.db_create( db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY )
    print "created"


client.db_open( db_name, "admin", "admin" )

try:
    cluster_id = client.command( "create class zip" )
except:
    cluster_id = 10

# cluster_id = client.command( "create class my_class extends V" )
# cluster_id = 10

with open('all_india_pin_code.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    count = 0
    for row in spamreader:
        if (count == 0):
            headers = row
        else:
            if (count>0):
                newRow = row
                row = []
                for each in newRow:
                    each = re.sub("[']", "", each)
                    each = re.sub(r"\\", "", each)
                    row.append(each)
                command = "Insert into zip CLUSTER zip_india ('" + headers[0] + "','" + headers[1] + "','" + headers[2] + "','" + headers[3] + "','" + headers[4] + "','" + headers[5] + "','" + headers[6] + "','" + headers[7] + "','" + headers[8] + "','" + headers[9] + "') VALUES('" + row[0] + "','" + row[1] + "','" + row[2] + "','" + row[3] + "','" + row[4] + "','" + row[5] + "','" + row[6] + "','" + row[7] + "','" + row[8] + "','" + row[9] + "')"
                client.command(command)
                print count
        count +=1
