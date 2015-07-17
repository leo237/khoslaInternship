import csv
import sys
from time import time
from pprint import pprint

from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery, N1QLError

CONNECTION_STRING = "couchbase://localhost/zips"

bkt = Bucket(CONNECTION_STRING)

with open('all_india_pin_code.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	count = 0
	for row in spamreader:
		if (count == 0):
			headers = row
			headers.insert(0,'id')
		else:
			if (count>0):
				newRow = row
				newRow.insert(0,str(count))
				dataDict = {headers[0]:newRow[0], headers[1]:newRow[1],headers[2]:newRow[2],headers[3]:newRow[3],headers[4]:newRow[4],headers[5]:newRow[5],headers[6]:newRow[6],headers[7]:newRow[7],headers[8]:newRow[8],headers[9]:newRow[9],headers[10]:newRow[10]}
				bkt.upsert('pincode' + str(count),dataDict)
				print count
		count +=1

print "I think it's done."

