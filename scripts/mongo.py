import pymongo
#---------------CHANGE IP ADDRESS HERE----------------
ipaddress = "52.7.221.41"
port = 27017
#---------------Connect to Database-----------------
client = pymongo.MongoClient(ipaddress,port)
db = client.test
#----------------Count-----------------
count = db.zips.count()
print count

#------------Query---------------------
q = db.zips.find({'pincode':632014})
for each in q:
	print each
