from pymongo import MongoClient
import csv

#Connect to mongo server on local host
client = MongoClient('mongodb://localhost:27017')

#Create a database -> This holds all the tables/collections
db = client['database']

#Create table labled elements
elements = db["elements"]
mappings = db["mappings"]
tags = db["tags"]


#Function:      Add csv data set to a database collection in MongoDB
#Inputs:        data - Name of csv file
#               collection - Name of table in MongoDB
#Outputs:       Creates/Modifies database to contain all the csv file data
def csvToCollection(data, collection):
    #Open element csv file
    with open(data, 'r') as file:

        reader = csv.reader(file)#initialize reader
        titles = next(reader)# Get all header vallue
        columns = len(titles)#Get the amount of header values

        #Lopp through each row in the csv file
        for elem in reader:
            n = 0 #Index of row
            document = {} #document to add to collection

            #Loop through each value in the given row
            while n != columns:
                document[titles[n]] = elem[n] #Add each field to a document
                n += 1 #increment index

            collection.insert_one(document) #insert completed document into collection named "elements"

#Function:      Get all data from the database about the given element name
#Inputs:        name - Element Name
#               collection - Name of table in MongoDB
#Outputs:       returns document about the prompted element
def getElementInfo(name, collection):
    retval=collection.find_one({"Element Name":name})
    if retval:
        del retval['_id']
    else:
        print(name)
    return retval

def tagMappingExists(rfid:str):
    try:
        if mappings.find_one({"uid":rfid}) == None:
            return False
        return True
    except:
        return False
    
def elementMappingExists(elementId:int):
    try:
        if mappings.find_one({"_id":elementId}) == None:
            return False
        return True
    except:
        return False

def getTagMappings(rfid):
    return mappings.find_one({"uid":rfid})

def mapTagToElementId(rfidTag:str, elementId:int):
    return mappings.insert_one({"uid":rfidTag,"_id":elementId})

   
    
def getTagInfo(name, collection):
    retval=collection.find_one({"Poster2":name})
    if retval:
        del retval['_id']
    else:
        print(name)
    return retval

def updateTag(name, tagID, collection):
    # Update the tag ID in the database
    collection.update_one({"Tag Name": name}, {"$set": {"Chem Tag ID": tagID}})
