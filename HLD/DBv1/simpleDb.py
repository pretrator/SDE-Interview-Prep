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

    # Ram
    # Hard disk 
    # Network
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

# RAM -> 4GB
# CPU -> 
# HDD -> 100 -> 
# Network

#     RAM 200GB 
#     HDD 1000GB 
#     # Ram
#         -> O(1) for update
#         => O(N) for new key
#     # Hard disk 
#         -> Read IOPS 10GBps
#         -> Write IOPS 40GPps
#         200GB 
#         1 write -> 

#     # Network
#         -> 1GBps
#         -> latency -> 
# delta -> 





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


 
# read -> 
#     speed of read -> 

# write ->
#     10GB
#     100GB 
#     100GB 

# Write Amplification


# 100GB HDD
# 4GB RAM

# How much data we can store
#     Ankur -> 4GB
#     Chiya -> 
#     Khusboo -> 

# Read -> 
#     1 read per second 
#     20k reads per second ->
#         stress 
#             -> Network BandWidth (4mbps)
#                 15000
#             -> Network CArd (10 GBPS)
#             -> Ram bus speed 48GBPS
#             -> Network Queue =

# /simpleDb/read/key

Write -> 
    1 write per second 
    Neto