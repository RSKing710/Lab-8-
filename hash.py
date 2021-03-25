#!/usr/bin/env python3
#Jonathan Goohs and Ryan Serrato
#Lab 8: Parts 1-3
#CAPT Doherty SY402

#imports
import hashlib 
import os 
import time 

#Collaborations
#MIDN Goohs wrote hashing portion
#MIDN Serrato wrote file exceptions and iterations of initial file parsing
#design
#have a dictionary with the paths as keys and the values as tuples of the hashes and their respective timestamp for being observed

#start source code
ignoreList = ['/dev', '/proc', '/run', '/sys', '/tmp', '/var/lib', '/var/run']

listOfFiles = []
fileDict = {}
rootdir = "/"

def traverseOS(): 
    for subdir, dirs, files in os.walk(rootdir):    #traverse through the entire file system using os.walk
        for file in files: 
            path = os.path.join(subdir, file)
            if path.startswith('/dev') or path.startswith('/proc') or path.startswith('/run') or path.startswith('/sys') or path.startswith('/tmp') or path.startswith('/var/lib') or path.startswith('/var/run'): 
                continue
            listOfFiles.append(path)
            print(path)    
    return listOfFiles        


def getFileInfo(listOfFiles): 
    for files in listOfFiles:
        try:
            time = os.path.getmtime(files)
            hashf = hashlib.sha256()
            with open(files, "rb") as rf:
                for byte in iter(lambda: rf.read(4096), b""):
                    hashf.update(byte)
                print("File content's hash: " + hashf.hexdigest())
            val = [hashf.hexdigest(), time]
            fileDict[files] = val
        except:
            print("Exception occured")

def printData(dictionary): 
    with open('storedhash.txt', 'w+') as f: 
        for k,v in dictionary.items():
            f.write(f'{k}:{v}\n')

def main(): 
    listOfFiles = traverseOS()
    dictionary = getFileInfo(listOfFiles)
    printData(dictionary)

if __name__ == "__main__":
    main()

#retrieve comparison of initial flags vs. later point flags
#dump things into new list, changed list, deleted list

#os.path.getmtime(file)      #retreives the last modified time 