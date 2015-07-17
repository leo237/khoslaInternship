#--------------------Couchbase Server Read Query------------------
from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery, N1QLError
from pprint import pprint 
import time
server = "52.27.232.218"
bucketname = "zips"

Connection = "couchbase://" + server + "/" + bucketname
print Connection
p0 = time.time()
bkt = Bucket(Connection)
print "It takes ", time.time()-p0, " seconds to establish connection" 

#------------------CREATE INDEX HERE--------------------------------

#bkt.n1ql_query('CREATE PRIMARY INDEX ON zips using GSI').execute()
#bkt.n1ql_query('CREATE INDEX zips_index ON zips(pincode) using GSI').execute()

#---------------N1QL Query goes in here---------------------------

t1 = time.time()
query = "SELECT * FROM `zips` where pincode= '632014'"
q = N1QLQuery(query)


for row in bkt.n1ql_query(q):
    print row
t = time.time()-t1

print("It takes %.15f seconds to query" % t)
with open("result.csv", "a") as myfile:
    myfile.write(str("%.15f" % t)+"\n")

#----------------------MongoDB Read Query----------------------------
#from pymongo import MongoClient
#---------------CHANGE IP ADDRESS HERE----------------
#ipaddress = "52.7.244.128"
#port = 27017
#---------------Connect to Database-----------------
#client = MongoClient(ipaddress,port)
#db = client.test
#----------------Count-----------------
#count = db.zips.count()
#print count

#------------Query---------------------
#q = db.zips.find({'pincode':632014})
#for each in q:
#    print each
