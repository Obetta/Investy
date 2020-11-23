import pymongo

myclient = pymongo.MongoClient("mongodb://3.20.235.122:27017/")
mydb = myclient["411project"]

if mydb.authenticate('superadmin', "411project", source="admin"):
    mycol = mydb["Stock Historical Data"]

    myquery = {"Meta Data.2 Symbol": "MMM"}
    
    mydoc = list(mycol.find(myquery))[0]['Monthly Time Series']
    for key in mydoc:
      print(key)