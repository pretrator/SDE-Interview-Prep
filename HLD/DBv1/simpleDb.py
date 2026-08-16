# Functional Req
# 1. Read, Write
# 2. Persist

# SimpleDB
#     - read
#     - write

# kv

# planning 
#  init mai file se data load krke memory self.hash mai daal lo
# 1. Init
    # - create file if not FileExistsError
    # - create hash = 
    #     readfromFile
    #     dict bana kar 

from pathlib import Path
import json
import os
 
class SimpleDB():
    def __init__(self, dbName):
        self.file = self.createFileIfNotExist(dbName)
        self.hash = self.loadFromFile(dbName)

    def createFileIfNotExist(self, dbName):
        Path(dbName).touch(exist_ok=True)
        return open(dbName, "r+")
    
    def read(self, key):
        if key not in self.hash: return
        return self.hash[key]

    def write(self, key, value):
        self.hash[key] = value
        self.persist()

    def persist(self):
        serialized = json.dumps(self.hash)
        self.file.seek(0)
        self.file.truncate()
        self.file.write(serialized)
        self.file.flush()
        os.fsync(self.file.fileno())
        

    def loadFromFile(self, dbName):
        with open(dbName, "r", encoding="utf-8") as file:
            file_contents = file.read()
            if file_contents == "":
                return dict()
            deserialized = json.loads(file_contents)
            return deserialized




# HDD OFFset 14000 15000
# File - 0     1000
# 500 
# truncate()
# 0 => 500
# 14000-14500

sdb = SimpleDB("Chiya")
# sdb.write("Name", "Chiya")
# sdb.write("SName", "Srivastava")
print(sdb.read("SName"))



read -> 
    speed of read -> 

write ->
    10GB
    100GB 
    100GB 

Write Amplification